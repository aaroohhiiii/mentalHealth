# Model Artifacts

This directory contains trained machine learning models:

## Current Status: Placeholder Models

The system currently uses rule-based placeholder logic. Real models will be added incrementally:

### Text Analysis (`text_lr.joblib`)
- **Model**: Logistic Regression on DistilBERT embeddings
- **Training**: Fine-tuned on mental health text datasets
- **Status**: 🔴 Pending

### Audio Analysis (`audio_xgb.json`)
- **Model**: XGBoost classifier on librosa features
- **Features**: MFCC (13), Chroma (12), Spectral Centroid, ZCR, Energy
- **Status**: 🔴 Pending

### Image Analysis
- **Model**: FER library or MobileNet (FER2013)
- **Task**: Facial Expression Recognition (7 emotions)
- **Status**: 🔴 Pending

## Model Files (Will be added)

```
models/
├── text_lr.joblib              # Logistic Regression (text)
├── text_vectorizer.joblib      # Feature vectorizer
├── audio_xgb.json              # XGBoost (audio)
├── audio_scaler.joblib         # Feature scaler
└── image_fer_mobilenet.h5      # MobileNet FER (optional)
```

## Training Instructions

Models will be trained on:
- **Text**: Synthetic/anonymized mental health text data
- **Audio**: RAVDESS, CREMA-D, or similar SER datasets
- **Images**: FER2013 or AffectNet datasets

Training scripts to be added in `backend/train/`
