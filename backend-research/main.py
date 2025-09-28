import json
# from fastapi import FastAPI, HTTPException, Depends
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from pydantic import BaseModel, HttpUrl, field_validator
import os, httpx, uuid
from ytdl import download_to_disk
from settings import settings
from dotenv import load_dotenv
from models import FactCheckRequest, FactCheckResponse, ExaAnswerResponse
from exa_service import ExaService
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(title="Backend Research API", version="1.0.0")

RAPIDAPI_KEY = settings.RAPIDAPI_KEY
RAPIDAPI_HOST = settings.RAPIDAPI_HOST

RAPIDAPI_KEY = settings.RAPIDAPI_KEY
RAPIDAPI_HOST = settings.RAPIDAPI_HOST

VIDEO_STORAGE_DIR = os.path.join(os.path.dirname(__file__), "downloaded_videos")
os.makedirs(VIDEO_STORAGE_DIR, exist_ok=True)

# Mount the directory as a static files path. This makes files publicly accessible.
app.mount("/videos", StaticFiles(directory=VIDEO_STORAGE_DIR), name="videos")

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

# Middleware to handle HEAD requests
@app.middleware("http")
async def head_request_middleware(request: Request, call_next):
    if request.method == "HEAD":
        # Convert HEAD to GET and return only headers
        request.scope["method"] = "GET"
        response = await call_next(request)
        return Response(status_code=response.status_code, headers=response.headers)
    return await call_next(request)

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
        result["startSec"] = request.startSec
        result["endSec"]  = request.endSec
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
    Download from RapidAPI and return permanent URLs
    """
    path = f"/file/{jobId}/{filename}"
    url = f"https://{settings.RAPIDAPI_HOST}{path}"

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.get(url, headers=BROWSER_HEADERS)

    if response.status_code != 200:
        # Your error handling...
        pass

    # Generate unique filename
    file_extension = os.path.splitext(filename)[1] or ".mp4"
    unique_filename = f"{jobId}_{uuid.uuid4().hex[:8]}{file_extension}"
    local_filepath = os.path.join(VIDEO_STORAGE_DIR, unique_filename)

    # Save file permanently
    with open(local_filepath, 'wb') as f:
        f.write(response.content)

    # Generate permanent URLs
    video_url = f"https://neda-pericardial-unanachronously.ngrok-free.dev/videos/{unique_filename}"
    embed_url = f"https://neda-pericardial-unanachronously.ngrok-free.dev/embed/{unique_filename}"

    return {
        "status": "ok",
        "direct_video_url": video_url,
        "embed_url": embed_url,         # Web page with embedded video; use for TwelveLabs
        "filename": unique_filename,
        "message": "Video permanently stored and available at the provided URLs"
    }

@app.get("/videos/{filename}")
async def get_video(filename: str):
    """
    Stream a video file for playback in the browser.
    """
    local_filepath = os.path.join(VIDEO_STORAGE_DIR, filename)

    if not os.path.exists(local_filepath):
        raise HTTPException(status_code=404, detail="Video file not found")

    return FileResponse(
        path=local_filepath,
        media_type="video/mp4",
        filename=filename,
        # These headers make it embeddable and permanent
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "public, max-age=31536000"  # Cache for 1 year
        }
    )

@app.get("/embed/{filename}", response_class=HTMLResponse)
async def embed_video(filename: str):
    """
    Return an HTML page with the video embedded
    """
    video_url = f"https://neda-pericardial-unanachronously.ngrok-free.dev/videos/{filename}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video: {filename}</title>
        <style>
            body {{ margin: 0; padding: 20px; background: #f5f5f5; }}
            .video-container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
            video {{ width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <div class="video-container">
            <h2>Video: {filename}</h2>
            <video controls autoplay muted>
                <source src="{video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <p><a href="{video_url}" download>Download Video</a></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
