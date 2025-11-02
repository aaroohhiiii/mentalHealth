# MindEase - Mental Health AI System
## Complete Technical Documentation for Judges

---

## 🎯 Project Overview

**MindEase** is an AI-powered mental health monitoring system that analyzes text, audio, and facial expressions to detect early signs of stress and depression. It uses a hybrid approach combining **pre-trained deep learning models** with **LLM-enhanced reasoning** to provide comprehensive mental health insights.

**Tagline:** *Find Calm. Feel Better.*

---

## 📊 System Architecture

### **Multi-Modal Analysis Pipeline**

```
User Input (Text/Audio/Image)
    ↓
Pre-trained ML Models
    ├── RoBERTa (Text Sentiment)
    ├── Wav2Vec2 (Audio Emotion)
    └── FER (Facial Expression)
    ↓
LLM Enhancement (Groq Llama 3.1 8B)
    ↓
Risk Score (0-1) + Bucket (Low/Moderate/High)
    ↓
Explainable Results + Personalized Suggestions
```

---

## 🧠 Machine Learning Models Used

### 1. **Text Analysis: RoBERTa**
- **Model:** `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Type:** Transformer-based sentiment analysis (125M parameters)
- **Purpose:** Detects depression/stress indicators in written text
- **Features:**
  - Token-level attention for explainability
  - Sentiment classification (positive/negative/neutral)
  - Keyword extraction for mental health themes
  - Real-time inference (<500ms)

**How it works:**
```python
Text Input → Tokenization → RoBERTa Encoder → 
Sentiment Score → Stress Mapping (0-1) → 
Risk Categorization (Low/Moderate/High)
```

### 2. **Audio Analysis: Wav2Vec2**
- **Model:** `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition`
- **Type:** Speech emotion recognition (1.27GB model)
- **Purpose:** Analyzes vocal patterns for emotional state
- **Features:**
  - Detects 6 emotions: neutral, happy, sad, angry, fear, surprise
  - Vocal feature extraction (pitch, energy, spectral analysis)
  - Supports multiple audio formats (.wav, .mp3, .ogg, .flac, .webm)
  - Automatic webm-to-wav conversion

**How it works:**
```python
Audio Recording → Format Conversion (if needed) → 
Audio Resampling (16kHz) → Wav2Vec2 Feature Extraction → 
Emotion Classification → Stress Mapping → Risk Score
```

**Vocal Features Analyzed:**
- Mean pitch & variance
- Energy levels
- Zero-crossing rate
- Spectral centroid

### 3. **Image Analysis: FER (Facial Expression Recognition)**
- **Model:** Custom FER CNN model
- **Type:** Convolutional Neural Network for facial emotion
- **Purpose:** Detects emotions from facial expressions
- **Features:**
  - Real-time face detection
  - 7 emotion categories
  - Confidence scores per emotion
  - Privacy-preserving (no image storage)

**How it works:**
```python
Selfie Upload → Face Detection → 
Image Preprocessing (64x64 grayscale) → 
CNN Classification → Top 3 Emotions → 
Stress Score Calculation
```

---

## 🚀 Key Technical Features

### **1. Hybrid AI Approach**
Combines the accuracy of pre-trained models with LLM reasoning:

**Pre-trained Models (Fast & Accurate):**
- RoBERTa: 125M parameters, trained on 58M tweets
- Wav2Vec2: 1.27GB model, trained on speech emotion datasets
- FER CNN: Trained on facial expression databases

**LLM Enhancement (Groq Llama 3.1 8B):**
- Contextual interpretation of ML results
- Personalized mental health suggestions
- Natural language explanations
- Holistic daily assessment

### **2. Multi-Modal Fusion**
Late fusion strategy for daily aggregation:
```python
Daily Score = weighted_average(
    text_scores,    # Weight: 0.4
    audio_scores,   # Weight: 0.35
    image_scores    # Weight: 0.25
)
```

**Reasoning:** Text provides most explicit information, audio captures tone/emotion, images add visual confirmation.

### **3. Privacy-First Design**
- ✅ **Local Processing:** All analysis happens on-device/server
- ✅ **No Cloud Storage:** Raw audio/images never stored
- ✅ **Anonymized Data:** Only aggregated scores saved
- ✅ **Data Purge:** Users can delete all data instantly
- ✅ **No Tracking:** No user identification or surveillance

---

## 🔧 Technology Stack

### **Backend**
- **Framework:** FastAPI (Python)
- **ML Libraries:**
  - PyTorch 2.1.2
  - Transformers 4.37.2 (HuggingFace)
  - Librosa 0.10.1 (audio processing)
  - OpenCV 4.9.0 (image processing)
- **LLM Integration:** Groq API (Llama 3.1 8B Instant)
- **Audio Processing:** pydub 0.25.1 (webm conversion)

### **Frontend**
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite 5.0
- **Styling:** Custom CSS with responsive design
- **Charts:** Recharts (trend visualization)
- **Audio Recording:** MediaRecorder API (browser native)

### **APIs & Models**
```
├── /analyze/text              - RoBERTa sentiment analysis
├── /analyze/audio             - Wav2Vec2 emotion recognition
├── /analyze/image             - FER facial analysis
├── /analyze/text/enhanced     - RoBERTa + LLM explanation
├── /analyze/audio/enhanced    - Wav2Vec2 + LLM reasoning
├── /analyze/image/enhanced    - FER + LLM interpretation
├── /aggregate/day             - Multi-modal fusion
├── /aggregate/day/enhanced    - Fusion + LLM assessment
└── /trend/7d                  - 7-day trend data
```

---

## 📈 How It Works (Step-by-Step)

### **User Journey:**

#### **1. Daily Check-in**
User visits MindEase and logs their mental state through:
- **Text:** "I feel overwhelmed with work and can't sleep well"
- **Audio:** 5-10 second voice recording
- **Selfie:** Quick photo capture

#### **2. Analysis Phase**
Each modality is processed independently:

**Text Analysis:**
```
1. Input text tokenized
2. RoBERTa processes tokens
3. Sentiment extracted (negative: 0.82 confidence)
4. Keywords detected: "overwhelmed", "can't sleep"
5. Stress score calculated: 0.68 (Moderate risk)
6. LLM generates explanation
```

**Audio Analysis:**
```
1. WebM recording uploaded
2. Converted to WAV (16kHz)
3. Wav2Vec2 analyzes vocal patterns
4. Emotions detected: sad (45%), fear (30%)
5. Stress score: 0.72 (Moderate-High risk)
6. LLM provides vocal interpretation
```

**Image Analysis:**
```
1. Selfie uploaded
2. Face detected and cropped
3. FER CNN classifies expression
4. Top emotions: sad (60%), neutral (25%)
5. Stress score: 0.58 (Moderate risk)
6. LLM adds context
```

#### **3. Fusion & Results**
```
Daily Aggregate Score = 
  (0.68 × 0.4) + (0.72 × 0.35) + (0.58 × 0.25)
= 0.272 + 0.252 + 0.145
= 0.669 (Moderate Risk)
```

**LLM-Enhanced Assessment:**
```
"Based on your check-in, you're experiencing moderate stress 
levels. The combination of work overwhelm, sleep difficulties, 
and emotional indicators suggest you might benefit from:

1. Sleep hygiene improvements
2. Workload management strategies
3. Stress reduction techniques
4. Consider speaking with a counselor if symptoms persist"
```

#### **4. Trend Tracking**
- 7-day visualization shows risk score over time
- Identifies patterns and triggers
- Helps users see progress

---

## 🎨 User Interface

### **Pages:**

1. **Home** - Welcome screen with system overview
2. **New Entry** - Multi-modal input interface
   - Text area for daily logs
   - Audio recorder with 🎙️ controls
   - Camera for selfie capture
   - Real-time results display
3. **Dashboard** - Analysis results with:
   - Risk gauge (0-100%)
   - Modality breakdowns
   - Explainable AI insights
4. **Trends** - 7-day visualization
   - Line chart of daily scores
   - Color-coded risk levels
   - Pattern identification
5. **Privacy** - Data management
   - Delete all data option
   - Privacy policy
   - Data usage transparency

---

## 🔬 Technical Innovations

### **1. Browser-to-Server WebM Support**
**Challenge:** Browsers record audio in WebM format, but ML models need WAV.

**Solution:** 
```python
# Server-side conversion without system ffmpeg
def _convert_webm_to_wav(audio_bytes: bytes) -> bytes:
    # Use pydub (pure Python) to convert
    audio = AudioSegment.from_file(BytesIO(webm_bytes), format="webm")
    audio.export(temp_wav, format="wav")
    return wav_bytes
```

**Impact:** No client-side processing needed, works on all browsers

### **2. Explainable AI with Attention**
RoBERTa provides token-level attention scores showing which words influenced the decision:
```json
{
  "tokens": [
    {"word": "overwhelmed", "score": 0.89, "type": "negative"},
    {"word": "can't", "score": 0.76, "type": "negative"},
    {"word": "sleep", "score": 0.68, "type": "concern"}
  ]
}
```

### **3. Hybrid Inference Strategy**
- **Fast path:** Pre-trained models only (200-500ms)
- **Enhanced path:** Models + LLM (1-2s)
- Users choose based on need

### **4. Progressive Model Loading**
Models load on-demand to save memory:
```python
# Lazy loading
_audio_model = None

def _load_audio_model():
    global _audio_model
    if _audio_model is None:
        _audio_model = pipeline("audio-classification", ...)
    return _audio_model
```

---

## 📊 Performance Metrics

### **Inference Times:**
- Text Analysis: 200-400ms
- Audio Analysis: 500-800ms (including conversion)
- Image Analysis: 300-500ms
- LLM Enhancement: +1000-1500ms

### **Model Sizes:**
- RoBERTa: 498MB
- Wav2Vec2: 1.27GB
- FER CNN: ~50MB

### **Accuracy (Based on literature):**
- RoBERTa Sentiment: ~85% accuracy
- Wav2Vec2 Emotion: ~70-75% accuracy
- FER: ~65-70% accuracy
- Multi-modal Fusion: ~80-85% (estimated)

---

## 🛡️ Privacy & Security

### **Data Flow:**
```
User Input → Temporary Processing → Analysis Results → Storage
              ↓                      ↓
         (No raw data)          (Scores only)
              ↓                      ↓
         Deleted after          User-controlled
```

### **Privacy Features:**
1. **No Personal Identification:** System doesn't require login
2. **No Cloud Storage:** All data local
3. **No Audio/Image Retention:** Deleted after analysis
4. **Aggregated Scores Only:** Only numerical results stored
5. **Instant Purge:** Delete all data with one click
6. **No Tracking:** No cookies, analytics, or telemetry

### **Ethical Considerations:**
- ⚠️ **Not a Medical Device:** Clearly stated disclaimer
- ⚠️ **Educational Purpose:** For research and awareness only
- ⚠️ **Professional Guidance:** Recommends consulting healthcare professionals
- ⚠️ **Non-Diagnostic:** Results are indicators, not diagnoses

---

## 🚀 Deployment & Setup

### **Running Locally:**

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# Opens on http://localhost:5173
```

### **System Requirements:**
- Python 3.10+
- Node.js 18+
- 8GB RAM (for ML models)
- 5GB disk space (model storage)

---

## 🎓 Educational Value

### **Learning Outcomes:**
1. **Multi-Modal AI:** Combining text, audio, and visual inputs
2. **Pre-trained Models:** Leveraging HuggingFace transformers
3. **LLM Integration:** Enhancing ML with language models
4. **Full-Stack ML:** End-to-end deployment
5. **Privacy-First Design:** Ethical AI development
6. **Real-World Application:** Mental health technology

### **Use Cases:**
- **Research:** Study mental health patterns
- **Education:** Learn about AI in healthcare
- **Awareness:** Understand mental wellness
- **Self-Monitoring:** Track personal mental state
- **Early Detection:** Identify concerning trends

---

## 📚 Technical Challenges Overcome

### **1. PyTorch-FFmpeg Conflict on macOS**
**Problem:** System ffmpeg caused mutex lock errors with PyTorch

**Solution:** Used pydub (pure Python) for audio conversion instead

### **2. WebM Browser Recording**
**Problem:** Browsers record in WebM, models need WAV

**Solution:** Server-side conversion pipeline

### **3. Model Size & Loading**
**Problem:** 1.2GB+ models slow to load

**Solution:** Lazy loading + caching

### **4. Real-time Inference**
**Problem:** Need fast responses for good UX

**Solution:** CPU-optimized models + async processing

### **5. Explainability**
**Problem:** ML models are "black boxes"

**Solution:** Attention mechanisms + LLM explanations

---

## 🏆 Innovation Highlights

1. **Hybrid AI Architecture:** Combines precision of specialized models with reasoning of LLMs
2. **Multi-Modal Fusion:** Analyzes 3 different input types simultaneously
3. **Privacy-Preserving:** No data storage, all processing ephemeral
4. **Explainable Results:** Shows why decisions were made
5. **Browser-Native:** No app installation required
6. **Open Source Models:** Uses public, research-backed models
7. **Real-Time Processing:** Instant feedback to users
8. **Trend Analysis:** 7-day pattern recognition

---

## 📝 Citations & References

### **Models:**
1. RoBERTa: "A Robustly Optimized BERT Pretraining Approach" (Liu et al., 2019)
2. Wav2Vec2: "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations" (Baevski et al., 2020)
3. FER: "Challenges in Representation Learning: Facial Expression Recognition" (Goodfellow et al., 2013)

### **Frameworks:**
- HuggingFace Transformers
- PyTorch
- FastAPI
- React

---

## 🔮 Future Enhancements

1. **Longitudinal Analysis:** Long-term pattern tracking
2. **Crisis Detection:** Immediate intervention triggers
3. **Multi-Language Support:** Global accessibility
4. **Mobile App:** iOS/Android native apps
5. **Wearable Integration:** Heart rate, sleep data
6. **Therapist Dashboard:** Professional monitoring tools
7. **Community Support:** Anonymous peer groups
8. **Advanced Models:** GPT-4 Vision, Whisper integration

---

## 📞 Technical Support

**Repository:** https://github.com/aaroohhiiii/mentalHealth

**Technologies Used:**
- Python 3.10.16
- React 18
- PyTorch 2.1.2
- Transformers 4.37.2
- FastAPI 0.109.0
- Groq API (Llama 3.1 8B)

---

## 📋 Summary for Judges

**MindEase** represents a comprehensive, privacy-first approach to mental health monitoring using cutting-edge AI technology. By combining:

✅ **Pre-trained deep learning models** (RoBERTa, Wav2Vec2, FER)  
✅ **LLM-enhanced reasoning** (Groq Llama 3.1 8B)  
✅ **Multi-modal data fusion** (text + audio + image)  
✅ **Explainable AI** (attention mechanisms + natural language)  
✅ **Privacy-preserving architecture** (no data storage)  

...we've created a system that provides actionable mental health insights while maintaining user privacy and ethical standards.

The system demonstrates technical excellence in ML engineering, full-stack development, and responsible AI deployment, making it both an educational tool and a practical application for mental wellness awareness.

---

**Disclaimer:** *This system is for educational and research purposes only. It is not a medical device and should not be used for clinical diagnosis. Users experiencing mental health concerns should consult qualified healthcare professionals.*

---

**Built with ❤️ for mental health awareness**
