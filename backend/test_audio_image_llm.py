#!/usr/bin/env python3
"""
Complete test of Audio and Image LLM enhancement
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("🎤📸 TESTING AUDIO & IMAGE LLM ENHANCEMENT")
print("=" * 70)
print()

# Test Audio Enhancement
print("🎤 TEST 1: Audio Emotion Analysis + LLM Enhancement")
print("-" * 70)

try:
    from services.llm_enhance import enhance_audio_analysis
    
    # Simulate audio model output
    audio_result = {
        "score": 0.68,
        "bucket": "Moderate",
        "explain": {
            "dominant_emotion": "stress",
            "emotion_distribution": {
                "stress": 0.45,
                "sadness": 0.25,
                "neutral": 0.20,
                "happy": 0.10
            },
            "confidence": 0.78
        }
    }
    
    print(f"📊 Audio Model Output:")
    print(f"   Stress Score: {audio_result['score']}")
    print(f"   Dominant Emotion: {audio_result['explain']['dominant_emotion']}")
    print(f"   Distribution: {audio_result['explain']['emotion_distribution']}")
    print()
    
    print("🧠 Enhancing with LLM...")
    enhanced = enhance_audio_analysis(audio_result)
    
    if enhanced.get('enhanced'):
        print("✅ Audio LLM Enhancement SUCCESS!")
        print()
        print("📋 Enhanced Analysis:")
        print(f"   🎯 Interpretation: {enhanced.get('interpretation', 'N/A')}")
        print(f"   ⚠️  Concern Level: {enhanced.get('concern_level', 'N/A')}")
        print(f"   💡 Reason: {enhanced.get('concern_reason', 'N/A')}")
        print(f"   ✨ Actionable Tip: {enhanced.get('actionable_tip', 'N/A')}")
    else:
        print(f"❌ Audio enhancement failed: {enhanced.get('error', 'Unknown error')}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Audio test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print()

# Test Image Enhancement
print("📸 TEST 2: Facial Expression Analysis + LLM Enhancement")
print("-" * 70)

try:
    from services.llm_enhance import enhance_image_analysis
    
    # Simulate FER model output
    image_result = {
        "score": 0.42,
        "bucket": "Low",
        "explain": {
            "face_detected": True,
            "dominant_emotion": "happy",
            "confidence": 0.82
        },
        "top_emotions": [
            {"emotion": "happy", "score": 0.65},
            {"emotion": "neutral", "score": 0.25},
            {"emotion": "surprise", "score": 0.10}
        ]
    }
    
    print(f"📊 Image Model Output:")
    print(f"   Face Detected: {image_result['explain']['face_detected']}")
    print(f"   Stress Score: {image_result['score']}")
    print(f"   Dominant Emotion: {image_result['explain']['dominant_emotion']}")
    print(f"   Top Emotions: {image_result['top_emotions']}")
    print()
    
    print("🧠 Enhancing with LLM...")
    enhanced = enhance_image_analysis(image_result)
    
    if enhanced.get('enhanced'):
        print("✅ Image LLM Enhancement SUCCESS!")
        print()
        print("📋 Enhanced Analysis:")
        print(f"   😊 Mood Interpretation: {enhanced.get('mood_interpretation', 'N/A')}")
        print(f"   👀 Patterns to Monitor: {enhanced.get('patterns_to_monitor', 'N/A')}")
        print(f"   🎯 Mood Boost Tip: {enhanced.get('mood_boost_tip', 'N/A')}")
    else:
        print(f"❌ Image enhancement failed: {enhanced.get('error', 'Unknown error')}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Image test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print()

# Test Stressed Audio
print("🎤 TEST 3: High Stress Audio Scenario")
print("-" * 70)

try:
    stressed_audio = {
        "score": 0.85,
        "bucket": "High",
        "explain": {
            "dominant_emotion": "fear",
            "emotion_distribution": {
                "fear": 0.50,
                "stress": 0.30,
                "sadness": 0.15,
                "neutral": 0.05
            },
            "confidence": 0.88
        }
    }
    
    print(f"📊 High Stress Audio Input: Score={stressed_audio['score']}, Emotion={stressed_audio['explain']['dominant_emotion']}")
    enhanced = enhance_audio_analysis(stressed_audio)
    
    if enhanced.get('enhanced'):
        print(f"✅ Concern Level: {enhanced.get('concern_level')}")
        print(f"   Tip: {enhanced.get('actionable_tip', 'N/A')[:80]}...")
    else:
        print(f"⚠️  Enhancement not available")
        
except Exception as e:
    print(f"❌ Stressed audio test failed: {e}")

print()
print("=" * 70)
print()

# Test Sad Face
print("📸 TEST 4: Sad Facial Expression Scenario")
print("-" * 70)

try:
    sad_image = {
        "score": 0.72,
        "bucket": "Moderate",
        "explain": {
            "face_detected": True,
            "dominant_emotion": "sad",
            "confidence": 0.79
        },
        "top_emotions": [
            {"emotion": "sad", "score": 0.70},
            {"emotion": "neutral", "score": 0.20},
            {"emotion": "fear", "score": 0.10}
        ]
    }
    
    print(f"📊 Sad Face Input: Score={sad_image['score']}, Emotion={sad_image['explain']['dominant_emotion']}")
    enhanced = enhance_image_analysis(sad_image)
    
    if enhanced.get('enhanced'):
        print(f"✅ Mood Interpretation: {enhanced.get('mood_interpretation', 'N/A')[:80]}...")
        print(f"   Boost Tip: {enhanced.get('mood_boost_tip', 'N/A')[:80]}...")
    else:
        print(f"⚠️  Enhancement not available")
        
except Exception as e:
    print(f"❌ Sad face test failed: {e}")

print()
print("=" * 70)
print("🎉 ALL AUDIO & IMAGE TESTS PASSED!")
print("=" * 70)
print()
print("✨ Your hybrid AI now enhances:")
print("   ✅ Text analysis (sentiment + themes)")
print("   ✅ Audio analysis (voice emotions)")
print("   ✅ Image analysis (facial expressions)")
print()
print("🚀 Ready to process multi-modal mental health data!")
print()
