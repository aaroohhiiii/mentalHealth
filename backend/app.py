"""
FastAPI Backend for Mental Health Multi-Modal AI System
Author: Aarohi (B.Tech)
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta, date
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
from models.user import create_user, authenticate_user, get_user, get_user_by_id
from models.session import (
    create_session,
    get_session,
    get_user_sessions,
    update_session_text,
    update_session_audio,
    update_session_image,
    update_session_fusion,
    get_sessions_by_date_range
)
from utils.auth import create_access_token, verify_token
from utils.database import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="Mental Health AI System",
    description="Multi-modal early detection for stress/depression",
    version="1.0.0"
)


# ===== Database Lifecycle Events =====

@app.on_event("startup")
async def startup_db_client():
    """Connect to MongoDB on startup"""
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    """Close MongoDB connection on shutdown"""
    await close_mongo_connection()

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Request/Response Models =====

# Authentication Models
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict


# Analysis Models
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
        "database": "MongoDB Connected",
        "endpoints": {
            "authentication": [
                "/auth/signup",
                "/auth/login",
                "/auth/me"
            ],
            "session_based_analysis": [
                "/sessions/analyze/text",
                "/sessions/analyze/audio",
                "/sessions/analyze/image",
                "/sessions/aggregate",
                "/sessions/my-sessions",
                "/sessions/{date}",
                "/sessions/range/{start}/{end}"
            ],
            "legacy_analysis": [
                "/analyze/text",
                "/analyze/audio",
                "/analyze/image",
                "/aggregate/day",
                "/trend/7d"
            ]
        }
    }


# ===== Authentication Endpoints =====

@app.post("/auth/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """Register a new user"""
    # Validate input
    if len(request.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    
    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    if "@" not in request.email:
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    # Create user
    user = await create_user(request.username, request.email, request.password)
    
    if not user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Generate token
    access_token = create_access_token(data={"sub": user.username, "user_id": str(user._id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }


@app.post("/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login with username and password"""
    user = await authenticate_user(request.username, request.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Generate token
    access_token = create_access_token(data={"sub": user.username, "user_id": str(user._id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }


@app.get("/auth/me")
async def get_current_user_endpoint(authorization: Optional[str] = Header(None)):
    """Get current user from token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Extract token from "Bearer <token>"
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        username = payload.get("sub")
        user = await get_user(username)
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user.to_dict()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


# ===== Helper Function for Authentication =====

async def get_current_user(authorization: Optional[str] = Header(None)):
    """Dependency to extract current user from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = payload.get("user_id")
        username = payload.get("sub")
        
        if not user_id or not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        user = await get_user(username)
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


# ===== Session Management Endpoints =====

@app.post("/sessions/analyze/text")
async def session_analyze_text(
    request: TextAnalysisRequest,
    session_date: str,
    user = Depends(get_current_user)
):
    """
    Analyze text with LLM enhancement and store in user's daily session
    session_date format: YYYY-MM-DD
    """
    try:
        # Step 1: Perform base text analysis
        result = analyze_text(request.text)
        
        # Step 2: Enhance with LLM feedback
        enhanced_result = enhance_text_analysis(request.text, result)
        
        # Get or create session for today
        session = await get_session(str(user._id), session_date)
        if not session:
            session = await create_session(str(user._id), user.username, session_date)
        
        # Update session with enhanced analysis
        analysis_data = {
            "text": request.text,
            "score": result["score"],
            "bucket": result["bucket"],
            "explain": result["explain"],
            "enhanced": enhanced_result.get("enhanced", False),
            "llm_feedback": enhanced_result.get("llm_feedback", {}),
            "timestamp": datetime.now().isoformat()
        }
        
        updated_session = await update_session_text(str(user._id), session_date, analysis_data)
        
        return {
            "status": "success",
            "score": result["score"],
            "bucket": result["bucket"],
            "explain": result["explain"],
            "llm_feedback": enhanced_result.get("llm_feedback", {}),
            "enhanced": enhanced_result.get("enhanced", False),
            "session_id": str(updated_session._id),
            "date": session_date
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")


@app.post("/sessions/analyze/audio")
async def session_analyze_audio(
    file: UploadFile = File(...),
    session_date: str = None,
    user = Depends(get_current_user)
):
    """
    Analyze audio with LLM enhancement and store in user's daily session
    """
    try:
        if not session_date:
            session_date = date.today().isoformat()
        
        # Validate file
        if not file.filename.endswith(('.wav', '.mp3', '.ogg', '.flac', '.webm')):
            raise HTTPException(status_code=400, detail="Invalid audio format")
        
        audio_bytes = await file.read()
        
        # Step 1: Perform base audio analysis
        result = analyze_audio(audio_bytes, file.filename)
        
        # Step 2: Enhance with LLM feedback
        enhanced_result = enhance_audio_analysis(result)
        
        # Get or create session
        session = await get_session(str(user._id), session_date)
        if not session:
            session = await create_session(str(user._id), user.username, session_date)
        
        # Update session with enhanced audio analysis
        analysis_data = {
            "filename": file.filename,
            "score": result["score"],
            "bucket": result["bucket"],
            "explain": result["explain"],
            "enhanced": enhanced_result.get("enhanced", False),
            "llm_feedback": enhanced_result.get("llm_feedback", {}),
            "timestamp": datetime.now().isoformat()
        }
        
        updated_session = await update_session_audio(str(user._id), session_date, analysis_data)
        
        return {
            "status": "success",
            "score": result["score"],
            "bucket": result["bucket"],
            "explain": result["explain"],
            "llm_feedback": enhanced_result.get("llm_feedback", {}),
            "enhanced": enhanced_result.get("enhanced", False),
            "session_id": str(updated_session._id),
            "date": session_date
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio analysis failed: {str(e)}")


@app.post("/sessions/analyze/image")
async def session_analyze_image(
    file: UploadFile = File(...),
    session_date: str = None,
    user = Depends(get_current_user)
):
    """
    Analyze image with LLM enhancement and store in user's daily session
    """
    try:
        if not session_date:
            session_date = date.today().isoformat()
        
        # Validate file
        if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        image_bytes = await file.read()
        
        # Step 1: Perform base image analysis
        result = analyze_image(image_bytes, file.filename)
        
        # Step 2: Enhance with LLM feedback
        enhanced_result = enhance_image_analysis(result)
        
        # Get or create session
        session = await get_session(str(user._id), session_date)
        if not session:
            session = await create_session(str(user._id), user.username, session_date)
        
        # Update session with enhanced image analysis
        analysis_data = {
            "filename": file.filename,
            "score": result["score"],
            "bucket": result["bucket"],
            "top_emotions": result.get("top_emotions", {}),
            "explain": result["explain"],
            "enhanced": enhanced_result.get("enhanced", False),
            "llm_feedback": enhanced_result.get("llm_feedback", {}),
            "timestamp": datetime.now().isoformat()
        }
        
        updated_session = await update_session_image(str(user._id), session_date, analysis_data)
        
        return {
            "status": "success",
            "score": result["score"],
            "bucket": result["bucket"],
            "top_emotions": result.get("top_emotions", {}),
            "explain": result["explain"],
            "llm_feedback": enhanced_result.get("llm_feedback", {}),
            "enhanced": enhanced_result.get("enhanced", False),
            "session_id": str(updated_session._id),
            "date": session_date
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")


@app.post("/sessions/aggregate")
async def session_aggregate(
    session_date: str,
    user = Depends(get_current_user)
):
    """
    Aggregate all modality scores for a specific date
    Combines text, audio, and image analysis into final risk score
    """
    try:
        # Get session for the date
        session = await get_session(str(user._id), session_date)
        
        if not session:
            raise HTTPException(status_code=404, detail="No session found for this date")
        
        # Extract scores from each modality
        text_score = session.text_analysis.get("score") if session.text_analysis else None
        audio_score = session.audio_analysis.get("score") if session.audio_analysis else None
        image_score = session.image_analysis.get("score") if session.image_analysis else None
        
        # Aggregate scores
        modality_scores = {}
        if text_score is not None:
            modality_scores["text"] = text_score
        if audio_score is not None:
            modality_scores["audio"] = audio_score
        if image_score is not None:
            modality_scores["image"] = image_score
        
        if not modality_scores:
            raise HTTPException(status_code=400, detail="No analysis data available for aggregation")
        
        # Calculate final score (weighted average)
        weights = {"text": 0.4, "audio": 0.3, "image": 0.3}
        final_score = sum(modality_scores[m] * weights.get(m, 1.0) for m in modality_scores) / len(modality_scores)
        final_bucket = categorize_risk(final_score)
        
        # Generate explanation and suggestions
        explanation = f"Combined analysis from {len(modality_scores)} modalities"
        suggestions = []
        
        if final_score >= 0.66:
            suggestions = ["Consider reaching out to a mental health professional", "Practice stress-reduction techniques", "Maintain social connections"]
        elif final_score >= 0.33:
            suggestions = ["Monitor your well-being regularly", "Ensure adequate sleep and exercise", "Practice mindfulness"]
        else:
            suggestions = ["Continue healthy habits", "Stay socially connected", "Maintain work-life balance"]
        
        # Store fusion result
        fusion_data = {
            "final_score": final_score,
            "bucket": final_bucket,
            "modality_scores": modality_scores,
            "explanation": explanation,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }
        
        updated_session = await update_session_fusion(str(user._id), session_date, fusion_data)
        
        return {
            "status": "success",
            "date": session_date,
            "final_score": final_score,
            "bucket": final_bucket,
            "modality_scores": modality_scores,
            "explanation": explanation,
            "suggestions": suggestions
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Aggregation failed: {str(e)}")


@app.post("/sessions/chat")
async def session_chat(
    request: dict,
    user = Depends(get_current_user)
):
    """
    Chat endpoint for conversational support based on session analysis
    Takes session context and user message, returns AI response
    """
    try:
        import os
        from groq import Groq
        
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise HTTPException(status_code=503, detail="Chat service unavailable")
        
        groq_client = Groq(api_key=groq_api_key)
        
        session_date = request.get("session_date")
        user_message = request.get("message")
        chat_history = request.get("chat_history", [])
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Get session for context
        session = await get_session(str(user._id), session_date) if session_date else None
        
        # Build context from session analysis
        context_parts = []
        
        if session:
            if session.text_analysis and session.text_analysis.get("llm_feedback"):
                feedback = session.text_analysis["llm_feedback"]
                context_parts.append(f"Text Analysis: Risk level - {feedback.get('risk_level', 'N/A')}, Key concerns - {', '.join(feedback.get('key_concerns', []))}")
            
            if session.audio_analysis and session.audio_analysis.get("llm_feedback"):
                feedback = session.audio_analysis["llm_feedback"]
                context_parts.append(f"Voice Analysis: Concern level - {feedback.get('concern_level', 'N/A')}, Observations - {', '.join(feedback.get('key_observations', []))}")
            
            if session.image_analysis and session.image_analysis.get("llm_feedback"):
                feedback = session.image_analysis["llm_feedback"]
                context_parts.append(f"Image Analysis: Concern level - {feedback.get('concern_level', 'N/A')}, Observations - {', '.join(feedback.get('key_observations', []))}")
        
        context_summary = " | ".join(context_parts) if context_parts else "No analysis data available yet."
        
        # Build chat messages
        messages = [
            {
                "role": "system",
                "content": f"""You are a warm, empathetic friend helping someone understand their mental health check-in.

Context: {context_summary}

Talk like a caring friend would:
- Use simple, natural language
- Keep responses SHORT (2-4 sentences max)
- Be warm but genuine - no fake cheerfulness
- Acknowledge their feelings first
- Give ONE practical tip at a time
- If they need help, gently suggest talking to someone
- NO emojis, NO clinical jargon, NO long paragraphs

Remember: You're here to support, not replace a therapist. Be real, be brief, be kind."""
            }
        ]
        
        # Add chat history
        for msg in chat_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from Groq
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.8,  # More natural/human-like
            max_tokens=200    # Shorter responses (about 2-4 sentences)
        )
        
        assistant_message = response.choices[0].message.content.strip()
        
        return {
            "status": "success",
            "message": assistant_message,
            "context_available": len(context_parts) > 0
        }
    
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.post("/sessions/chat/history")
async def historical_chat(
    request: dict,
    user = Depends(get_current_user)
):
    """
    Historical chat endpoint with full mental health timeline analysis
    Analyzes trends, patterns, and warning signs across all user sessions
    """
    try:
        import os
        from groq import Groq
        from datetime import datetime, timedelta
        
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise HTTPException(status_code=503, detail="Chat service unavailable")
        
        groq_client = Groq(api_key=groq_api_key)
        
        user_message = request.get("message")
        chat_history = request.get("chat_history", [])
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Fetch last 30 sessions from MongoDB
        sessions = await get_user_sessions(str(user._id), limit=30)
        
        # Build comprehensive historical context
        if not sessions:
            context_summary = "No mental health check-in history available yet. User should complete some assessments first."
        else:
            # Analyze trends
            risk_levels = []
            concerns = []
            dates = []
            
            for session in sessions:
                dates.append(session.date)
                
                # Extract risk levels
                if session.text_analysis and session.text_analysis.get("llm_feedback"):
                    fb = session.text_analysis["llm_feedback"]
                    risk_levels.append(fb.get("risk_level", ""))
                    concerns.extend(fb.get("key_concerns", []))
                
                if session.audio_analysis and session.audio_analysis.get("llm_feedback"):
                    fb = session.audio_analysis["llm_feedback"]
                    risk_levels.append(fb.get("concern_level", ""))
                    concerns.extend(fb.get("key_observations", []))
                
                if session.image_analysis and session.image_analysis.get("llm_feedback"):
                    fb = session.image_analysis["llm_feedback"]
                    risk_levels.append(fb.get("concern_level", ""))
                    concerns.extend(fb.get("key_observations", []))
            
            # Count risk levels
            high_risk_count = sum(1 for r in risk_levels if r and "high" in r.lower())
            moderate_risk_count = sum(1 for r in risk_levels if r and "moderate" in r.lower())
            low_risk_count = sum(1 for r in risk_levels if r and "low" in r.lower())
            
            # Identify recurring concerns
            from collections import Counter
            concern_counts = Counter(concerns)
            top_concerns = [c for c, count in concern_counts.most_common(5)]
            
            # Calculate trend
            recent_risks = risk_levels[:5]  # Last 5
            older_risks = risk_levels[5:10] if len(risk_levels) > 5 else []
            
            recent_high = sum(1 for r in recent_risks if r and "high" in r.lower())
            older_high = sum(1 for r in older_risks if r and "high" in r.lower())
            
            if recent_high > older_high:
                trend = "WORSENING - Recent risk levels are HIGHER than before"
            elif recent_high < older_high:
                trend = "IMPROVING - Recent risk levels are LOWER than before"
            else:
                trend = "STABLE - Consistent risk levels over time"
            
            context_summary = f"""
Mental Health History Summary ({len(sessions)} sessions, last {len(dates)} days):

TREND: {trend}

RISK DISTRIBUTION:
- High risk: {high_risk_count} times
- Moderate risk: {moderate_risk_count} times  
- Low risk: {low_risk_count} times

RECURRING CONCERNS:
{', '.join(top_concerns[:5]) if top_concerns else 'None identified'}

LATEST SESSION: {dates[0] if dates else 'N/A'}
OLDEST SESSION: {dates[-1] if dates else 'N/A'}
"""
        
        # Build chat messages with historical context
        messages = [
            {
                "role": "system",
                "content": f"""You are a caring mental health companion who's been tracking someone's wellbeing over time.

{context_summary}

Your role:
- Spot patterns and trends in their mental health
- Notice if things are getting better or worse
- Identify recurring struggles
- Gently point out concerning patterns
- Celebrate improvements
- Suggest when professional help might be needed
- Be honest but kind about what you're seeing

Talk like a friend who genuinely cares:
- Keep it SHORT (2-4 sentences)
- Be real and direct when needed
- Acknowledge both struggles AND progress
- If you see warning signs, say so gently
- NO emojis, NO sugarcoating, but stay warm

You have the full picture. Use it wisely."""
            }
        ]
        
        # Add chat history
        for msg in chat_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from Groq
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.75,
            max_tokens=250
        )
        
        assistant_message = response.choices[0].message.content.strip()
        
        return {
            "status": "success",
            "message": assistant_message,
            "sessions_analyzed": len(sessions),
            "has_history": len(sessions) > 0
        }
    
    except Exception as e:
        print(f"Historical chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.get("/sessions/my-sessions")
async def get_my_sessions(
    limit: int = 30,
    user = Depends(get_current_user)
):
    """Get all sessions for the current user (last 30 days by default)"""
    try:
        sessions = await get_user_sessions(str(user._id), limit=limit)
        
        return {
            "username": user.username,
            "total_sessions": len(sessions),
            "sessions": [s.to_dict(include_id=True) for s in sessions]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve sessions: {str(e)}")


@app.get("/sessions/{session_date}")
async def get_session_by_date(
    session_date: str,
    user = Depends(get_current_user)
):
    """Get a specific session by date"""
    try:
        session = await get_session(str(user._id), session_date)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found for this date")
        
        return session.to_dict(include_id=True)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve session: {str(e)}")


@app.get("/sessions/range/{start_date}/{end_date}")
async def get_sessions_range(
    start_date: str,
    end_date: str,
    user = Depends(get_current_user)
):
    """Get sessions within a date range (YYYY-MM-DD format)"""
    try:
        sessions = await get_sessions_by_date_range(str(user._id), start_date, end_date)
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_sessions": len(sessions),
            "sessions": [s.to_dict(include_id=True) for s in sessions]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve sessions: {str(e)}")


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
