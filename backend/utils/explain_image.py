"""
Image Explainability Utilities
Provides explanations for facial expression recognition
"""

from typing import Dict, List


def explain_facial_emotion(emotion: str, confidence: float) -> str:
    """
    Provide human-readable explanation of detected facial emotion
    
    Args:
        emotion: Detected emotion
        confidence: Confidence score (0-1)
    
    Returns:
        Explanation string
    """
    
    explanations = {
        "happy": "Facial features show positive expression (smile, raised cheeks).",
        "sad": "Facial features indicate low mood (downturned mouth, lowered eyebrows).",
        "angry": "Expression shows tension (furrowed brow, tightened jaw).",
        "fear": "Facial features suggest anxiety (wide eyes, raised eyebrows).",
        "surprise": "Expression shows surprise or alertness (wide eyes, open mouth).",
        "disgust": "Facial features indicate negative reaction (wrinkled nose, raised upper lip).",
        "neutral": "Facial expression appears relaxed and neutral."
    }
    
    base_explanation = explanations.get(emotion, "Facial expression analyzed.")
    
    if confidence > 0.7:
        return f"{base_explanation} High confidence detection."
    elif confidence > 0.4:
        return f"{base_explanation} Moderate confidence detection."
    else:
        return f"{base_explanation} Low confidence - results may be less reliable."


def highlight_facial_regions(image, emotion: str) -> str:
    """
    Highlight facial regions that contributed to emotion detection
    
    Args:
        image: Input image
        emotion: Detected emotion
    
    Returns:
        Base64-encoded image with highlighted regions
    """
    pass


def generate_emotion_heatmap(face_landmarks, emotion_scores) -> str:
    """
    Generate heatmap showing which facial regions contributed most
    
    TODO: Implement with Grad-CAM or similar technique
    """
    pass
