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

class AnswerCitation(BaseModel):
    id: str
    url: str
    title: str
    author: Optional[str] = None
    publishedDate: Optional[str] = None
    text: str
    image: Optional[str] = None
    favicon: Optional[str] = None

class CostBreakdown(BaseModel):
    keywordSearch: float = 0
    neuralSearch: float = 0
    contentText: float = 0
    contentHighlight: float = 0
    contentSummary: float = 0

class CostBreakdownItem(BaseModel):
    search: float = 0
    contents: float = 0
    breakdown: CostBreakdown

class PerRequestPrices(BaseModel):
    neuralSearch_1_25_results: float = 0.005
    neuralSearch_26_100_results: float = 0.025
    neuralSearch_100_plus_results: float = 1
    keywordSearch_1_100_results: float = 0.0025
    keywordSearch_100_plus_results: float = 3

class PerPagePrices(BaseModel):
    contentText: float = 0.001
    contentHighlight: float = 0.001
    contentSummary: float = 0.001

class CostDollars(BaseModel):
    total: float
    breakDown: List[CostBreakdownItem] = []
    perRequestPrices: Optional[PerRequestPrices] = None
    perPagePrices: Optional[PerPagePrices] = None

class ExaAnswerResponse(BaseModel):
    answer: str
    citations: List[AnswerCitation] = []
    costDollars: Optional[CostDollars] = None

class FactCheckResponse(BaseModel):
    startSec: float = Field(..., ge=0)
    endSec: float = Field(..., gt=0)
    title: str
    description: str
    truthfulnessScore: int = Field(..., ge=1, le=5)
    response: str
    sources: List[AnswerCitation] = []
    exaResponse: Optional[ExaAnswerResponse] = None

class EnrichedClip(BaseModel):
    clip: Clip
    factCheck: Optional[FactCheckResponse] = None
