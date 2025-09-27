import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, HttpUrl, field_validator
import os, httpx
from ytdl import download_to_disk
from settings import settings
from dotenv import load_dotenv
from models import FactCheckRequest, FactCheckResponse, ExaAnswerResponse
from exa_service import ExaService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Backend Research API", version="1.0.0")

RAPIDAPI_KEY = settings.RAPIDAPI_KEY
RAPIDAPI_HOST = settings.RAPIDAPI_HOST

RAPIDAPI_KEY = settings.RAPIDAPI_KEY
RAPIDAPI_HOST = settings.RAPIDAPI_HOST

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Backend Research API", 
    version="1.0.0",
    description="API for fact-checking claims using Exa search"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Exa service
def get_exa_service() -> ExaService:
    try:
        return ExaService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Backend Research API", "version": "1.0.0"}


@app.post("/fact-check", response_model=FactCheckResponse)
async def fact_check_claim(
    request: FactCheckRequest,
    exa_service: ExaService = Depends(get_exa_service)
):
    """
    Fact-check a claim using Exa search and return a truthfulness analysis.
    
    This endpoint takes a claim and uses the Exa API to search for relevant
    information and provide an analysis of the claim's truthfulness.
    """
    try:
        result = await exa_service.fact_check_claim(request.claim)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fact-check claim: {str(e)}"
        )


@app.post("/exa-search", response_model=ExaAnswerResponse)
async def exa_search(
    query: str,
    exa_service: ExaService = Depends(get_exa_service)
):
    """
    Direct access to Exa's answer API for general queries.
    """
    try:
        result = await exa_service.answer_query(query)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search Exa: {str(e)}"
        )


@app.get("/config")
def get_config():
    """Get API configuration status"""
    has_exa_key = bool(os.getenv("EXA_API_KEY"))
    return {
        "exa_api_configured": has_exa_key,
        "environment": os.getenv("ENV", "development")
    }


# class IngestRequest(BaseModel):
#     youtube_url: HttpUrl
#     quality: int = 720

# @app.post("/videos")
# def create_video(req: IngestRequest):
#     try:
#         out = download_to_disk(
#             youtube_url=str(req.youtube_url),
#             out_path=f"videos/demo/video_{req.quality}p.mp4",
#             quality=req.quality,
#             rapidapi_key=os.environ["RAPIDAPI_KEY"]
#         )
#         return {"status": "ok", "path": out["path"]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
class DownloadRequest(BaseModel):
    url: HttpUrl
    format: str = "mp4"
    quality: int = 720

    @field_validator("format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        allowed = {"mp4", "mp3", "webm", "m4a"}
        if v.lower() not in allowed:
            raise ValueError(f"format must be one of {sorted(allowed)}")
        return v.lower()

@app.post("/video_info")
async def video_info(req: DownloadRequest):
    data = await post_rapidapi("/video_info", {"url": str(req.url)})
    return {"status": "ok", "data": data}

@app.post("/download")
async def download(req: DownloadRequest):
    data = await post_rapidapi("/download", {
        "url": str(req.url),
        "format": req.format,
        "quality": req.quality,
    })
    if "jobId" not in data:
        raise HTTPException(status_code=502, detail={"message": "invalid response from upstream", "data": data})
    return {"status": "ok", "jobId": data["jobId"]}

@app.get("/status/{jobId}")
async def status(jobId: str):
    data = await get_rapidapi(f"/status/{jobId}")
    return {"status": "ok", "data": data}

@app.get("/downloadFile/{jobId}/{filename}")
async def download_file(jobId: str, filename: str):
    """
    Download the file and return it directly
    """
    path = f"/file/{jobId}/{filename}"
    
    # Use your existing get_rapidapi function but handle the binary response
    url = f"https://{settings.RAPIDAPI_HOST}{path}"
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.get(url, headers=BROWSER_HEADERS)
    
    if response.status_code != 200:
        # Use similar error handling as your get_rapidapi function
        text = response.text
        try:
            data = response.json()
            error_msg = data.get("error") or data.get("message") or text[:300]
        except:
            error_msg = text[:300]
        
        raise HTTPException(status_code=502, detail={
            "upstream_status": response.status_code,
            "message": error_msg,
        })
    
    # Return the file content directly
    from fastapi.responses import Response
    import mimetypes
    
    content_type = response.headers.get('content-type')
    if not content_type:
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    return Response(
        content=response.content,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
    # """
    # Get the public URL for the downloaded video/audio file.
    
    # Args:
    #     jobId: The job ID returned from the /download endpoint
    #     filename: The filename to download (e.g., 'video.mp4', 'audio.mp3')
    # """
    # # Construct the direct download URL
    # download_url = f"https://{settings.RAPIDAPI_HOST}/file/{jobId}/{filename}"
    
    # # Return the public URL that TwelveLabs can use directly
    # return {
    #     "status": "ok", 
    #     "download_url": download_url,
    #     "headers_required": {
    #         "x-rapidapi-host": settings.RAPIDAPI_HOST,
    #         "x-rapidapi-key": settings.RAPIDAPI_KEY
    #     }
    # }

BROWSER_HEADERS = {
    "Content-Type": "application/json",
    "x-rapidapi-host": settings.RAPIDAPI_HOST,
    "x-rapidapi-key": settings.RAPIDAPI_KEY,
    # Browser-y headers:
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity",
    "Origin": "https://rapidapi.com",
    "Referer": "https://rapidapi.com/",
}

async def post_rapidapi(path: str, payload: dict):
    url = f"https://{settings.RAPIDAPI_HOST}{path}"
    async with httpx.AsyncClient(timeout=60.0, http2=False) as client:
        r = await client.post(url, headers=BROWSER_HEADERS, json=payload)
    text = r.text
    try:
        data = r.json()
        if isinstance(data, str) and data.strip().startswith("{"):
            data = json.loads(data)
    except ValueError:
        data = {"raw": text}

    if r.status_code >= 400 or ("error" in data and "Automated requests" in (data.get("error") or "")):
        raise HTTPException(status_code=502, detail={
            "upstream_status": r.status_code,
            "message": data.get("error") or data.get("message") or text[:300],
        })
    return data

async def get_rapidapi(path: str):
    url = f"https://{settings.RAPIDAPI_HOST}{path}"
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Use GET method instead of POST
        r = await client.get(url, headers=BROWSER_HEADERS) # Note: 'GET' here
    # ... (keep the same response handling logic as your post_rapidapi function)
    text = r.text
    try:
        data = r.json()
        if isinstance(data, str) and data.strip().startswith("{"):
            data = json.loads(data)
    except ValueError:
        data = {"raw": text}

    if r.status_code >= 400:
        raise HTTPException(status_code=502, detail={
            "upstream_status": r.status_code,
            "message": data.get("error") or data.get("message") or text[:300],
        })
    return data