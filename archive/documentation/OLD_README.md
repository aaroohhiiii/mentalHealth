# Mental Health Multi-Modal AI System

## 🎯 Overview
**Hybrid AI system** for early detection of stress/depression using:
- **Stage 1** - Pre-trained models (RoBERTa, Wav2Vec2, FER) - Fast & Local
- **Stage 2** - LLM enhancement (Llama 3.1 via Groq) - Smart & Contextual

**Three modalities:**
- **Text**: Daily logs analysis (NLP)
- **Audio**: 5-10s voice check-ins (SER)
- **Images**: 4-5 selfies/day (FER)

## ⚡ Quick Start

### Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # macOS/Linux (.venv\Scripts\activate on Windows)
pip install -r requirements.txt

# Setup LLM enhancement (optional but recommended)
cp .env.example .env
# Add your free Groq API key to .env file

# Pre-download AI models (recommended)
python download_models.py

# Start server
uvicorn app:app --reload --port 8000
```

**Notes:**
- First run downloads ~1.8GB of pre-trained models
- Get free Groq API key at: https://console.groq.com/keys
- See [HYBRID_SETUP.md](HYBRID_SETUP.md) for full hybrid setup guide

### Frontend (React + Vite)
```powershell
cd frontend
npm install
npm run dev
```

## 🔗 API Endpoints

### Standard (Pre-trained Models Only)
- `POST /analyze/text` - Text sentiment analysis
- `POST /analyze/audio` - Voice emotion detection
- `POST /analyze/image` - Facial expression recognition
- `POST /aggregate/day` - Daily multi-modal fusion
- `GET /trend/7d` - 7-day trend data
- `DELETE /purge` - Delete all local data

### ✨ Enhanced (Hybrid: Pre-trained + LLM)
- `POST /analyze/text/enhanced` - Text + intelligent insights
- `POST /analyze/audio/enhanced` - Audio + contextual analysis
- `POST /analyze/image/enhanced` - Image + mood interpretation
- `POST /aggregate/day/enhanced` - Comprehensive LLM assessment

## 🛡️ Ethics & Privacy
- **Non-diagnostic**: Educational/research only
- **Privacy-first**: Local processing, optional data deletion
- **Explainable**: Token highlights, emotion breakdown
- **Anonymized**: Synthetic data for demos

## 📊 Tech Stack
- **Backend**: FastAPI, Transformers (Hugging Face), librosa, FER
- **Frontend**: React, Vite, TypeScript, Recharts
- **Models**: RoBERTa (sentiment), Wav2Vec2 (audio emotion), FER (facial expressions)

## 👩‍💻 Author
Aarohi (B.Tech) - Mental Health AI Research Project
