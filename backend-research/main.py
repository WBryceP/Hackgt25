import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import FactCheckRequest, FactCheckResponse, ExaAnswerResponse
from exa_service import ExaService

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
