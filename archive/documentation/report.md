# Mental Health AI System - Technical Report

**Author:** Aarohi (B.Tech)  
**Project:** Multi-Modal Mental Health Monitoring System  
**Date:** November 2025  
**Duration:** 48-hour rapid prototype

---

## Executive Summary

This project implements an early detection system for stress and depression using three modalities:
- **Text Analysis (NLP)**: Daily text logs analyzed for sentiment and stress indicators
- **Audio Analysis (SER)**: Voice check-ins analyzed for emotional tone
- **Image Analysis (FER)**: Facial expressions analyzed for emotional state

**Key Features:**
- Multi-modal fusion for comprehensive assessment
- Explainable AI with token highlights and emotion breakdown
- Privacy-first: local processing, in-memory storage
- Non-diagnostic: Educational tool with ethical disclaimers
- Full-stack: FastAPI backend + React/Vite frontend

---

## 1. Dataset & Data Sources

### 1.1 Text Data
- **Placeholder Phase:** Rule-based keyword matching (negative/positive indicators)
- **Real Implementation (TODO):**
  - Sentiment140, GoEmotions, or mental health forum datasets
  - Synthetic anonymized text logs
  - Fine-tuned on stress/depression indicators

### 1.2 Audio Data
- **Placeholder Phase:** Deterministic pseudo-random emotion generation
- **Real Implementation (TODO):**
  - RAVDESS (Ryerson Audio-Visual Database of Emotional Speech)
  - CREMA-D (Crowd-sourced Emotional Multimodal Actors Dataset)
  - Features: MFCC (13 coefficients), Chroma, Spectral Centroid, ZCR, Energy

### 1.3 Image Data
- **Placeholder Phase:** Simulated facial emotion recognition
- **Real Implementation (TODO):**
  - FER2013 (Facial Expression Recognition 2013)
  - AffectNet (large-scale facial expression dataset)
  - 7 emotions: angry, disgust, fear, happy, sad, surprise, neutral

---

## 2. Preprocessing Pipeline

### 2.1 Text Preprocessing
```
Raw Text → Tokenization → Lowercasing → Keyword Matching → Sentiment Score
```

**Future:** 
```
Raw Text → BERT Tokenization → Embedding → Classification Head → Risk Score
```

### 2.2 Audio Preprocessing
```
Audio File → Load (librosa) → Feature Extraction (MFCC, Chroma, etc.) → Normalization → XGBoost → Emotion Probs
```

### 2.3 Image Preprocessing
```
Image → Face Detection (OpenCV/MTCNN) → Crop & Resize → FER Model → Emotion Distribution
Daily: Multiple Images → Aggregation → Daily Mood Index
```

---

## 3. Model Architecture

### 3.1 Text Model
**Current:** Rule-based keyword matching  
**Target:** 
- Base: `distilbert-base-multilingual-cased` or `cardiffnlp/twitter-roberta-base-sentiment`
- Head: Logistic Regression or simple MLP
- Output: Binary classification (stress/no-stress) + confidence

### 3.2 Audio Model
**Current:** Deterministic pseudo-random  
**Target:**
- Features: librosa-extracted (MFCC, Chroma, Spectral features)
- Model: XGBoost classifier (7 emotions)
- Emotion → Stress mapping

### 3.3 Image Model
**Current:** Simulated FER  
**Target:**
- Base: `fer` library (FER2013) or MobileNetV2 (FER-trained)
- Output: 7-emotion probabilities
- Daily aggregation: Average of 4-5 daily selfies

### 3.4 Fusion Model
**Late Fusion:**
```
final_score = w_text * text_score + w_audio * audio_score + w_image * image_score
```

**Default Weights:**
- Text: 0.5 (highest weight - most reliable self-report)
- Audio: 0.25
- Image: 0.25

**Risk Categorization:**
- Low: score < 0.33
- Moderate: 0.33 ≤ score < 0.66
- High: score ≥ 0.66

---

## 4. Evaluation Metrics

### 4.1 Per-Modality Metrics
- **Accuracy, Precision, Recall, F1-Score** (for classification tasks)
- **AUC-ROC** (for risk score calibration)

### 4.2 Fusion Metrics
- **Overall Classification Accuracy**
- **Early Detection Rate** (days ahead of clinical diagnosis)
- **False Positive Rate** (minimize over-alarming)

### 4.3 Explainability Metrics
- **Token Importance Coverage** (% of influential tokens highlighted)
- **User Satisfaction** (qualitative feedback on explanations)

---

## 5. Explainability Features

### 5.1 Text
- **Token Highlights:** Negative/positive keywords color-coded
- **Themes:** Sleep issues, anxiety, low mood, isolation
- **Attention Weights (Future):** BERT attention visualization

### 5.2 Audio
- **Emotion Distribution:** Bar chart of detected emotions
- **Vocal Features:** Pitch, energy, speech rate displayed
- **Salient Frames (Future):** Highlight high-emotion segments

### 5.3 Image
- **Top Emotions:** Display top 3 facial expressions
- **Confidence Scores:** Model confidence for each prediction
- **Heatmaps (Future):** Grad-CAM for facial region importance

---

## 6. Ethics & Privacy

### 6.1 Ethical Considerations
✅ **Non-Diagnostic Disclaimer:** Clearly stated throughout UI  
✅ **No Medical Claims:** Not a replacement for professional care  
✅ **Transparent:** Explanations provided for all predictions  
✅ **User Control:** Delete data anytime, local-only mode  

### 6.2 Privacy Measures
✅ **Local Processing:** All inference happens on-device  
✅ **In-Memory Storage:** Default mode (no persistent files)  
✅ **No Cloud Upload:** Audio/images never leave the machine  
✅ **Anonymized:** No personal identifiers collected  
✅ **GDPR-Ready:** Right to delete, right to view data  

### 6.3 Bias Mitigation
⚠️ **TODO:** Test on diverse demographics (age, gender, ethnicity)  
⚠️ **TODO:** Validate across cultural contexts (emotion expression varies)  
⚠️ **TODO:** Monitor for false positive/negative disparities  

---

## 7. System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  React + Vite Frontend              │
│  (Dashboard, New Entry, Trends, Privacy)            │
└────────────────┬────────────────────────────────────┘
                 │ HTTP/REST API
                 ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)            │
│  Endpoints: /analyze/text, /audio, /image, etc.    │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────┴────────┬────────────┐
        ▼                 ▼            ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Text Service │  │ Audio Service│  │ Image Service│
│ (NLP)        │  │ (SER)        │  │ (FER)        │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │
       └─────────────────┴──────────────────┘
                         │
                         ▼
                 ┌──────────────┐
                 │ Fusion Service│
                 │ (Late Fusion) │
                 └──────┬────────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   Storage    │
                 │ (In-Memory)  │
                 └──────────────┘
```

---

## 8. Performance & Scalability

### 8.1 Current Performance (Placeholder)
- **Text Analysis:** ~10ms per entry (keyword matching)
- **Audio Analysis:** ~50ms per file (simulated)
- **Image Analysis:** ~30ms per image (simulated)

### 8.2 Target Performance (Real Models)
- **Text:** ~100-200ms (DistilBERT inference on CPU)
- **Audio:** ~500-1000ms (librosa feature extraction + XGBoost)
- **Image:** ~200-500ms (FER inference on CPU)

### 8.3 Scalability
- **Current:** Single-user, local deployment
- **Future:** Multi-user with Redis caching, batch processing

---

## 9. Deployment Instructions

### 9.1 Backend Setup
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### 9.2 Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```

### 9.3 Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 10. Future Enhancements

### 10.1 Short-Term (Next 2 Weeks)
- [ ] Replace placeholder models with real ML models
- [ ] Add model training scripts
- [ ] Implement SHAP for text explainability
- [ ] Add audio waveform visualization
- [ ] Implement daily aggregation logic

### 10.2 Medium-Term (1-2 Months)
- [ ] Multi-user support with authentication
- [ ] Data export (CSV/JSON)
- [ ] Trend analysis with anomaly detection
- [ ] Mobile app (React Native)
- [ ] Integration with wearables (heart rate, sleep)

### 10.3 Long-Term (3-6 Months)
- [ ] Clinical validation study
- [ ] Longitudinal tracking (months/years)
- [ ] Personalized intervention recommendations
- [ ] Collaboration with mental health professionals
- [ ] Regulatory compliance (CE Mark, FDA clearance if applicable)

---

## 11. Limitations

⚠️ **Current Limitations:**
1. **Placeholder Models:** Not yet using real ML inference
2. **Small Dataset:** No large-scale validation yet
3. **Single Language:** English-only (NLP)
4. **No Longitudinal Validation:** Requires long-term study
5. **CPU-Only:** Slower inference compared to GPU

⚠️ **Inherent Limitations:**
1. **Not a Medical Device:** Cannot replace clinical diagnosis
2. **Self-Reported Data:** Subject to bias and incomplete information
3. **Cultural Variation:** Emotion expression varies across cultures
4. **Privacy-Performance Tradeoff:** Local processing limits model size

---

## 12. Conclusion

This Mental Health AI System demonstrates a **privacy-first, explainable, multi-modal approach** to early detection of mental health concerns. While currently using placeholder models, the architecture is designed for **seamless integration of real ML models** trained on validated datasets.

**Key Achievements:**
✅ Full-stack prototype (FastAPI + React)  
✅ Multi-modal fusion pipeline  
✅ Explainable AI features  
✅ Privacy-preserving design  
✅ Ethical disclaimers and user control  

**Next Steps:**
1. Train real models on validated datasets
2. Conduct user testing for UX/explainability
3. Validate accuracy against clinical assessments
4. Explore partnerships with mental health organizations

---

## 13. References

### Datasets
- **FER2013:** Goodfellow et al. (2013)
- **RAVDESS:** Livingstone & Russo (2018)
- **Sentiment140:** Go et al. (2009)

### Models
- **DistilBERT:** Sanh et al. (2019)
- **XGBoost:** Chen & Guestrin (2016)
- **FER Library:** https://github.com/justinshenk/fer

### Ethics
- **AI Ethics Guidelines:** EU HLEG (2019)
- **Mental Health AI:** Graham et al. (2019)

---

**Document Version:** 1.0  
**Last Updated:** November 2, 2025  
**Contact:** Aarohi (B.Tech)
