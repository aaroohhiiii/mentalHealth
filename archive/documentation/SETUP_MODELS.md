# 🚀 Setup Instructions with Pre-trained Models

## ✅ What's New: Real AI Models (No Datasets Needed!)

Your mental health app now uses **production-ready pre-trained models**:

| Modality | Model | Source | Size |
|----------|-------|--------|------|
| **Text** | RoBERTa Sentiment | Hugging Face (cardiffnlp) | ~500MB |
| **Audio** | Wav2Vec2 Emotion | Hugging Face (ehcalabres) | ~1.2GB |
| **Image** | FER + MTCNN | FER2013 Dataset | ~100MB |

**Total download size: ~1.8GB** (one-time download, cached locally)

---

## 🛠️ Installation Steps

### 1. Install Python Dependencies

```bash
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Install all dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected install time:** 5-10 minutes (downloads models on first use)

### 2. Download Pre-trained Models (Optional but Recommended)

```bash
# Pre-download models to avoid delays during first API calls
python download_models.py
```

This will download:
- ✅ Text sentiment model (~500MB)
- ✅ Audio emotion model (~1.2GB)
- ✅ Facial expression model (~100MB)

**First-time download:** ~5-10 minutes (depending on internet speed)  
**Subsequent runs:** Instant (models are cached)

### 3. Start the Backend

```bash
uvicorn app:app --reload --port 8000
```

Server will be available at: http://localhost:8000

---

## 🎨 Frontend Setup (Unchanged)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## 📊 How It Works

### Text Analysis
- **Model:** `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **What it does:** Analyzes sentiment (positive/negative/neutral) from text
- **Fallback:** If model fails to load, uses keyword matching
- **Example:**
  ```python
  Input: "Feeling stressed and overwhelmed today"
  Output: Negative sentiment (score: 0.72, High risk)
  ```

### Audio Analysis
- **Model:** `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition`
- **What it does:** Detects emotions from voice recordings
- **Features extracted:** MFCC, spectral centroid, zero-crossing rate, energy
- **Supported formats:** WAV, MP3, OGG, FLAC
- **Fallback:** If model fails, uses deterministic placeholder
- **Example:**
  ```python
  Input: 5-second voice recording
  Output: Sad (65%), Neutral (25%), Anxious (10%) → High risk
  ```

### Image Analysis
- **Model:** `FER` library with MTCNN face detection
- **What it does:** Recognizes 7 facial emotions from selfies
- **Emotions:** angry, disgust, fear, happy, sad, surprise, neutral
- **Face detection:** MTCNN (Multi-task Cascaded Convolutional Networks)
- **Fallback:** If model fails, uses deterministic placeholder
- **Example:**
  ```python
  Input: Selfie image
  Output: Sad (40%), Neutral (35%), Angry (15%) → Moderate risk
  ```

---

## 🔧 Troubleshooting

### Issue: Models take too long to load
**Solution:** Run `python download_models.py` before starting the server

### Issue: `transformers` or `torch` not found
**Solution:** 
```bash
pip install transformers==4.37.2 torch==2.1.2
```

### Issue: `fer` or `cv2` import errors
**Solution:**
```bash
pip install fer==22.5.1 opencv-python==4.9.0.80 mtcnn==0.1.1
```

### Issue: Out of memory
**Solution:** Models use ~2GB RAM. Close other applications or use CPU-only mode (already default)

### Issue: Models still using fallback
**Check:** Look for warning messages in terminal. Install missing dependencies if needed.

---

## 💾 Model Storage Location

Models are cached in:
- **Linux/macOS:** `~/.cache/huggingface/` and `~/.keras/`
- **Windows:** `%USERPROFILE%\.cache\huggingface\` and `%USERPROFILE%\.keras\`

To clear cache (if needed):
```bash
# Linux/macOS
rm -rf ~/.cache/huggingface
rm -rf ~/.keras

# Windows
rmdir /s %USERPROFILE%\.cache\huggingface
rmdir /s %USERPROFILE%\.keras
```

---

## 🚀 Performance Notes

| Operation | Time (CPU) | Time (GPU) |
|-----------|-----------|-----------|
| Text analysis | ~100ms | ~50ms |
| Audio analysis | ~500ms | ~200ms |
| Image analysis | ~300ms | ~150ms |
| Daily fusion | ~10ms | ~10ms |

**Recommended:** Use CPU mode for development, GPU for production with high traffic

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Run `python download_models.py`
3. ✅ Start backend: `uvicorn app:app --reload`
4. ✅ Start frontend: `npm run dev`
5. ✅ Test with sample text/audio/image

**Need datasets for custom training?** See `DATASETS.md` for recommended sources.

---

## 📝 System Requirements

- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** 5GB free space (for models)
- **Internet:** Required for initial model download
- **OS:** macOS, Linux, or Windows

---

## 🆘 Still Having Issues?

Check the logs in terminal for specific error messages. Most issues are related to:
1. Missing dependencies → Run `pip install -r requirements.txt` again
2. Network issues → Check internet connection for model downloads
3. Python version → Use Python 3.8+

The system will **automatically fall back** to simpler methods if models fail to load, so the app will always work!
