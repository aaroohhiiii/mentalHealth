# 🚀 SETUP & RUN INSTRUCTIONS

## Project Status: ✅ Complete Skeleton with Placeholder Models

All files have been created. The system is ready to run with **placeholder/mock models** that generate deterministic results for demo purposes.

---

## 📁 Project Structure

```
mentalHealth/
├── backend/                      # FastAPI backend
│   ├── app.py                   # Main FastAPI application
│   ├── requirements.txt         # Python dependencies
│   ├── models/                  # Model artifacts (placeholder)
│   │   └── README.md
│   ├── services/                # Business logic
│   │   ├── text_infer.py       # Text analysis (NLP)
│   │   ├── audio_infer.py      # Audio analysis (SER)
│   │   ├── image_infer.py      # Image analysis (FER)
│   │   ├── fusion.py           # Multi-modal fusion
│   │   └── storage.py          # Data persistence
│   └── utils/                   # Explainability utilities
│       ├── explain_text.py
│       ├── explain_audio.py
│       └── explain_image.py
├── frontend/                    # React + Vite frontend
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── components/         # Reusable components
│       │   ├── RiskGauge.tsx
│       │   ├── TrendChart.tsx
│       │   ├── ModalityCard.tsx
│       │   ├── UploadAudio.tsx
│       │   └── UploadImage.tsx
│       └── pages/              # Main pages
│           ├── Dashboard.tsx
│           ├── NewEntry.tsx
│           ├── Trends.tsx
│           └── Privacy.tsx
├── docs/
│   ├── report.md               # Technical report
│   └── demo-script.md          # 2-3 minute demo script
└── README.md                    # Project overview
```

---

## ⚡ Quick Start (2 Terminals)

### Terminal 1: Backend (FastAPI)

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app:app --reload --port 8000
```

**Backend will be available at:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000

---

### Terminal 2: Frontend (React + Vite)

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Frontend will be available at:**
- App: http://localhost:5173

---

## 📊 Testing the System

### 1. Backend API Testing

Visit http://localhost:8000/docs for interactive API documentation.

**Test Endpoints:**

```powershell
# Test text analysis
curl -X POST "http://localhost:8000/analyze/text" -H "Content-Type: application/json" -d "{\"text\": \"Feeling stressed and overwhelmed today\"}"

# Test 7-day trend
curl "http://localhost:8000/trend/7d"

# Test stats
curl "http://localhost:8000/stats"

# Test health
curl "http://localhost:8000"
```

### 2. Frontend Testing

1. **Dashboard Page** - View overall risk assessment and 7-day trend
2. **New Entry Page** - Add text logs, upload audio/images
3. **Trends Page** - View detailed 7-day trend with daily breakdown
4. **Privacy Page** - View data statistics and delete all data

---

## 🔧 Current Implementation Status

### ✅ Completed (Placeholder Logic)

| Component | Status | Details |
|-----------|--------|---------|
| Backend API | ✅ Complete | All 6 endpoints functional |
| Text Analysis | ✅ Placeholder | Keyword-based sentiment |
| Audio Analysis | ✅ Placeholder | Deterministic pseudo-random |
| Image Analysis | ✅ Placeholder | Simulated FER |
| Multi-modal Fusion | ✅ Complete | Late fusion with weights |
| Storage System | ✅ Complete | In-memory storage |
| Frontend UI | ✅ Complete | All 4 pages + components |
| Dashboard | ✅ Complete | Risk gauge + trend chart |
| New Entry | ✅ Complete | Text/audio/image upload |
| Trends | ✅ Complete | 7-day trend visualization |
| Privacy | ✅ Complete | Data control + disclaimers |

### 🔴 Pending (Real Models)

| Component | Status | Next Steps |
|-----------|--------|------------|
| Text NLP Model | 🔴 Pending | Train DistilBERT on mental health data |
| Audio SER Model | 🔴 Pending | Train XGBoost on RAVDESS/CREMA-D |
| Image FER Model | 🔴 Pending | Integrate fer library or MobileNet |
| Explainability | 🔴 Pending | SHAP for text, Grad-CAM for images |
| Model Training Scripts | 🔴 Pending | Create training pipelines |
| Validation Study | 🔴 Pending | Clinical validation on real users |

---

## 📦 Dependencies

### Backend (Python)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
scikit-learn==1.4.0
transformers==4.37.2
torch==2.1.2
librosa==0.10.1
opencv-python==4.9.0.80
fer==22.5.1
shap==0.44.1
```

### Frontend (Node.js)
```
react@18.2.0
react-dom@18.2.0
recharts@2.10.3
axios@1.6.5
vite@5.0.11
typescript@5.3.3
```

---

## 🎯 Demo Instructions

### Recommended Demo Flow (2-3 minutes)

1. **Start Backend & Frontend** (both terminals)
2. **Open Browser** → http://localhost:5173
3. **Show Dashboard** - Explain multi-modal approach
4. **Navigate to New Entry**:
   - Enter text: "Feeling stressed, can't sleep well, worried constantly"
   - Upload a sample audio file (any .wav/.mp3)
   - Upload a sample image (any selfie .jpg/.png)
5. **Show Results** - Highlight explanations (keywords, emotions)
6. **Navigate to Trends** - Show 7-day tracking
7. **Navigate to Privacy** - Emphasize local processing & delete feature
8. **Closing** - Stress non-diagnostic nature

---

## 🔄 Incremental Upgrade Path

### Phase 1: Text Model (Week 1)
```python
# Replace services/text_infer.py with:
from transformers import pipeline

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_text(text):
    result = sentiment_analyzer(text)[0]
    score = result['score'] if result['label'] == 'NEGATIVE' else 1 - result['score']
    # ... rest of logic
```

### Phase 2: Audio Model (Week 2)
```python
# Replace services/audio_infer.py with:
import librosa
import xgboost as xgb

def analyze_audio(audio_bytes):
    audio, sr = sf.read(io.BytesIO(audio_bytes))
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    features = np.mean(mfcc, axis=1)
    
    model = xgb.Booster()
    model.load_model('models/audio_xgb.json')
    emotion_probs = model.predict(features)
    # ... rest of logic
```

### Phase 3: Image Model (Week 3)
```python
# Replace services/image_infer.py with:
from fer import FER
import cv2

detector = FER(mtcnn=True)

def analyze_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image_array = np.array(image)
    result = detector.detect_emotions(image_array)
    
    if result:
        emotions = result[0]['emotions']
        # ... rest of logic
```

---

## 🛠️ Troubleshooting

### Issue: Backend won't start
**Solution:**
```powershell
# Check Python version (3.9+ required)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check port 8000 is free
netstat -ano | findstr :8000
```

### Issue: Frontend won't start
**Solution:**
```powershell
# Check Node version (16+ required)
node --version

# Clear cache and reinstall
rm -r node_modules
rm package-lock.json
npm install

# Check port 5173 is free
netstat -ano | findstr :5173
```

### Issue: CORS errors
**Solution:**
- Backend `app.py` already has CORS configured for `localhost:5173`
- If using different port, update `allow_origins` in `app.py`

### Issue: TypeScript errors in VS Code
**Solution:**
- Errors will disappear after `npm install`
- If persisting, restart VS Code: `Ctrl+Shift+P` → "Reload Window"

---

## 📝 Next Steps After Setup

### Immediate (Demo Ready)
✅ System is fully functional with placeholder models  
✅ Can demonstrate all features end-to-end  
✅ Ready for 2-3 minute presentation  

### Short-Term (1-2 Weeks)
- [ ] Replace text analysis with DistilBERT
- [ ] Integrate librosa for audio feature extraction
- [ ] Add fer library for facial expression recognition
- [ ] Implement SHAP-based text explainability
- [ ] Create model training scripts

### Medium-Term (1-2 Months)
- [ ] Conduct user testing (10-20 participants)
- [ ] Validate against clinical assessments
- [ ] Add data export functionality
- [ ] Build mobile app (React Native)
- [ ] Explore wearable integration

### Long-Term (3-6 Months)
- [ ] Clinical validation study (IRB approval)
- [ ] Multi-cultural dataset validation
- [ ] Regulatory pathway exploration (CE/FDA)
- [ ] Partnership with mental health organizations

---

## 🎓 Academic Submission Checklist

- [x] Working prototype (FastAPI + React)
- [x] Technical report (`docs/report.md`)
- [x] Demo script (`docs/demo-script.md`)
- [x] README with instructions
- [x] Ethics & privacy considerations
- [x] Explainability features
- [x] Non-diagnostic disclaimers
- [ ] Video demo recording (TODO)
- [ ] GitHub repository setup (TODO)
- [ ] Presentation slides (TODO)

---

## 📞 Support & Contact

**Developer:** Aarohi (B.Tech)  
**Project:** Mental Health AI Multi-Modal System  
**Repository:** (To be added after GitHub setup)  

For questions or issues:
1. Check troubleshooting section above
2. Review API docs at http://localhost:8000/docs
3. Check browser console for frontend errors
4. Verify both backend and frontend are running

---

## 🎉 Success Indicators

You'll know everything is working when:

✅ Backend shows: `INFO: Uvicorn running on http://0.0.0.0:8000`  
✅ Frontend shows: `Local: http://localhost:5173/`  
✅ Browser loads the dashboard without errors  
✅ Text submission returns risk score + explanations  
✅ Audio/image uploads work (even without real files)  
✅ Trend chart displays 7-day data  
✅ Privacy page shows data statistics  

---

**Last Updated:** November 2, 2025  
**Version:** 1.0 (Placeholder Models)  
**Status:** ✅ Ready for Demo
