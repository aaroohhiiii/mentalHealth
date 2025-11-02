"""
FastAPI Backend for Mental Health Multi-Modal AI System
Author: Aarohi (B.Tech)
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import json
import os

from services.text_infer import analyze_text
from services.audio_infer import analyze_audio
from services.image_infer import analyze_image
from services.fusion import aggregate_daily_scores
from services.storage import (
    store_analysis,
    get_trend_data,
    purge_all_data,
    get_daily_entries
)
from services.llm_enhance import (
    enhance_text_analysis,
    enhance_audio_analysis,
    enhance_image_analysis,
    enhance_daily_fusion
)

app = FastAPI(
    title="Mental Health AI System",
    description="Multi-modal early detection for stress/depression",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Request/Response Models =====

class TextAnalysisRequest(BaseModel):
    text: str
    timestamp: Optional[str] = None


class TextAnalysisResponse(BaseModel):
    score: float
    bucket: str
    explain: Dict
    timestamp: str


class AudioAnalysisResponse(BaseModel):
    score: float
    bucket: str
    explain: Dict
    timestamp: str


class ImageAnalysisResponse(BaseModel):
    score: float
    bucket: str
    top_emotions: Dict[str, float]
    explain: Dict
    timestamp: str


class DailyAggregateRequest(BaseModel):
    date: str  # YYYY-MM-DD
    text_ids: Optional[List[str]] = []
    audio_ids: Optional[List[str]] = []
    image_ids: Optional[List[str]] = []


class DailyAggregateResponse(BaseModel):
    date: str
    final_score: float
    bucket: str
    modality_scores: Dict[str, float]
    explanation: str
    suggestions: List[str]


class TrendResponse(BaseModel):
    dates: List[str]
    scores: List[Optional[float]]
    buckets: List[str]


# ===== Utility Functions =====

def categorize_risk(score: float) -> str:
    """Convert score (0-1) to risk bucket"""
    if score < 0.33:
        return "Low"
    elif score < 0.66:
        return "Moderate"
    else:
        return "High"


# ===== Endpoints =====

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Mental Health AI System",
        "version": "1.0.0",
        "endpoints": [
            "/analyze/text",
            "/analyze/audio",
            "/analyze/image",
            "/aggregate/day",
            "/trend/7d",
            "/purge"
        ]
    }


@app.post("/analyze/text", response_model=TextAnalysisResponse)
async def analyze_text_endpoint(request: TextAnalysisRequest):
    """
    Analyze text input for stress/depression indicators
    Returns sentiment score, risk bucket, and token-level explanations
    """
    try:
        timestamp = request.timestamp or datetime.now().isoformat()
        
        # Perform text analysis
        result = analyze_text(request.text)
        
        # Store the analysis
        analysis_id = store_analysis("text", {
            "text": request.text,
            "score": result["score"],
            "bucket": result["bucket"],
            "explain": result["explain"],
            "timestamp": timestamp
        })
        
        return TextAnalysisResponse(
            score=result["score"],
            bucket=result["bucket"],
            explain=result["explain"],
            timestamp=timestamp
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")


@app.post("/analyze/audio", response_model=AudioAnalysisResponse)
async def analyze_audio_endpoint(file: UploadFile = File(...)):
    """
    Analyze audio file for vocal emotion/stress indicators
    Accepts WAV/MP3/WEBM files (5-10 seconds)
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.wav', '.mp3', '.ogg', '.flac', '.webm')):
            raise HTTPException(status_code=400, detail="Invalid audio format. Use WAV/MP3/OGG/FLAC/WEBM")
        
        # Read audio file
        audio_bytes = await file.read()
        
        # Validate file size
        if len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        if len(audio_bytes) < 1000:  # Less than 1KB is suspicious
            raise HTTPException(status_code=400, detail=f"Audio file too small: {len(audio_bytes)} bytes")
        
        print(f"Received audio file: {file.filename}, {len(audio_bytes)} bytes")
        
        # Perform audio analysis
        result = analyze_audio(audio_bytes, file.filename)
        
        timestamp = datetime.now().isoformat()
        
        # Store the analysis (without raw audio for privacy)
        analysis_id = store_analysis("audio", {
            "filename": file.filename,
            "score": result["score"],
            "bucket": result["bucket"],
            "explain": result["explain"],
            "timestamp": timestamp
        })
        
        return AudioAnalysisResponse(
            score=result["score"],
            bucket=result["bucket"],
            explain=result["explain"],
            timestamp=timestamp
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio analysis failed: {str(e)}")


@app.post("/analyze/image", response_model=ImageAnalysisResponse)
async def analyze_image_endpoint(file: UploadFile = File(...)):
    """
    Analyze facial expression in image for emotional state
    Accepts JPG/PNG images
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Invalid image format. Use JPG/PNG")
        
        # Read image file
        image_bytes = await file.read()
        
        # Perform image analysis
        result = analyze_image(image_bytes, file.filename)
        
        timestamp = datetime.now().isoformat()
        
        # Store the analysis (without raw image for privacy)
        analysis_id = store_analysis("image", {
            "filename": file.filename,
            "score": result["score"],
            "bucket": result["bucket"],
            "top_emotions": result["top_emotions"],
            "explain": result["explain"],
            "timestamp": timestamp
        })
        
        return ImageAnalysisResponse(
            score=result["score"],
            bucket=result["bucket"],
            top_emotions=result["top_emotions"],
            explain=result["explain"],
            timestamp=timestamp
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")


@app.post("/aggregate/day", response_model=DailyAggregateResponse)
async def aggregate_day_endpoint(request: DailyAggregateRequest):
    """
    Aggregate all modalities for a given day using late fusion
    Returns final risk score, bucket, and personalized suggestions
    """
    try:
        # Get all entries for the specified date
        daily_data = get_daily_entries(request.date)
        
        # Perform fusion
        result = aggregate_daily_scores(
            daily_data["text"],
            daily_data["audio"],
            daily_data["image"]
        )
        
        # Store daily aggregate
        store_analysis("daily_aggregate", {
            "date": request.date,
            "final_score": result["final_score"],
            "bucket": result["bucket"],
            "modality_scores": result["modality_scores"],
            "explanation": result["explanation"],
            "suggestions": result["suggestions"]
        })
        
        return DailyAggregateResponse(
            date=request.date,
            final_score=result["final_score"],
            bucket=result["bucket"],
            modality_scores=result["modality_scores"],
            explanation=result["explanation"],
            suggestions=result["suggestions"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Daily aggregation failed: {str(e)}")


@app.get("/trend/7d", response_model=TrendResponse)
async def get_trend_endpoint():
    """
    Get 7-day rolling trend of daily risk scores
    Returns dates, scores, and risk buckets
    """
    try:
        trend_data = get_trend_data(days=7)
        
        return TrendResponse(
            dates=trend_data["dates"],
            scores=trend_data["scores"],
            buckets=trend_data["buckets"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend retrieval failed: {str(e)}")


@app.delete("/purge")
async def purge_data_endpoint():
    """
    Delete all stored analysis data (privacy feature)
    Returns count of deleted entries
    """
    try:
        deleted_count = purge_all_data()
        
        return {
            "status": "success",
            "message": f"Deleted {deleted_count} entries",
            "deleted_count": deleted_count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data purge failed: {str(e)}")


@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        from services.storage import get_stats
        stats = get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")


# ===== LLM-Enhanced Endpoints (Hybrid Approach) =====

@app.post("/analyze/text/enhanced")
async def analyze_text_enhanced_endpoint(request: TextAnalysisRequest):
    """
    Enhanced text analysis with LLM reasoning (Llama 3.1 8B via Groq)
    Returns both model analysis AND intelligent interpretation
    """
    try:
        timestamp = request.timestamp or datetime.now().isoformat()
        
        # Step 1: Get pre-trained model analysis
        model_result = analyze_text(request.text)
        
        # Step 2: Enhance with LLM
        enhanced_result = enhance_text_analysis(request.text, model_result)
        
        # Store both
        analysis_id = store_analysis("text", {
            "text": request.text,
            "model_result": model_result,
            "enhanced_result": enhanced_result,
            "timestamp": timestamp
        })
        
        return {
            **enhanced_result,
            "timestamp": timestamp,
            "analysis_id": analysis_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced text analysis failed: {str(e)}")


@app.post("/analyze/audio/enhanced")
async def analyze_audio_enhanced_endpoint(file: UploadFile = File(...)):
    """
    Enhanced audio analysis with LLM reasoning
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.wav', '.mp3', '.ogg', '.flac', '.webm')):
            raise HTTPException(status_code=400, detail="Invalid audio format. Use WAV/MP3/OGG/FLAC/WEBM")
        
        # Step 1: Get pre-trained model analysis
        audio_bytes = await file.read()
        model_result = analyze_audio(audio_bytes, file.filename)
        
        # Step 2: Enhance with LLM
        enhanced_result = enhance_audio_analysis(model_result)
        
        timestamp = datetime.now().isoformat()
        
        # Store
        analysis_id = store_analysis("audio", {
            "filename": file.filename,
            "model_result": model_result,
            "enhanced_result": enhanced_result,
            "timestamp": timestamp
        })
        
        return {
            **enhanced_result,
            "timestamp": timestamp,
            "analysis_id": analysis_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced audio analysis failed: {str(e)}")


@app.post("/analyze/image/enhanced")
async def analyze_image_enhanced_endpoint(file: UploadFile = File(...)):
    """
    Enhanced image analysis with LLM reasoning
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Step 1: Get pre-trained model analysis
        image_bytes = await file.read()
        model_result = analyze_image(image_bytes, file.filename)
        
        # Step 2: Enhance with LLM
        enhanced_result = enhance_image_analysis(model_result)
        
        timestamp = datetime.now().isoformat()
        
        # Store
        analysis_id = store_analysis("image", {
            "filename": file.filename,
            "model_result": model_result,
            "enhanced_result": enhanced_result,
            "timestamp": timestamp
        })
        
        return {
            **enhanced_result,
            "timestamp": timestamp,
            "analysis_id": analysis_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced image analysis failed: {str(e)}")


@app.post("/aggregate/day/enhanced")
async def aggregate_day_enhanced_endpoint(request: DailyAggregateRequest):
    """
    Enhanced daily aggregation with comprehensive LLM assessment
    """
    try:
        # Get all entries for the day
        daily_data = get_daily_entries(request.date)
        
        # Perform fusion
        fusion_result = aggregate_daily_scores(
            daily_data["text"],
            daily_data["audio"],
            daily_data["image"]
        )
        
        # Enhance with LLM
        enhanced_result = enhance_daily_fusion(fusion_result, daily_data)
        
        # Store
        store_analysis("daily_aggregate_enhanced", {
            "date": request.date,
            "fusion_result": fusion_result,
            "enhanced_result": enhanced_result
        })
        
        return enhanced_result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced daily aggregation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
