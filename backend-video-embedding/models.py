from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional


class EmbedRequest(BaseModel):
    downloadUrl: HttpUrl = Field(..., description="Direct download URL for the video")


class Clip(BaseModel):
    startSec: float = Field(..., ge=0)
    endSec: float = Field(..., gt=0)
    description: str = Field(..., min_length=1)


class EmbedStatus(BaseModel):
    taskId: str
    status: str
    progressPct: Optional[float] = 0


class EmbedResponse(BaseModel):
    taskId: str
    indexId: str
    videoId: str
    clips: List[Clip] = Field(default_factory=list)

