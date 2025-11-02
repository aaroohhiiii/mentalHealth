"""
Audio Analysis Service
Analyzes vocal emotions from audio files using Speech Emotion Recognition (SER)
Uses librosa for feature extraction and pre-trained models
"""

import io
import random
from typing import Dict
import numpy as np
import tempfile
import os

try:
    import librosa
    import soundfile as sf
    LIBROSA_AVAILABLE = True
except ImportError:
    print("Warning: librosa not available, using fallback audio analysis")
    LIBROSA_AVAILABLE = False

try:
    from transformers import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
    _audio_model = None
except ImportError:
    print("Warning: transformers not available for audio")
    TRANSFORMERS_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    print("Warning: pydub not available for webm conversion")
    PYDUB_AVAILABLE = False


# Emotion categories for SER
EMOTIONS = ['neutral', 'happy', 'sad', 'angry', 'fear', 'surprise']

# Map emotions to stress levels
EMOTION_STRESS_MAP = {
    'neutral': 0.3,
    'happy': 0.1,
    'sad': 0.7,
    'angry': 0.8,
    'fear': 0.85,
    'surprise': 0.4
}


def _load_audio_model():
    """Load pre-trained audio emotion recognition model"""
    global _audio_model
    
    if _audio_model is None and TRANSFORMERS_AVAILABLE:
        try:
            print("Loading audio emotion recognition model (first time only)...")
            # Use Wav2Vec2 for emotion recognition
            _audio_model = pipeline(
                "audio-classification",
                model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
                device=-1  # CPU
            )
            print("✓ Audio emotion model loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load audio model: {e}")
            _audio_model = "fallback"
    
    return _audio_model


def _convert_webm_to_wav(audio_bytes: bytes) -> bytes:
    """Convert webm audio to wav format using pydub"""
    if not PYDUB_AVAILABLE:
        raise Exception("pydub not available for webm conversion")
    
    # Validate input
    if not audio_bytes or len(audio_bytes) == 0:
        raise ValueError("Empty audio data")
    
    # Check if it's actually a valid WebM file (should start with 0x1A 0x45 0xDF 0xA3)
    if len(audio_bytes) < 4:
        raise ValueError(f"Audio data too short: {len(audio_bytes)} bytes")
    
    # Log first few bytes for debugging
    header_bytes = ' '.join(f'{b:02x}' for b in audio_bytes[:8])
    print(f"Audio file header: {header_bytes}")
    
    temp_webm_path = None
    temp_wav_path = None
    
    try:
        # Save webm to temp file
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_webm:
            temp_webm.write(audio_bytes)
            temp_webm_path = temp_webm.name
        
        print(f"Saved WebM to: {temp_webm_path} ({len(audio_bytes)} bytes)")
        
        # Convert to wav using pydub (will use ffmpeg internally)
        # Try to explicitly set frame rate to 16kHz for Wav2Vec2
        audio = AudioSegment.from_file(temp_webm_path, format="webm")
        
        # Resample to 16kHz mono if needed
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        
        print(f"Audio loaded: {len(audio)}ms, {audio.frame_rate}Hz, {audio.channels} channel(s)")
        
        # Export as wav to temp file
        temp_wav_path = tempfile.mktemp(suffix='.wav')
        audio.export(
            temp_wav_path, 
            format="wav",
            parameters=["-ar", "16000", "-ac", "1"]  # 16kHz, mono
        )
        
        print(f"Exported WAV to: {temp_wav_path}")
        
        # Read wav bytes
        with open(temp_wav_path, 'rb') as f:
            wav_bytes = f.read()
        
        print(f"✓ Conversion successful: {len(wav_bytes)} bytes WAV")
        
        return wav_bytes
        
    except Exception as e:
        print(f"Error converting webm: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        # Cleanup temp files
        if temp_webm_path and os.path.exists(temp_webm_path):
            try:
                os.unlink(temp_webm_path)
            except:
                pass
        if temp_wav_path and os.path.exists(temp_wav_path):
            try:
                os.unlink(temp_wav_path)
            except:
                pass


def analyze_audio(audio_bytes: bytes, filename: str) -> Dict:
    """
    Analyze audio for vocal emotion and stress indicators using pre-trained models
    
    Args:
        audio_bytes: Raw audio file bytes
        filename: Original filename
    
    Returns:
        {
            'score': float (0-1, higher = more concerning),
            'bucket': str ('Low', 'Moderate', 'High'),
            'explain': {
                'dominant_emotion': str,
                'emotion_distribution': Dict[str, float],
                'vocal_features': Dict[str, float],
                'salient_frames': List[int]
            }
        }
    """
    
    # If libraries not available, use fallback
    if not LIBROSA_AVAILABLE or not TRANSFORMERS_AVAILABLE:
        return _analyze_audio_fallback(audio_bytes, filename)
    
    # Convert webm to wav if needed
    if filename.lower().endswith('.webm'):
        try:
            print(f"Converting webm to wav: {filename}")
            audio_bytes = _convert_webm_to_wav(audio_bytes)
            print("✓ Conversion successful")
        except Exception as e:
            print(f"Warning: webm conversion failed: {e}")
            return _analyze_audio_fallback(audio_bytes, filename)
    
    # Load model
    model = _load_audio_model()
    if model == "fallback" or model is None:
        return _analyze_audio_fallback(audio_bytes, filename)
    
    try:
        # Load and resample audio
        audio, sr = sf.read(io.BytesIO(audio_bytes))
        
        # Convert to mono if stereo
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        
        # Resample to 16kHz (required by model)
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        
        # Run emotion recognition
        results = model(audio)
        
        # Convert to our emotion format
        emotions_prob = {}
        for result in results:
            emotion = result['label'].lower()
            score = result['score']
            emotions_prob[emotion] = round(score, 3)
        
        # Get dominant emotion
        dominant_emotion = max(emotions_prob.items(), key=lambda x: x[1])[0]
        
        # Map to our stress scoring
        stress_contribution = 0
        for emotion, prob in emotions_prob.items():
            # Map model emotions to stress levels
            if 'sad' in emotion or 'angry' in emotion or 'fear' in emotion:
                stress_contribution += prob * 0.75
            elif 'happy' in emotion or 'calm' in emotion:
                stress_contribution += prob * 0.15
            else:
                stress_contribution += prob * 0.4
        
        score = round(min(1.0, max(0.0, stress_contribution)), 3)
        
    except Exception as e:
        print(f"Error in audio analysis: {e}, using fallback")
        return _analyze_audio_fallback(audio_bytes, filename)
    
    # Extract vocal features with librosa
    try:
        audio_for_features, sr_features = sf.read(io.BytesIO(audio_bytes))
        if len(audio_for_features.shape) > 1:
            audio_for_features = np.mean(audio_for_features, axis=1)
        
        # Extract acoustic features
        mfcc = librosa.feature.mfcc(y=audio_for_features, sr=sr_features, n_mfcc=13)
        spectral_centroid = librosa.feature.spectral_centroid(y=audio_for_features, sr=sr_features)
        zcr = librosa.feature.zero_crossing_rate(audio_for_features)
        energy = librosa.feature.rms(y=audio_for_features)
        
        vocal_features = {
            "mean_pitch": round(float(np.mean(mfcc[0])) * 10 + 150, 2),  # Approximation
            "pitch_variance": round(float(np.std(mfcc[0])) * 10, 2),
            "energy": round(float(np.mean(energy)), 3),
            "zero_crossing_rate": round(float(np.mean(zcr)), 3),
            "spectral_centroid": round(float(np.mean(spectral_centroid)), 2)
        }
    except Exception as e:
        print(f"Could not extract vocal features: {e}")
        vocal_features = {"note": "Feature extraction failed"}
    
    # Categorize
    if score < 0.33:
        bucket = "Low"
    elif score < 0.66:
        bucket = "Moderate"
    else:
        bucket = "High"
    
    return {
        "score": score,
        "bucket": bucket,
        "explain": {
            "dominant_emotion": dominant_emotion,
            "emotion_distribution": emotions_prob,
            "vocal_features": vocal_features,
            "confidence": round(emotions_prob[dominant_emotion], 3),
            "model": "Wav2Vec2 (pre-trained)"
        }
    }


# ===== Fallback: Placeholder Analysis =====
def _analyze_audio_fallback(audio_bytes: bytes, filename: str) -> Dict:
    """
    Fallback placeholder audio analysis if models fail to load
    """
    filename_hash = sum(ord(c) for c in filename)
    random.seed(filename_hash)
    
    # Simulate emotion detection
    emotions_prob = {}
    total = 0
    for emotion in EMOTIONS:
        prob = random.random()
        emotions_prob[emotion] = round(prob, 3)
        total += prob
    
    # Normalize probabilities
    for emotion in emotions_prob:
        emotions_prob[emotion] = round(emotions_prob[emotion] / total, 3)
    
    # Get dominant emotion
    dominant_emotion = max(emotions_prob.items(), key=lambda x: x[1])[0]
    
    # Calculate stress score based on emotion
    base_score = EMOTION_STRESS_MAP.get(dominant_emotion, 0.5)
    
    # Add some variance based on emotion distribution
    stress_contribution = sum(
        emotions_prob[e] * EMOTION_STRESS_MAP[e] 
        for e in emotions_prob
    )
    
    score = round((base_score * 0.6 + stress_contribution * 0.4), 3)
    
    # Categorize
    if score < 0.33:
        bucket = "Low"
    elif score < 0.66:
        bucket = "Moderate"
    else:
        bucket = "High"
    
    # Simulate vocal features (would come from librosa)
    vocal_features = {
        "mean_pitch": round(random.uniform(80, 250), 2),  # Hz
        "pitch_variance": round(random.uniform(10, 50), 2),
        "energy": round(random.uniform(0.3, 0.9), 2),
        "speech_rate": round(random.uniform(2, 5), 2),  # words/sec
        "zero_crossing_rate": round(random.uniform(0.1, 0.4), 2)
    }
    
    # Simulate salient frames (high emotion intensity)
    num_frames = random.randint(50, 100)
    salient_frames = sorted(random.sample(range(num_frames), k=min(5, num_frames)))
    
    return {
        "score": score,
        "bucket": bucket,
        "explain": {
            "dominant_emotion": dominant_emotion,
            "emotion_distribution": emotions_prob,
            "vocal_features": vocal_features,
            "salient_frames": salient_frames,
            "confidence": round(emotions_prob[dominant_emotion], 3),
            "note": "Placeholder analysis - install librosa for real features"
        }
    }
