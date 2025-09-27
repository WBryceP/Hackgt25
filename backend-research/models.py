from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class FactCheckRequest(BaseModel):
    claim: str = Field(..., description="The claim to fact-check", min_length=1)


class AnswerCitation(BaseModel):
    id: str = Field(..., description="The temporary ID for the document")
    url: str = Field(..., description="The URL of the search result")
    title: str = Field(..., description="The title of the search result")
    author: Optional[str] = Field(None, description="The author of the content")
    publishedDate: Optional[str] = Field(None, description="The creation date")
    text: str = Field(..., description="The full text content of the source")
    image: Optional[str] = Field(None, description="The URL of the associated image")
    favicon: Optional[str] = Field(None, description="The URL of the favicon")


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
    total: float = Field(..., description="Total dollar cost for the request")
    breakDown: List[CostBreakdownItem] = Field(default_factory=list)
    perRequestPrices: Optional[PerRequestPrices] = None
    perPagePrices: Optional[PerPagePrices] = None


class ExaAnswerResponse(BaseModel):
    answer: str = Field(..., description="The generated answer based on search results")
    citations: List[AnswerCitation] = Field(default_factory=list)
    costDollars: Optional[CostDollars] = None


class FactCheckResponse(BaseModel):
    title: str = Field(..., description="A very short title for the claim made")
    description: str = Field(..., description="A description of the claim made. Keep the description without fluff like a news sub-headline.")
    truthfulnessScore: int = Field(
        ..., 
        description="A truthfulness score between 1-5. The score should represent 1 - Untrue, 2-Mostly Untrue 3-Mix of Truth 4-Mostly True 5-True", 
        ge=1, 
        le=5
    )
    response: str = Field(
        ..., 
        description="A medium-length response summarizing why the claim is true or untrue"
    )
    sources: List[AnswerCitation] = Field(
        default_factory=list,
        description="Sources used to fact-check the claim"
    )
    exaResponse: Optional[ExaAnswerResponse] = Field(
        None,
        description="Full Exa API response for reference"
    )
