"""
Text Explainability Utilities
Provides token-level explanations using attention weights or SHAP
"""

from typing import Dict, List


def highlight_tokens(text: str, token_scores: List[Dict]) -> str:
    """
    Generate HTML with highlighted tokens
    
    Args:
        text: Original text
        token_scores: List of {word, type, importance}
    
    Returns:
        HTML string with highlighted text
    """
    
    highlighted = text
    
    # Sort by importance (descending)
    sorted_tokens = sorted(token_scores, key=lambda x: x["importance"], reverse=True)
    
    for token_info in sorted_tokens:
        word = token_info["word"]
        token_type = token_info["type"]
        importance = token_info["importance"]
        
        # Color coding
        if token_type == "negative":
            color = f"rgba(255, 0, 0, {importance})"  # Red
        else:
            color = f"rgba(0, 255, 0, {importance})"  # Green
        
        # Replace word with highlighted version
        highlighted = highlighted.replace(
            word,
            f'<mark style="background-color: {color};">{word}</mark>'
        )
    
    return highlighted


def extract_attention_weights(text: str, model_output) -> List[Dict]:
    """
    Extract attention weights from transformer model
    TODO: Implement with actual transformer model
    """
    pass


def compute_shap_values(text: str, model) -> List[Dict]:
    """
    Compute SHAP values for text classification
    TODO: Implement with SHAP library
    """
    pass
