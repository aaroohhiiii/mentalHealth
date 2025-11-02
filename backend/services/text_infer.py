"""
Text Analysis Service
Uses NLP to detect stress/depression indicators in text
Currently using placeholder logic - will be replaced with DistilBERT/RoBERTa
"""

import re
from typing import Dict, List


# Stress/depression indicator keywords (simple baseline)
NEGATIVE_KEYWORDS = [
    'sad', 'depressed', 'anxious', 'worried', 'stressed', 'tired', 'exhausted',
    'hopeless', 'alone', 'lonely', 'overwhelmed', 'frustrated', 'angry',
    'worthless', 'empty', 'numb', 'pain', 'hurt', 'cry', 'crying', 'death',
    'die', 'suicide', 'hate', 'terrible', 'awful', 'horrible', 'miserable',
    'helpless', 'scared', 'fear', 'panic', 'nightmare', 'insomnia', 'can\'t sleep'
]

POSITIVE_KEYWORDS = [
    'happy', 'good', 'great', 'excellent', 'wonderful', 'joy', 'excited',
    'grateful', 'thankful', 'blessed', 'love', 'amazing', 'fantastic',
    'peaceful', 'calm', 'relaxed', 'energetic', 'motivated', 'productive',
    'confident', 'hopeful', 'optimistic', 'better', 'improved', 'progress'
]


def analyze_text(text: str) -> Dict:
    """
    Analyze text for stress/depression indicators
    
    Args:
        text: Input text (daily log)
    
    Returns:
        {
            'score': float (0-1, higher = more concerning),
            'bucket': str ('Low', 'Moderate', 'High'),
            'explain': {
                'tokens': List of highlighted words with scores,
                'sentiment': str,
                'dominant_themes': List[str]
            }
        }
    """
    
    # Normalize text
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    # Count keyword matches
    negative_matches = []
    positive_matches = []
    
    for word in words:
        if word in NEGATIVE_KEYWORDS:
            negative_matches.append(word)
        elif word in POSITIVE_KEYWORDS:
            positive_matches.append(word)
    
    # Calculate simple score
    neg_count = len(negative_matches)
    pos_count = len(positive_matches)
    total_words = max(len(words), 1)
    
    # Score calculation (0-1 range)
    if neg_count == 0 and pos_count == 0:
        base_score = 0.35  # Neutral default
    else:
        # Higher negative ratio = higher score (more concerning)
        base_score = min(1.0, (neg_count * 0.15) / max(total_words * 0.1, 1))
        # Reduce score for positive indicators
        base_score = max(0.0, base_score - (pos_count * 0.05) / max(total_words * 0.1, 1))
    
    # Add variance based on text length
    if len(words) < 10:
        base_score *= 0.8  # Reduce confidence for short texts
    
    score = min(1.0, max(0.0, base_score + 0.2))  # Add baseline concern
    
    # Categorize
    if score < 0.33:
        bucket = "Low"
        sentiment = "Positive/Neutral"
    elif score < 0.66:
        bucket = "Moderate"
        sentiment = "Mixed/Concerning"
    else:
        bucket = "High"
        sentiment = "Negative/High Concern"
    
    # Prepare explanation with token highlights
    highlighted_tokens = []
    for word in set(negative_matches):
        highlighted_tokens.append({
            "word": word,
            "type": "negative",
            "importance": 0.8
        })
    for word in set(positive_matches):
        highlighted_tokens.append({
            "word": word,
            "type": "positive",
            "importance": 0.6
        })
    
    # Identify themes
    themes = []
    if any(w in text_lower for w in ['sleep', 'insomnia', 'tired', 'exhausted']):
        themes.append("sleep_issues")
    if any(w in text_lower for w in ['anxious', 'worried', 'panic', 'scared']):
        themes.append("anxiety")
    if any(w in text_lower for w in ['sad', 'depressed', 'hopeless', 'empty']):
        themes.append("low_mood")
    if any(w in text_lower for w in ['alone', 'lonely', 'isolated']):
        themes.append("isolation")
    
    return {
        "score": round(score, 3),
        "bucket": bucket,
        "explain": {
            "tokens": highlighted_tokens[:10],  # Top 10 for display
            "sentiment": sentiment,
            "dominant_themes": themes,
            "negative_indicators": len(negative_matches),
            "positive_indicators": len(positive_matches),
            "text_length": len(words)
        }
    }


# ===== Future: Real Model Implementation =====
"""
def analyze_text_transformer(text: str) -> Dict:
    # TODO: Replace with actual transformer model
    # from transformers import pipeline
    # sentiment_analyzer = pipeline("sentiment-analysis", 
    #                               model="distilbert-base-uncased-finetuned-sst-2-english")
    # 
    # result = sentiment_analyzer(text)[0]
    # score = result['score'] if result['label'] == 'NEGATIVE' else 1 - result['score']
    # 
    # Use SHAP or attention weights for token-level explanations
    pass
"""
