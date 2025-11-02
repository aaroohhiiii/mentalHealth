"""
Quick Test Script for Pre-trained Models
Run this to verify all models are working correctly
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_text_analysis():
    """Test text sentiment analysis"""
    print("\n" + "="*60)
    print("Testing Text Analysis")
    print("="*60)
    
    try:
        from services.text_infer import analyze_text
        
        test_cases = [
            "I'm feeling great and energetic today!",
            "Feeling overwhelmed and stressed, can't sleep well.",
            "Had a normal day, nothing special."
        ]
        
        for i, text in enumerate(test_cases, 1):
            print(f"\n[Test {i}] Input: '{text}'")
            result = analyze_text(text)
            print(f"  Score: {result['score']}")
            print(f"  Bucket: {result['bucket']}")
            print(f"  Sentiment: {result['explain']['sentiment']}")
        
        print("\n✅ Text analysis working!")
        return True
        
    except Exception as e:
        print(f"\n❌ Text analysis failed: {e}")
        return False


def test_audio_analysis():
    """Test audio emotion recognition"""
    print("\n" + "="*60)
    print("Testing Audio Analysis")
    print("="*60)
    
    try:
        from services.audio_infer import analyze_audio
        
        # Create dummy audio bytes for testing
        dummy_audio = b"RIFF" + b"\x00" * 100  # Minimal WAV-like data
        
        print("\n[Test] Analyzing dummy audio file...")
        result = analyze_audio(dummy_audio, "test_audio.wav")
        
        print(f"  Score: {result['score']}")
        print(f"  Bucket: {result['bucket']}")
        print(f"  Dominant emotion: {result['explain']['dominant_emotion']}")
        
        if 'model' in result['explain']:
            print(f"  Using: {result['explain']['model']}")
        elif 'note' in result['explain']:
            print(f"  Note: {result['explain']['note']}")
        
        print("\n✅ Audio analysis working!")
        return True
        
    except Exception as e:
        print(f"\n❌ Audio analysis failed: {e}")
        return False


def test_image_analysis():
    """Test facial expression recognition"""
    print("\n" + "="*60)
    print("Testing Image Analysis")
    print("="*60)
    
    try:
        from services.image_infer import analyze_image
        from PIL import Image
        import io
        
        # Create a simple test image (100x100 black square)
        img = Image.new('RGB', (100, 100), color='black')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()
        
        print("\n[Test] Analyzing test image...")
        result = analyze_image(img_bytes, "test_image.jpg")
        
        print(f"  Score: {result['score']}")
        print(f"  Bucket: {result['bucket']}")
        print(f"  Face detected: {result['explain']['face_detected']}")
        if result['explain']['face_detected']:
            print(f"  Dominant emotion: {result['explain']['dominant_emotion']}")
            print(f"  Top emotions: {list(result['top_emotions'].keys())}")
        
        if 'note' in result['explain']:
            print(f"  Note: {result['explain']['note']}")
        
        print("\n✅ Image analysis working!")
        return True
        
    except Exception as e:
        print(f"\n❌ Image analysis failed: {e}")
        return False


def main():
    print("\n" + "🧠 Mental Health AI - Model Testing")
    print("="*60)
    
    results = {
        "text": test_text_analysis(),
        "audio": test_audio_analysis(),
        "image": test_image_analysis()
    }
    
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    for modality, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{modality.capitalize():10} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed! Your models are working correctly.")
        print("\nYou can now start the server with:")
        print("  uvicorn app:app --reload --port 8000")
    else:
        print("⚠️  Some tests failed, but the system will use fallback methods.")
        print("\nTo install missing dependencies:")
        print("  pip install transformers torch fer opencv-python")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
