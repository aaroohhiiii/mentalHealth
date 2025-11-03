"""
Test Script for LLM Enhancement
Verifies Groq API integration and hybrid analysis
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def test_groq_connection():
    """Test Groq API connection"""
    print("\n" + "="*60)
    print("Testing Groq API Connection")
    print("="*60)
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("\n📋 Setup instructions:")
        print("1. Get free API key: https://console.groq.com/keys")
        print("2. Create .env file:")
        print("   cp .env.example .env")
        print("3. Add your key:")
        print("   GROQ_API_KEY=your_key_here")
        return False
    
    print(f"✅ GROQ_API_KEY found: {api_key[:20]}...")
    
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        # Test with simple request
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Say 'Hello, I am working!' in JSON format"}],
            max_tokens=50,
            response_format={"type": "json_object"}
        )
        
        print(f"✅ Groq API connection successful!")
        print(f"   Model: llama-3.1-8b-instant")
        print(f"   Response: {response.choices[0].message.content[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Groq API connection failed: {e}")
        return False


def test_text_enhancement():
    """Test text analysis enhancement"""
    print("\n" + "="*60)
    print("Testing Text Analysis Enhancement")
    print("="*60)
    
    try:
        from services.text_infer import analyze_text
        from services.llm_enhance import enhance_text_analysis
        
        test_text = "I've been feeling really overwhelmed lately. Haven't slept well in days and I'm constantly worried about work deadlines. Getting irritable with family."
        
        print(f"\n📝 Input text:")
        print(f"   '{test_text}'")
        
        # Stage 1: Pre-trained model
        print(f"\n[Stage 1] Running pre-trained sentiment analysis...")
        model_result = analyze_text(test_text)
        print(f"   Score: {model_result['score']}")
        print(f"   Bucket: {model_result['bucket']}")
        print(f"   Sentiment: {model_result['explain']['sentiment']}")
        
        # Stage 2: LLM enhancement
        print(f"\n[Stage 2] Enhancing with LLM (Llama 3.1)...")
        enhanced_result = enhance_text_analysis(test_text, model_result)
        
        if enhanced_result.get('enhanced'):
            print(f"   ✅ LLM enhancement successful!")
            print(f"\n   📊 LLM Analysis:")
            print(f"      Risk Level: {enhanced_result.get('llm_risk_level')}")
            print(f"      Reasoning: {enhanced_result.get('reasoning', '')[:100]}...")
            print(f"\n   🎯 Key Concerns:")
            for i, concern in enumerate(enhanced_result.get('key_concerns', [])[:3], 1):
                print(f"      {i}. {concern}")
            print(f"\n   💡 Suggestions:")
            for i, suggestion in enumerate(enhanced_result.get('suggestions', [])[:3], 1):
                print(f"      {i}. {suggestion}")
            return True
        else:
            print(f"   ⚠️  LLM enhancement not available")
            print(f"   Note: {enhanced_result.get('note', 'Unknown reason')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Text enhancement failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_audio_enhancement():
    """Test audio analysis enhancement"""
    print("\n" + "="*60)
    print("Testing Audio Analysis Enhancement")
    print("="*60)
    
    try:
        from services.audio_infer import analyze_audio
        from services.llm_enhance import enhance_audio_analysis
        
        # Create dummy audio for testing
        dummy_audio = b"RIFF" + b"\x00" * 100
        
        print(f"\n🎤 Analyzing sample audio...")
        
        # Stage 1: Pre-trained model
        print(f"[Stage 1] Running audio emotion detection...")
        model_result = analyze_audio(dummy_audio, "test_audio.wav")
        print(f"   Score: {model_result['score']}")
        print(f"   Dominant emotion: {model_result['explain']['dominant_emotion']}")
        
        # Stage 2: LLM enhancement
        print(f"\n[Stage 2] Enhancing with LLM...")
        enhanced_result = enhance_audio_analysis(model_result)
        
        if enhanced_result.get('enhanced'):
            print(f"   ✅ LLM enhancement successful!")
            print(f"      Interpretation: {enhanced_result.get('interpretation', '')[:80]}...")
            print(f"      Concern level: {enhanced_result.get('concern_level')}")
            print(f"      Tip: {enhanced_result.get('actionable_tip', '')[:80]}...")
            return True
        else:
            print(f"   ⚠️  LLM enhancement not available")
            return False
            
    except Exception as e:
        print(f"   ❌ Audio enhancement failed: {e}")
        return False


def test_image_enhancement():
    """Test image analysis enhancement"""
    print("\n" + "="*60)
    print("Testing Image Analysis Enhancement")
    print("="*60)
    
    try:
        from services.image_infer import analyze_image
        from services.llm_enhance import enhance_image_analysis
        from PIL import Image
        import io
        
        # Create test image
        img = Image.new('RGB', (100, 100), color='black')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()
        
        print(f"\n📸 Analyzing sample image...")
        
        # Stage 1: Pre-trained model
        print(f"[Stage 1] Running facial expression analysis...")
        model_result = analyze_image(img_bytes, "test_image.jpg")
        print(f"   Score: {model_result['score']}")
        print(f"   Face detected: {model_result['explain']['face_detected']}")
        
        # Stage 2: LLM enhancement
        print(f"\n[Stage 2] Enhancing with LLM...")
        enhanced_result = enhance_image_analysis(model_result)
        
        if enhanced_result.get('enhanced'):
            print(f"   ✅ LLM enhancement successful!")
            print(f"      Mood interpretation: {enhanced_result.get('mood_interpretation', '')[:80]}...")
            print(f"      Mood boost tip: {enhanced_result.get('mood_boost_tip', '')[:80]}...")
            return True
        else:
            print(f"   ⚠️  LLM enhancement not available")
            return False
            
    except Exception as e:
        print(f"   ❌ Image enhancement failed: {e}")
        return False


def main():
    print("\n" + "🧠 Mental Health AI - LLM Enhancement Testing")
    print("="*60)
    
    results = {
        "groq_connection": test_groq_connection(),
        "text_enhancement": test_text_enhancement(),
        "audio_enhancement": test_audio_enhancement(),
        "image_enhancement": test_image_enhancement()
    }
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():30} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All LLM enhancement tests passed!")
        print("\n✨ Your hybrid AI system is fully operational!")
        print("\nYou can now:")
        print("  1. Start the server: uvicorn app:app --reload")
        print("  2. Use enhanced endpoints:")
        print("     - POST /analyze/text/enhanced")
        print("     - POST /analyze/audio/enhanced")
        print("     - POST /analyze/image/enhanced")
        print("     - POST /aggregate/day/enhanced")
    else:
        print("⚠️  Some tests failed")
        print("\nIf Groq connection failed:")
        print("  - Check GROQ_API_KEY in .env file")
        print("  - Get free key: https://console.groq.com/keys")
        print("\nIf other tests failed:")
        print("  - Check server logs for details")
        print("  - System will use pre-trained models only (still works!)")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
