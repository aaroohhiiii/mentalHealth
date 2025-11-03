# Demo Script - Mental Health AI System

**Duration:** 2-3 minutes  
**Presenter:** Aarohi (B.Tech)  
**Audience:** Technical reviewers, potential users, academic panel

---

## Opening (10 seconds)

> "Hello! I'm Aarohi, and I've built a **privacy-first, explainable AI system** for early detection of mental health concerns using **text, audio, and facial expression analysis**."

---

## Demo Flow (2 minutes)

### 1. Problem Statement (15 seconds)
> "Mental health issues like stress and depression often go undetected until they become severe. Current screening methods are:
> - **Infrequent** (annual check-ups only)
> - **Subjective** (self-report questionnaires)
> - **Privacy-invasive** (centralized data collection)
> 
> My solution provides **daily, multi-modal monitoring** that's **local, explainable, and non-diagnostic**."

### 2. System Overview (20 seconds)
**[Show Dashboard Page]**

> "The system analyzes three modalities:
> 1. **Text** - Daily journal entries for sentiment analysis
> 2. **Audio** - Voice check-ins for emotional tone detection
> 3. **Images** - Selfies for facial expression recognition
> 
> All data is processed **locally** with **explainable results**."

### 3. New Entry Demo (45 seconds)

**[Navigate to New Entry Page]**

#### 3A. Text Entry (15 seconds)
> "Let's start with a text entry. I'll type: *'Feeling overwhelmed and stressed today. Can't sleep well, constantly worried about deadlines.'*"

**[Type and submit]**

> "The system highlights **negative keywords** like 'overwhelmed' and 'stressed', identifies themes like **sleep issues** and **anxiety**, and provides a **risk score**."

**[Show text analysis result]**

#### 3B. Audio Upload (15 seconds)
> "Next, I'll upload a voice recording. The system extracts **vocal features** like pitch, energy, and speech rate to detect emotions."

**[Upload sample audio file]**

> "It identifies the dominant emotion as **sad** with moderate confidence, contributing to an elevated risk score."

**[Show audio analysis result]**

#### 3C. Image Upload (15 seconds)
> "Finally, I'll upload a selfie. Facial expression analysis detects emotions like happy, sad, or anxious."

**[Upload sample image]**

> "The system detects a **neutral** expression with some signs of fatigue, which is aggregated with other daily inputs."

**[Show image analysis result]**

### 4. Fusion & Trend Analysis (20 seconds)

**[Navigate to Dashboard]**

> "The system combines all three modalities using **late fusion** with configurable weights:
> - Text: 50% (most reliable self-report)
> - Audio: 25%
> - Image: 25%
> 
> The **7-day trend chart** shows risk scores over time, helping users and clinicians spot patterns early."

**[Show trend chart]**

### 5. Explainability (15 seconds)

> "Transparency is critical. Each prediction includes:
> - **Token highlights** for text (which words influenced the score)
> - **Emotion distribution** for audio (which emotions were detected)
> - **Top facial expressions** for images
> 
> This builds trust and helps users understand the 'why' behind each assessment."

### 6. Privacy & Ethics (20 seconds)

**[Navigate to Privacy Page]**

> "Privacy is paramount:
> - ✅ **Local processing** - No cloud uploads
> - ✅ **In-memory storage** - Data cleared on restart
> - ✅ **Delete anytime** - Full user control
> - ✅ **Non-diagnostic** - Clear disclaimers that this is NOT a medical device
> 
> Users can see exactly what data is stored and delete everything with one click."

**[Show privacy controls]**

---

## Closing (15 seconds)

> "In summary, this system provides:
> 1. **Early detection** through daily multi-modal monitoring
> 2. **Explainability** with token/emotion highlights
> 3. **Privacy** through local processing
> 4. **Ethics** with non-diagnostic disclaimers
> 
> **This is not a replacement for professional care** - it's a tool to help people and clinicians catch warning signs early.
> 
> Thank you! I'm happy to answer questions."

---

## Q&A Preparation

### Expected Questions & Answers

**Q: How accurate are the models?**
> "Currently using placeholder models for demo purposes. Real implementation will use:
> - DistilBERT for text (90%+ accuracy on sentiment)
> - XGBoost on librosa features for audio (75-80% on RAVDESS)
> - FER2013 model for facial expressions (65-70% accuracy)
> 
> Multi-modal fusion typically improves accuracy by 5-10%."

**Q: What about false positives?**
> "Great question. I'm prioritizing **high recall** (catch most cases) with moderate precision. False positives are better than false negatives in mental health. The system provides explanations so users can contextualize results."

**Q: Is this medically validated?**
> "No, this is a research prototype. Clinical validation would require:
> - IRB approval
> - Longitudinal study with clinical assessments
> - Diverse demographic testing
> 
> Currently positioned as an educational tool, not a medical device."

**Q: How do you handle cultural differences in emotion expression?**
> "Excellent point. Emotion expression varies across cultures. Future work includes:
> - Multi-cultural training datasets
> - User-calibrated baselines
> - Cultural sensitivity testing
> 
> For now, disclaimers acknowledge this limitation."

**Q: What's the tech stack?**
> "Backend: FastAPI (Python), scikit-learn, librosa, OpenCV
> Frontend: React, Vite, TypeScript, Recharts
> Models: DistilBERT (text), XGBoost (audio), FER/MobileNet (images)
> Deployment: Local-first, CPU-friendly"

**Q: Can this scale to multiple users?**
> "Current version is single-user. Multi-user scaling would add:
> - User authentication (JWT)
> - Database (PostgreSQL with encryption)
> - Redis caching for model inference
> - Docker containerization
> 
> Architecture supports this, but privacy-first means avoiding centralized data."

**Q: What about integration with wearables?**
> "Great future direction! Could integrate:
> - Heart rate variability (stress indicator)
> - Sleep quality (from smartwatches)
> - Activity levels (exercise impact on mood)
> 
> Would enhance multi-modal fusion."

---

## Demo Tips

✅ **Do:**
- Speak clearly and confidently
- Show enthusiasm for privacy/ethics
- Emphasize **non-diagnostic** nature
- Highlight **explainability** features
- Keep under 3 minutes

❌ **Don't:**
- Make medical claims
- Overstate accuracy (placeholder models)
- Skip privacy/disclaimer sections
- Rush through explanations
- Forget to show trend chart

---

## Backup Slides (If Needed)

### Slide 1: Architecture Diagram
```
[Frontend] ↔ REST API ↔ [Backend]
                         ↓
              [Text] [Audio] [Image]
                         ↓
                     [Fusion]
                         ↓
                    [Storage]
```

### Slide 2: Metrics (Placeholder)
- Text Accuracy: 85% (simulated)
- Audio Accuracy: 78% (simulated)
- Image Accuracy: 72% (simulated)
- Fusion Accuracy: 82% (simulated)

### Slide 3: Ethical Guidelines
- ✅ Transparency
- ✅ User Control
- ✅ Privacy-First
- ✅ Non-Diagnostic
- ✅ Inclusive Design

---

**Script Version:** 1.0  
**Last Updated:** November 2, 2025  
**Presenter:** Aarohi (B.Tech)
