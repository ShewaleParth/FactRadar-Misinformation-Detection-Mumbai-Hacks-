from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict
from datetime import datetime

class Evidence(BaseModel):
    """Evidence source supporting the claim analysis"""
    title: str
    url: str
    snippet: str = ""
    credibility: Optional[str] = None  # high, medium, low
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "CDC Vaccine Safety Study",
                "url": "https://cdc.gov/vaccines/safety",
                "snippet": "Comprehensive research shows...",
                "credibility": "high"
            }
        }

class AIVerdict(BaseModel):
    """Verdict from a single AI model"""
    model_name: str
    verdict: Literal["TRUE", "FALSE", "MISLEADING", "UNVERIFIED"]
    confidence: float
    reasoning: str

class ClaimAnalysis(BaseModel):
    """Complete analysis of a single claim"""
    claim: str = Field(..., description="The claim being verified")
    final_verdict: Literal["TRUE", "FALSE", "MISLEADING", "UNVERIFIED"] = Field(
        ..., 
        description="Consensus verdict"
    )
    confidence: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Confidence score 0.0-1.0"
    )
    explanation: str = Field(..., description="Clear explanation of the verdict")
    ai_verdicts: List[AIVerdict] = Field(
        default_factory=list,
        description="Individual verdicts from different AI models"
    )
    sources: List[Evidence] = Field(
        default_factory=list,
        description="Credible sources with links"
    )
    analyzed_at: datetime = Field(
        default_factory=datetime.now,
        description="When this analysis was performed"
    )
    cached: bool = Field(
        default=False,
        description="Whether this result came from cache"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "claim": "Vaccines cause autism",
                "final_verdict": "FALSE",
                "confidence": 0.98,
                "explanation": "This claim has been thoroughly debunked by extensive research...",
                "ai_verdicts": [
                    {"model_name": "Gemini", "verdict": "FALSE", "confidence": 0.99, "reasoning": "..."},
                    {"model_name": "GPT-4", "verdict": "FALSE", "confidence": 0.97, "reasoning": "..."}
                ],
                "sources": [],
                "analyzed_at": "2025-12-09T09:38:00",
                "cached": False
            }
        }

class AnalysisRequest(BaseModel):
    """Request to verify a claim"""
    claim: str = Field(..., min_length=3, max_length=500, description="Claim or headline to verify")
    url: Optional[str] = Field(None, description="Optional URL to article")

class AnalysisResponse(BaseModel):
    """Response containing claim analysis"""
    analysis: ClaimAnalysis
    processing_time: float
    cached: bool = False
