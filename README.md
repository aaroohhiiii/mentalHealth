# Mental Health Multi-Modal AI System

## 🎯 Overview
Early detection system for stress/depression using:
- **Text**: Daily logs analysis (NLP)
- **Audio**: 5-10s voice check-ins (SER)
- **Images**: 4-5 selfies/day (FER)

## ⚡ Quick Start

### Backend (FastAPI)
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Frontend (React + Vite)
```powershell
cd frontend
npm install
npm run dev
```

## 🔗 Endpoints
- `POST /analyze/text` - Analyze text sentiment
- `POST /analyze/audio` - Analyze voice emotions
- `POST /analyze/image` - Analyze facial expressions
- `POST /aggregate/day` - Daily multi-modal fusion
- `GET /trend/7d` - 7-day trend data
- `DELETE /purge` - Delete all local data

## 🛡️ Ethics & Privacy
- **Non-diagnostic**: Educational/research only
- **Privacy-first**: Local processing, optional data deletion
- **Explainable**: Token highlights, emotion breakdown
- **Anonymized**: Synthetic data for demos

## 📊 Tech Stack
- **Backend**: FastAPI, scikit-learn, librosa, OpenCV
- **Frontend**: React, Vite, TypeScript, Recharts
- **Models**: DistilBERT, XGBoost, FER/MobileNet

## 👩‍💻 Author
Aarohi (B.Tech) - Mental Health AI Research Project
