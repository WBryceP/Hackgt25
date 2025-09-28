import os
import httpx
import json
import re
from typing import Optional
from fastapi import HTTPException
from models import ExaAnswerResponse, FactCheckResponse, AnswerCitation


class ExaService:
    def __init__(self):
        self.api_key = os.getenv("EXA_API_KEY")
        if not self.api_key:
            raise ValueError("EXA_API_KEY environment variable is required")
        
        self.base_url = "https://api.exa.ai"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def answer_query(self, query: str) -> ExaAnswerResponse:
        """Call the Exa answer API to get information about a query."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/answer",
                    headers=self.headers,
                    json={
                        "query": query,
                        "stream": False,
                        "text": True
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                return ExaAnswerResponse(**data)
                
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Exa API error: {e.response.text}"
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=503,
                    detail=f"Failed to connect to Exa API: {str(e)}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error calling Exa API: {str(e)}"
                )
    
    async def fact_check_claim(self, claim: str) -> FactCheckResponse:
        """
        Fact-check a claim using Exa's answer API.
        """
        # Create a structured fact-checking query that asks for specific format
        fact_check_query = f"""
        Please fact-check this claim and provide your response in this exact format:
        
        TITLE: [A very short title for the claim]
        DESCRIPTION: [A description of the claim like a news sub-headline without fluff]
        SCORE: [A number from 1-5 where 1=Untrue, 2=Mostly Untrue, 3=Mix of Truth, 4=Mostly True, 5=True]
        ANALYSIS: [Your detailed analysis explaining why the claim is true or untrue]
        
        Claim to fact-check: {claim}
        """
        
        try:
            # Get information from Exa
            exa_response = await self.answer_query(fact_check_query)
            
            # Parse the structured response
            parsed_response = self._parse_structured_response(exa_response.answer, claim)
            
            # Create a structured response
            return FactCheckResponse(
                title=parsed_response["title"],
                description=parsed_response["description"],
                truthfulnessScore=parsed_response["score"],
                response=parsed_response["analysis"],
                sources=exa_response.citations,
                exaResponse=exa_response
            )
            
        except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=f"Format validation error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during fact-checking: {str(e)}"
            )
    
    def _parse_structured_response(self, answer: str, original_claim: str) -> dict:
        """
        Parse the structured response from Exa API.
        If format is incorrect, return validation error.
        """
        try:
            # Extract fields using regex patterns
            title_match = re.search(r'TITLE:\s*(.+?)(?:\n|$)', answer, re.IGNORECASE | re.DOTALL)
            description_match = re.search(r'DESCRIPTION:\s*(.+?)(?:\n|SCORE:|$)', answer, re.IGNORECASE | re.DOTALL)
            score_match = re.search(r'SCORE:\s*(\d+)', answer, re.IGNORECASE)
            analysis_match = re.search(r'ANALYSIS:\s*(.+)', answer, re.IGNORECASE | re.DOTALL)
            
            # Validate required fields are present
            if not title_match:
                title = self._extract_fallback_title(original_claim)
            else:
                title = title_match.group(1).strip()
            
            if not description_match:
                description = original_claim
            else:
                description = description_match.group(1).strip()
            
            if not score_match:
                raise ValueError("SCORE field missing or invalid format. Expected SCORE: [1-5]")
            
            score = int(score_match.group(1))
            if score < 1 or score > 5:
                raise ValueError(f"Score must be between 1-5, got: {score}")
            
            if not analysis_match:
                raise ValueError("ANALYSIS field missing")
            
            analysis = analysis_match.group(1).strip()
            
            # Validate field lengths and content
            if len(title.strip()) == 0:
                raise ValueError("TITLE cannot be empty")
            if len(description.strip()) == 0:
                raise ValueError("DESCRIPTION cannot be empty")
            if len(analysis.strip()) == 0:
                raise ValueError("ANALYSIS cannot be empty")
            
            return {
                "title": title,
                "description": description,
                "score": score,
                "analysis": analysis
            }
            
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            raise ValueError(f"Failed to parse response format: {str(e)}")
    
    def _extract_fallback_title(self, claim: str) -> str:
        """Extract a fallback title if parsing fails."""
        title = claim.strip()
        if len(title) > 60:
            title = title[:57] + "..."
        return title
