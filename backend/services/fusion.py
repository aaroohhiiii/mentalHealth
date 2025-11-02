"""
Multi-Modal Fusion Service
Combines text, audio, and image analyses using late fusion
"""

from typing import Dict, List, Optional


# Default fusion weights (configurable)
DEFAULT_WEIGHTS = {
    "text": 0.5,
    "audio": 0.25,
    "image": 0.25
}


def aggregate_daily_scores(
    text_analyses: List[Dict],
    audio_analyses: List[Dict],
    image_analyses: List[Dict],
    weights: Optional[Dict] = None
) -> Dict:
    """
    Perform late fusion of multi-modal analyses
    
    Args:
        text_analyses: List of text analysis results
        audio_analyses: List of audio analysis results
        image_analyses: List of image analysis results
        weights: Optional custom weights for fusion
    
    Returns:
        {
            'final_score': float (0-1),
            'bucket': str ('Low', 'Moderate', 'High'),
            'modality_scores': Dict[str, float],
            'explanation': str,
            'suggestions': List[str]
        }
    """
    
    if weights is None:
        weights = DEFAULT_WEIGHTS.copy()
    
    # Calculate average scores per modality
    text_score = _average_scores(text_analyses) if text_analyses else None
    audio_score = _average_scores(audio_analyses) if audio_analyses else None
    image_score = _average_scores(image_analyses) if image_analyses else None
    
    # Adjust weights based on available modalities
    active_weights = {}
    if text_score is not None:
        active_weights["text"] = weights["text"]
    if audio_score is not None:
        active_weights["audio"] = weights["audio"]
    if image_score is not None:
        active_weights["image"] = weights["image"]
    
    # Normalize weights
    total_weight = sum(active_weights.values())
    if total_weight > 0:
        active_weights = {k: v / total_weight for k, v in active_weights.items()}
    else:
        # No data available
        return _no_data_response()
    
    # Compute weighted fusion
    final_score = 0.0
    if text_score is not None:
        final_score += text_score * active_weights.get("text", 0)
    if audio_score is not None:
        final_score += audio_score * active_weights.get("audio", 0)
    if image_score is not None:
        final_score += image_score * active_weights.get("image", 0)
    
    final_score = round(final_score, 3)
    
    # Categorize final risk
    if final_score < 0.33:
        bucket = "Low"
    elif final_score < 0.66:
        bucket = "Moderate"
    else:
        bucket = "High"
    
    # Generate explanation
    explanation = _generate_explanation(
        text_score, audio_score, image_score, 
        text_analyses, audio_analyses, image_analyses,
        bucket
    )
    
    # Generate personalized suggestions
    suggestions = _generate_suggestions(
        final_score, bucket,
        text_analyses, audio_analyses, image_analyses
    )
    
    return {
        "final_score": final_score,
        "bucket": bucket,
        "modality_scores": {
            "text": round(text_score, 3) if text_score is not None else None,
            "audio": round(audio_score, 3) if audio_score is not None else None,
            "image": round(image_score, 3) if image_score is not None else None
        },
        "explanation": explanation,
        "suggestions": suggestions
    }


def _average_scores(analyses: List[Dict]) -> Optional[float]:
    """Calculate average score from list of analyses"""
    if not analyses:
        return None
    scores = [a.get("score", 0.5) for a in analyses]
    return sum(scores) / len(scores)


def _no_data_response() -> Dict:
    """Return default response when no data is available"""
    return {
        "final_score": 0.5,
        "bucket": "Moderate",
        "modality_scores": {
            "text": None,
            "audio": None,
            "image": None
        },
        "explanation": "No analysis data available for this day.",
        "suggestions": ["Please log your daily text, audio, or image entries."]
    }


def _generate_explanation(
    text_score: Optional[float],
    audio_score: Optional[float],
    image_score: Optional[float],
    text_analyses: List[Dict],
    audio_analyses: List[Dict],
    image_analyses: List[Dict],
    bucket: str
) -> str:
    """Generate human-readable explanation of the assessment"""
    
    parts = []
    
    # Overall assessment
    if bucket == "Low":
        parts.append("Your overall mental health indicators suggest a positive state.")
    elif bucket == "Moderate":
        parts.append("Your indicators show some signs of stress or mood changes.")
    else:
        parts.append("Multiple indicators suggest elevated stress or concerning patterns.")
    
    # Text analysis
    if text_score is not None and text_analyses:
        if text_score > 0.66:
            parts.append("Your text entries contain concerning language patterns.")
        elif text_score > 0.33:
            parts.append("Your text shows mixed emotional indicators.")
        else:
            parts.append("Your text entries reflect generally positive sentiment.")
    
    # Audio analysis
    if audio_score is not None and audio_analyses:
        dominant_emotions = [a["explain"].get("dominant_emotion") for a in audio_analyses]
        if "sad" in dominant_emotions or "angry" in dominant_emotions or "fear" in dominant_emotions:
            parts.append(f"Voice analysis detected emotions like {', '.join(set(dominant_emotions))}.")
        else:
            parts.append("Voice analysis shows neutral or positive emotional tone.")
    
    # Image analysis
    if image_score is not None and image_analyses:
        facial_emotions = []
        for img in image_analyses:
            facial_emotions.extend(img.get("top_emotions", {}).keys())
        if "sad" in facial_emotions or "angry" in facial_emotions:
            parts.append("Facial expressions show some negative emotions.")
        else:
            parts.append("Facial expressions appear relatively neutral or positive.")
    
    return " ".join(parts)


def _generate_suggestions(
    final_score: float,
    bucket: str,
    text_analyses: List[Dict],
    audio_analyses: List[Dict],
    image_analyses: List[Dict]
) -> List[str]:
    """Generate personalized, non-diagnostic suggestions"""
    
    suggestions = []
    
    # Check for specific themes in text
    themes = set()
    if text_analyses:
        for analysis in text_analyses:
            themes.update(analysis.get("explain", {}).get("dominant_themes", []))
    
    # Sleep-related suggestions
    if "sleep_issues" in themes:
        suggestions.append("Consider establishing a regular sleep schedule and bedtime routine.")
        suggestions.append("Try limiting screen time 1 hour before bed.")
    
    # Anxiety-related suggestions
    if "anxiety" in themes or final_score > 0.6:
        suggestions.append("Practice deep breathing exercises (4-7-8 technique).")
        suggestions.append("Consider mindfulness or meditation apps (Headspace, Calm).")
    
    # Low mood suggestions
    if "low_mood" in themes or bucket == "High":
        suggestions.append("Engage in physical activity - even a 10-minute walk can help.")
        suggestions.append("Connect with friends or loved ones.")
    
    # Isolation suggestions
    if "isolation" in themes:
        suggestions.append("Reach out to someone you trust to talk or spend time together.")
        suggestions.append("Join a community group or online forum with shared interests.")
    
    # General wellness suggestions
    if bucket == "Moderate" or bucket == "High":
        suggestions.append("Maintain a balanced diet and stay hydrated.")
        suggestions.append("Journal your thoughts and feelings daily.")
    
    # Crisis resources (for high risk)
    if final_score > 0.75:
        suggestions.append("If you're in crisis, please contact: National Suicide Prevention Lifeline 988 (US)")
        suggestions.append("Consider speaking with a mental health professional.")
    
    # Default positive suggestions
    if bucket == "Low":
        suggestions.append("Keep up the positive habits! Continue monitoring your wellbeing.")
        suggestions.append("Practice gratitude by noting 3 things you're thankful for today.")
    
    # Limit to 5 suggestions
    return suggestions[:5] if suggestions else [
        "Continue monitoring your mental health daily.",
        "Maintain healthy sleep, exercise, and social connection habits."
    ]
