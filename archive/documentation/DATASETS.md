# 📊 Datasets Reference Guide

This document lists datasets you can use for **fine-tuning** or **training from scratch** if you want to customize the models beyond the pre-trained versions.

> **Note:** The current implementation uses pre-trained models and **doesn't require any datasets** to work!

---

## 📝 Text Analysis Datasets

### For Sentiment Analysis

| Dataset | Size | Description | Link |
|---------|------|-------------|------|
| **Sentiment140** | 1.6M tweets | Twitter sentiment (positive/negative) | [Kaggle](https://www.kaggle.com/datasets/kazanova/sentiment140) |
| **IMDb Reviews** | 50K reviews | Movie reviews with sentiment labels | [Stanford](https://ai.stanford.edu/~amaas/data/sentiment/) |
| **SST-2** | 70K sentences | Stanford Sentiment Treebank | [Hugging Face](https://huggingface.co/datasets/sst2) |

### For Mental Health Specific

| Dataset | Size | Description | Link |
|---------|------|-------------|------|
| **GoEmotions** | 58K comments | 27 emotion categories from Reddit | [Google](https://github.com/google-research/google-research/tree/master/goemotions) |
| **Mental Health Reddit** | 300K posts | r/depression, r/anxiety, r/mentalhealth | [Kaggle](https://www.kaggle.com/datasets/ruchi798/depression-and-anxiety-reddit-posts) |
| **DAIC-WOZ** | 189 interviews | Depression screening interviews (text transcripts) | [USC](https://dcapswoz.ict.usc.edu/) |
| **Twitter Mental Health** | 10K tweets | Tweets about mental health conditions | [Kaggle](https://www.kaggle.com/datasets/infamouscoder/mental-health-social-media) |
| **CLPsych** | Varies | Clinical psychology shared tasks | [CLPsych.org](http://clpsych.org/) |

---

## 🎤 Audio/Speech Emotion Datasets

| Dataset | Size | Emotions | Speakers | Link |
|---------|------|----------|----------|------|
| **RAVDESS** | 7,356 files | 8 emotions | 24 actors | [Zenodo](https://zenodo.org/record/1188976) |
| **CREMA-D** | 7,442 files | 6 emotions | 91 actors | [GitHub](https://github.com/CheyneyComputerScience/CREMA-D) |
| **TESS** | 2,800 files | 7 emotions | 2 speakers | [Kaggle](https://www.kaggle.com/datasets/ejlok1/toronto-emotional-speech-set-tess) |
| **SAVEE** | 480 files | 7 emotions | 4 speakers (male) | [SAVEE](http://kahlan.eps.surrey.ac.uk/savee/) |
| **EMO-DB** | 535 files | 7 emotions | 10 speakers (German) | [EMO-DB](http://emodb.bilderbar.info/) |
| **IEMOCAP** | 12 hours | 9 emotions | 10 speakers | [USC](https://sail.usc.edu/iemocap/) |

**Emotion Categories (typical):**
- Neutral, Happy, Sad, Angry, Fear, Surprise, Disgust

---

## 📸 Facial Expression Datasets

| Dataset | Size | Emotions | Type | Link |
|---------|------|----------|------|------|
| **FER2013** | 35,887 images | 7 emotions | Grayscale 48x48 | [Kaggle](https://www.kaggle.com/datasets/msambare/fer2013) |
| **AffectNet** | 1M images | 8 emotions + valence/arousal | Real-world photos | [AffectNet](http://mohammadmahoor.com/affectnet/) |
| **CK+** | 593 sequences | 7 emotions | Lab-controlled | [CMU](http://www.consortium.ri.cmu.edu/ckagree/) |
| **RAF-DB** | 30K images | 7 emotions | Real-world (in-the-wild) | [RAF-DB](http://www.whdeng.cn/raf/model1.html) |
| **FER+ (FER2013+)** | 35K images | 8 emotions | Improved FER2013 labels | [GitHub](https://github.com/Microsoft/FERPlus) |
| **JAFFE** | 213 images | 7 emotions | Japanese females | [JAFFE](https://zenodo.org/record/3451524) |

**Standard 7 Emotions:**
- Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral

---

## 🔄 Multi-Modal Datasets

For combined analysis (text + audio + video):

| Dataset | Modalities | Size | Description | Link |
|---------|-----------|------|-------------|------|
| **CMU-MOSEI** | Text, Audio, Video | 23K+ videos | Multi-modal sentiment analysis | [CMU](http://multicomp.cs.cmu.edu/resources/cmu-mosei-dataset/) |
| **DAIC-WOZ** | Text, Audio, Video | 189 interviews | Depression screening interviews | [USC](https://dcapswoz.ict.usc.edu/) |
| **OMG-Emotion** | Text, Audio, Video | 10 hours | One-Minute Gradual-Emotional Behavior | [OMG](https://www2.informatik.uni-hamburg.de/wtm/OMG-EmotionChallenge/) |

---

## 🚀 Quick Start with Datasets

### 1. Download FER2013 (Image Analysis)

```bash
# Install kaggle API
pip install kaggle

# Download FER2013
kaggle datasets download -d msambare/fer2013

# Unzip
unzip fer2013.zip -d data/fer2013/
```

### 2. Download RAVDESS (Audio Analysis)

```bash
# Direct download
wget https://zenodo.org/record/1188976/files/Audio_Speech_Actors_01-24.zip

# Unzip
unzip Audio_Speech_Actors_01-24.zip -d data/ravdess/
```

### 3. Fine-tune Text Model

```python
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

# Load dataset
dataset = load_dataset("emotion")  # GoEmotions subset

# Load pre-trained model
model = AutoModelForSequenceClassification.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
    num_labels=7  # For 7 emotion categories
)

# Fine-tune
training_args = TrainingArguments(
    output_dir="./models/text_finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=16,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"]
)

trainer.train()
```

---

## 📋 Data Preprocessing Examples

### Text Preprocessing

```python
import re

def preprocess_text(text):
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text.strip()
```

### Audio Feature Extraction

```python
import librosa
import numpy as np

def extract_audio_features(audio_path):
    # Load audio
    audio, sr = librosa.load(audio_path, sr=16000)
    
    # Extract features
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
    spectral = librosa.feature.spectral_centroid(y=audio, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(audio)
    
    # Compute statistics
    features = np.concatenate([
        np.mean(mfcc, axis=1),
        np.std(mfcc, axis=1),
        np.mean(chroma, axis=1),
        np.mean(spectral),
        np.mean(zcr)
    ])
    
    return features
```

### Image Preprocessing

```python
import cv2
from PIL import Image

def preprocess_image(image_path, target_size=(48, 48)):
    # Load image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Resize
    resized = cv2.resize(gray, target_size)
    
    # Normalize
    normalized = resized / 255.0
    
    return normalized
```

---

## 🎓 Training Tips

1. **Start with pre-trained models** (current approach) - fastest to deploy
2. **Fine-tune if needed** - when you have domain-specific data
3. **Train from scratch only if** - you have 10K+ labeled samples

**Current Status:** ✅ Using pre-trained models (no datasets needed!)

**Future:** If you collect user data (with consent), you can fine-tune models for better accuracy on your specific use case.

---

## 📚 Additional Resources

- **Papers with Code:** [https://paperswithcode.com/](https://paperswithcode.com/)
- **Hugging Face Datasets:** [https://huggingface.co/datasets](https://huggingface.co/datasets)
- **Kaggle Datasets:** [https://www.kaggle.com/datasets](https://www.kaggle.com/datasets)
- **UCI ML Repository:** [https://archive.ics.uci.edu/ml](https://archive.ics.uci.edu/ml)

---

## ⚖️ Ethical Considerations

When using mental health datasets:
- ✅ Always check licensing and usage rights
- ✅ Anonymize all personal information
- ✅ Follow IRB/ethics board approval if doing research
- ✅ Be transparent about data sources
- ✅ Never use data for diagnostic purposes without clinical validation

---

**Questions?** Check the main README or SETUP_MODELS.md for implementation details!
