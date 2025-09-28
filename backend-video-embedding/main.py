import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import EmbedRequest, EmbedResponse, EmbedStatus
from twelvelabs_service import TwelveLabsService


load_dotenv()

app = FastAPI(
    title="Video Embedding Service",
    version="1.0.0",
    description="Service to create TwelveLabs index, embed video, and return clips"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_twelvelabs_service() -> TwelveLabsService:
    try:
        return TwelveLabsService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def root():
    return {"message": "Video Embedding Service", "version": "1.0.0"}


@app.post("/embed", response_model=EmbedResponse)
async def embed_video(
    req: EmbedRequest,
    svc: TwelveLabsService = Depends(get_twelvelabs_service)
):
    try:
        index_id = await svc.ensure_index()
        task_id = await svc.submit_video(req.downloadUrl)
        video_id = await svc.poll_until_ready(task_id)
        # Use filter to extract claim/stat/graphic clips
        highlights = await svc.run_filter(video_id)
        return EmbedResponse(
            taskId=task_id,
            indexId=index_id,
            videoId=video_id,
            clips=highlights,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to embed video: {str(e)}")


@app.get("/status/{taskId}", response_model=EmbedStatus)
async def get_status(taskId: str, svc: TwelveLabsService = Depends(get_twelvelabs_service)):
    status_info = await svc.get_task_status(taskId)
    return EmbedStatus(taskId=taskId, status=status_info.get("status", "unknown"), progressPct=status_info.get("progressPct", 0))


@app.get("/config")
def get_config():
    return {
        "tl_api_configured": bool(os.getenv("TL_API_KEY") or os.getenv("TWELVELABS_API_KEY")),
        "environment": os.getenv("ENV", "development"),
    }

