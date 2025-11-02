# 📊 DATA FLOW DIAGRAM

## 🎤 AUDIO ANALYSIS FLOW

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER UPLOADS AUDIO FILE                          │
│                      (voice_recording.wav, 2MB)                         │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────────────┐
        │    POST /analyze/audio/enhanced                   │
        │    Body: FormData                                 │
        │    file: <binary audio data>                      │
        └───────────────────┬───────────────────────────────┘
                            │
                            ▼
        ╔═══════════════════════════════════════════════════╗
        ║       STAGE 1: PRE-TRAINED MODEL (Wav2Vec2)       ║
        ║                                                   ║
        ║  Input:  audio_bytes (raw WAV data)              ║
        ║  Model:  ehcalabres/wav2vec2-lg-xlsr...          ║
        ║  Process: Extract acoustic features               ║
        ║          Classify emotions from voice patterns    ║
        ║                                                   ║
        ║  Output: {                                        ║
        ║    "score": 0.68,                                ║
        ║    "bucket": "Moderate",                         ║
        ║    "explain": {                                  ║
        ║      "dominant_emotion": "stress",               ║
        ║      "emotion_distribution": {                   ║
        ║        "stress": 0.45,                          ║
        ║        "sadness": 0.25,                         ║
        ║        "neutral": 0.20,                         ║
        ║        "happy": 0.10                            ║
        ║      }                                           ║
        ║    }                                             ║
        ║  }                                               ║
        ╚═══════════════════════════════════════════════════╝
                            │
                            ▼
        ╔═══════════════════════════════════════════════════╗
        ║       STAGE 2: LLM ENHANCEMENT (Llama 3.1 8B)    ║
        ║                                                   ║
        ║  Input:  Model output from Stage 1                ║
        ║  LLM:    Groq API (llama-3.1-8b-instant)         ║
        ║  Process: Contextual interpretation               ║
        ║          Mental health insights                   ║
        ║          Actionable recommendations               ║
        ║                                                   ║
        ║  Prompt: "Analyze this voice emotion data..."     ║
        ║                                                   ║
        ║  Output: {                                        ║
        ║    "enhanced": true,                             ║
        ║    "interpretation": "High stress detected,       ║
        ║                       may indicate anxiety...",   ║
        ║    "concern_level": "Moderate",                  ║
        ║    "concern_reason": "Persistent stress with     ║
        ║                       sadness suggests...",       ║
        ║    "actionable_tip": "Practice deep breathing    ║
        ║                       exercises for 10 mins..."   ║
        ║  }                                               ║
        ╚═══════════════════════════════════════════════════╝
                            │
                            ▼
        ┌───────────────────────────────────────────────────┐
        │         RETURN TO FRONTEND (JSON Response)        │
        └───────────────────────────────────────────────────┘
```

---

## 📸 IMAGE ANALYSIS FLOW

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER UPLOADS IMAGE FILE                          │
│                         (selfie.jpg, 1.5MB)                             │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────────────┐
        │    POST /analyze/image/enhanced                   │
        │    Body: FormData                                 │
        │    file: <binary image data>                      │
        └───────────────────┬───────────────────────────────┘
                            │
                            ▼
        ╔═══════════════════════════════════════════════════╗
        ║       STAGE 1: PRE-TRAINED MODEL (FER + MTCNN)   ║
        ║                                                   ║
        ║  Input:  image_bytes (JPEG/PNG data)             ║
        ║  Models: MTCNN (face detection)                  ║
        ║          FER trained on FER2013 dataset          ║
        ║  Process: Detect face in image                    ║
        ║          Extract facial landmarks                 ║
        ║          Classify expressions                     ║
        ║                                                   ║
        ║  Output: {                                        ║
        ║    "score": 0.42,                                ║
        ║    "bucket": "Low",                              ║
        ║    "explain": {                                  ║
        ║      "face_detected": true,                      ║
        ║      "dominant_emotion": "happy",                ║
        ║      "confidence": 0.82                          ║
        ║    },                                            ║
        ║    "top_emotions": [                             ║
        ║      {"emotion": "happy", "score": 0.65},       ║
        ║      {"emotion": "neutral", "score": 0.25},     ║
        ║      {"emotion": "surprise", "score": 0.10}     ║
        ║    ]                                             ║
        ║  }                                               ║
        ╚═══════════════════════════════════════════════════╝
                            │
                            ▼
        ╔═══════════════════════════════════════════════════╗
        ║       STAGE 2: LLM ENHANCEMENT (Llama 3.1 8B)    ║
        ║                                                   ║
        ║  Input:  Model output from Stage 1                ║
        ║  LLM:    Groq API (llama-3.1-8b-instant)         ║
        ║  Process: Mood interpretation                     ║
        ║          Pattern recognition                      ║
        ║          Personalized tips                        ║
        ║                                                   ║
        ║  Prompt: "Analyze this facial expression..."      ║
        ║                                                   ║
        ║  Output: {                                        ║
        ║    "enhanced": true,                             ║
        ║    "mood_interpretation": "Predominantly         ║
        ║                            positive mood with     ║
        ║                            content feeling...",   ║
        ║    "patterns_to_monitor": "Watch for sudden      ║
        ║                            mood shifts or...",    ║
        ║    "mood_boost_tip": "Practice gratitude by      ║
        ║                       writing 3 things you're     ║
        ║                       thankful for daily..."      ║
        ║  }                                               ║
        ╚═══════════════════════════════════════════════════╝
                            │
                            ▼
        ┌───────────────────────────────────────────────────┐
        │         RETURN TO FRONTEND (JSON Response)        │
        └───────────────────────────────────────────────────┘
```

---

## 🧪 WHAT I TESTED

```
┌─────────────────────────────────────────────────────────────┐
│          MY TEST (test_audio_image_llm.py)                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────┐
        │  SKIPPED: Real file upload              │
        │  SKIPPED: Pre-trained model processing  │
        └─────────────────────────────────────────┘
                          │
                          ▼
        ╔═════════════════════════════════════════╗
        ║  SIMULATED: Model output (Stage 1)      ║
        ║                                         ║
        ║  audio_result = {                       ║
        ║    "score": 0.68,                      ║
        ║    "explain": {                        ║
        ║      "dominant_emotion": "stress",     ║
        ║      ...                               ║
        ║    }                                   ║
        ║  }                                     ║
        ╚═════════════════════════════════════════╝
                          │
                          ▼
        ╔═════════════════════════════════════════╗
        ║  TESTED: LLM Enhancement (Stage 2)      ║
        ║                                         ║
        ║  enhanced = enhance_audio_analysis(     ║
        ║    audio_result                        ║
        ║  )                                     ║
        ║                                         ║
        ║  ✅ Verified LLM reasoning works        ║
        ║  ✅ Verified JSON parsing works         ║
        ║  ✅ Verified Groq API works             ║
        ╚═════════════════════════════════════════╝
```

---

## 💡 KEY INSIGHT

**I tested ONLY the LLM enhancement part** because:

1. ✅ Pre-trained models (Wav2Vec2, FER) are already proven to work
2. ✅ We need to verify the NEW code (LLM integration)
3. ✅ Simulating model output is faster than processing real files
4. ✅ Focuses testing on the logic we just added

**To test the FULL pipeline with real files:**
- Start the server
- Use the API docs at http://localhost:8000/docs
- Upload a real .wav audio file or .jpg image
- See both Stage 1 (model) AND Stage 2 (LLM) work together!

---

## 📁 FILE STRUCTURE

```
backend/
├── services/
│   ├── audio_infer.py          ← Stage 1 (Wav2Vec2 model)
│   ├── image_infer.py          ← Stage 1 (FER model)
│   └── llm_enhance.py          ← Stage 2 (LLM reasoning) ✨ NEW
│
├── app.py                      ← API endpoints
│
└── test_audio_image_llm.py     ← Test script (simulates Stage 1)
```
