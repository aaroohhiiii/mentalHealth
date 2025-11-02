"""
Model Initialization Script
Pre-downloads and caches all AI models on first setup
Run this before starting the server to avoid delays during first API calls
"""

import os
import sys

def download_models():
    """Download and cache all pre-trained models"""
    
    print("=" * 60)
    print("Mental Health AI - Model Initialization")
    print("=" * 60)
    print()
    
    # 1. Text Analysis Model
    print("📝 [1/3] Downloading text sentiment model...")
    try:
        from transformers import pipeline, AutoTokenizer
        model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        print(f"   Loading: {model_name}")
        
        sentiment_model = pipeline(
            "sentiment-analysis",
            model=model_name,
            tokenizer=model_name
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Test it
        test_result = sentiment_model("I feel great today!")
        print(f"   ✓ Text model loaded successfully")
        print(f"   Test: {test_result[0]}")
    except Exception as e:
        print(f"   ⚠️  Warning: Could not load text model: {e}")
        print(f"   Will use keyword-based fallback")
    
    print()
    
    # 2. Audio Analysis Model
    print("🎤 [2/3] Downloading audio emotion model...")
    try:
        from transformers import pipeline
        print(f"   Loading: ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")
        
        audio_model = pipeline(
            "audio-classification",
            model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
        )
        
        print(f"   ✓ Audio model loaded successfully")
    except Exception as e:
        print(f"   ⚠️  Warning: Could not load audio model: {e}")
        print(f"   Will use placeholder analysis")
    
    print()
    
    # 3. Image Analysis Model (FER)
    print("📸 [3/3] Initializing facial expression recognition...")
    try:
        from fer import FER
        print(f"   Loading: FER with MTCNN face detection")
        
        detector = FER(mtcnn=True)
        
        print(f"   ✓ FER model loaded successfully")
    except Exception as e:
        print(f"   ⚠️  Warning: Could not load FER model: {e}")
        print(f"   Will use placeholder analysis")
    
    print()
    print("=" * 60)
    print("✅ Model initialization complete!")
    print("=" * 60)
    print()
    print("Models are cached and ready to use.")
    print("You can now start the server with: uvicorn app:app --reload")
    print()


if __name__ == "__main__":
    download_models()
