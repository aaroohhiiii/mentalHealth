"""
Audio Explainability Utilities
Provides frame-level salience and feature importance for audio
"""

from typing import List, Dict


def identify_salient_frames(audio_features, emotion_probs) -> List[int]:
    """
    Identify audio frames with high emotional salience
    
    Args:
        audio_features: Extracted audio features (MFCC, etc.)
        emotion_probs: Emotion probabilities over time
    
    Returns:
        List of frame indices with high salience
    """
    pass


def visualize_audio_features(features: Dict) -> str:
    """
    Generate visualization of audio features
    
    Args:
        features: Dictionary of audio features
    
    Returns:
        Base64-encoded image or chart URL
    """
    pass


def explain_vocal_indicators(emotion: str, features: Dict) -> str:
    """
    Provide human-readable explanation of vocal indicators
    
    Args:
        emotion: Detected emotion
        features: Vocal features
    
    Returns:
        Explanation string
    """
    
    explanations = {
        "sad": "Lower pitch and reduced energy often indicate sadness or low mood.",
        "angry": "Higher pitch variance and increased energy suggest anger or frustration.",
        "fear": "Elevated pitch and rapid speech rate may indicate anxiety or fear.",
        "happy": "Moderate pitch with stable energy reflects positive emotional state.",
        "neutral": "Balanced vocal features suggest neutral emotional state."
    }
    
    return explanations.get(emotion, "Vocal patterns analyzed for emotional content.")
