"""
LLM Enhancement Service
Uses Groq's Llama 3.1 8B to provide intelligent analysis and recommendations
based on pre-trained model outputs
"""

import os
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    print("Warning: groq not available. Install with: pip install groq")
    GROQ_AVAILABLE = False

# Configuration from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
ENABLE_LLM = os.getenv("ENABLE_LLM_ENHANCEMENT", "true").lower() == "true"

# Initialize Groq client
_groq_client = None


def _get_groq_client():
    """Get or create Groq client"""
    global _groq_client
    
    # Check if LLM enhancement is enabled
    if not ENABLE_LLM:
        print("LLM enhancement is disabled (ENABLE_LLM_ENHANCEMENT=false)")
        return None
    
    if _groq_client is None and GROQ_AVAILABLE:
        if not GROQ_API_KEY:
            print("=" * 60)
            print("⚠️  GROQ_API_KEY not set. LLM enhancement disabled.")
            print("=" * 60)
            print("To enable LLM-enhanced analysis:")
            print("1. Get free API key: https://console.groq.com/keys")
            print("2. Create backend/.env file:")
            print("   GROQ_API_KEY=your_key_here")
            print("3. Restart the server")
            print("=" * 60)
            print("Note: System still works with pre-trained models only!")
            print("=" * 60)
            return None
        
        try:
            # Initialize Groq client (compatible with version 0.4.x)
            _groq_client = Groq(api_key=GROQ_API_KEY)
            print("✅ Groq LLM client initialized successfully")
            print(f"   Using model: {GROQ_MODEL}")
        except TypeError as e:
            # Handle version mismatch - try without extra params
            try:
                import groq
                _groq_client = groq.Client(api_key=GROQ_API_KEY)
                print("✅ Groq LLM client initialized (compatibility mode)")
            except Exception as e2:
                print(f"❌ Failed to initialize Groq client: {e}, {e2}")
                return None
        except Exception as e:
            print(f"❌ Failed to initialize Groq client: {e}")
            return None
    
    return _groq_client


def enhance_text_analysis(text: str, model_result: Dict) -> Dict:
    """
    Enhance text analysis with LLM reasoning
    
    Args:
        text: Original user input
        model_result: Output from pre-trained sentiment model
    
    Returns:
        Enhanced analysis with LLM insights
    """
    client = _get_groq_client()
    
    # If LLM not available, return original result
    if client is None:
        return {
            "enhanced": False,
            "original_result": model_result,
            "note": "LLM enhancement not available"
        }
    
    try:
        # Extract model analysis details safely
        score = model_result.get('score', 0.5)
        sentiment = model_result.get('sentiment', 'neutral')
        themes = model_result.get('themes', [])
        
        # Get explain dict if it exists (from full pipeline)
        explain = model_result.get('explain', {})
        dominant_themes = explain.get('dominant_themes', themes)
        negative_indicators = explain.get('negative_indicators', 0)
        positive_indicators = explain.get('positive_indicators', 0)
        
        # Prepare prompt
        prompt = f"""You are a compassionate mental health support assistant. Analyze the user's text and provide thoughtful, actionable feedback.

**User's Input:**
"{text[:500]}"  

**Sentiment Analysis Results:**
- Stress/Concern Score: {score:.2f} (0.0 = very positive, 1.0 = high concern)
- Overall Sentiment: {sentiment}
- Themes Identified: {', '.join(dominant_themes) if dominant_themes else 'None detected'}
- Negative Indicators: {negative_indicators}
- Positive Indicators: {positive_indicators}

**Your Task:**
Provide a warm, professional response that helps the user understand their emotional state and offers practical support.

**Guidelines:**
1. Be empathetic and non-judgmental
2. Acknowledge their feelings with validation
3. Identify 2-3 specific concerns from their text
4. Provide 3 concrete, actionable suggestions they can implement today
5. Use encouraging but realistic language
6. If the text indicates severe distress, crisis, or self-harm thoughts, set needs_professional_help to true
7. NO EMOJIS - use professional, warm language only

**Response Format (JSON):**
{{
  "risk_level": "Low|Moderate|High",
  "reasoning": "2-3 sentences explaining the risk assessment based on their specific words and themes",
  "supportive_message": "A brief, warm message acknowledging their feelings (1-2 sentences)",
  "key_concerns": ["specific concern 1", "specific concern 2", "specific concern 3"],
  "suggestions": [
    "Immediate action: [specific, practical step they can take in the next hour]",
    "Short-term strategy: [something they can do today or this week]",
    "Long-term support: [ongoing practice or resource to consider]"
  ],
  "needs_professional_help": true|false,
  "professional_help_reason": "Brief explanation if professional help is recommended, empty string otherwise"
}}"""

        # Call Groq API
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        # Parse LLM response
        llm_output = json.loads(response.choices[0].message.content)
        
        # Get bucket safely (may not exist in test data)
        bucket = model_result.get('bucket', 'Moderate')
        
        return {
            "enhanced": True,
            "original_score": model_result.get('score', 0),
            "original_bucket": bucket,
            "llm_feedback": {
                "risk_level": llm_output.get('risk_level', bucket),
                "reasoning": llm_output.get('reasoning', ''),
                "supportive_message": llm_output.get('supportive_message', ''),
                "key_concerns": llm_output.get('key_concerns', []),
                "suggestions": llm_output.get('suggestions', []),
                "needs_professional_help": llm_output.get('needs_professional_help', False),
                "professional_help_reason": llm_output.get('professional_help_reason', '')
            },
            "model_explain": model_result.get('explain', {})
        }
    
    except Exception as e:
        print(f"LLM enhancement failed: {e}")
        return {
            "enhanced": False,
            "original_result": model_result,
            "error": str(e)
        }


def enhance_audio_analysis(audio_result: Dict) -> Dict:
    """
    Enhance audio analysis with LLM reasoning
    
    Args:
        audio_result: Output from pre-trained audio model
    
    Returns:
        Enhanced analysis with LLM insights
    """
    client = _get_groq_client()
    
    if client is None:
        return {
            "enhanced": False,
            "original_result": audio_result
        }
    
    try:
        # Extract audio analysis safely
        score = audio_result.get('score', 0.5)
        explain = audio_result.get('explain', {})
        dominant_emotion = explain.get('dominant_emotion', 'neutral')
        emotion_distribution = explain.get('emotion_distribution', {})
        
        prompt = f"""You are a compassionate mental health assistant analyzing voice patterns.

**Voice Data:**
Dominant Emotion: {dominant_emotion}
Emotion Distribution: {json.dumps(emotion_distribution)}
Stress Level: {score:.2f} (0=calm, 1=stressed)

**Instructions:**
Provide empathetic, practical feedback on voice patterns. NO EMOJIS. Be concise and warm.

**Required JSON Response:**
{{
  "interpretation": "1-2 sentences on what voice suggests about emotional state",
  "concern_level": "Low|Moderate|High",
  "supportive_message": "1 sentence validating their feelings",
  "key_observations": ["observation 1", "observation 2"],
  "suggestions": [
    "Immediate: [emotion regulation technique]",
    "Practice: [breathing or vocal exercise]",
    "Support: [strategy for detected emotion]"
  ],
  "needs_attention": true|false
}}"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400,
            response_format={"type": "json_object"}
        )
        
        llm_output = json.loads(response.choices[0].message.content)
        
        return {
            "enhanced": True,
            "original_score": score,
            "original_emotion": dominant_emotion,
            "llm_feedback": {
                "interpretation": llm_output.get('interpretation', ''),
                "concern_level": llm_output.get('concern_level', ''),
                "supportive_message": llm_output.get('supportive_message', ''),
                "key_observations": llm_output.get('key_observations', []),
                "suggestions": llm_output.get('suggestions', []),
                "needs_attention": llm_output.get('needs_attention', False)
            },
            "emotion_distribution": emotion_distribution
        }
    
    except Exception as e:
        print(f"Audio LLM enhancement failed: {e}")
        return {
            "enhanced": False,
            "original_result": audio_result,
            "error": str(e)
        }


def enhance_image_analysis(image_result: Dict) -> Dict:
    """
    Enhance facial expression analysis with LLM reasoning
    
    Args:
        image_result: Output from FER model
    
    Returns:
        Enhanced analysis with LLM insights
    """
    client = _get_groq_client()
    
    if client is None:
        return {
            "enhanced": False,
            "original_result": image_result
        }
    
    try:
        # Extract image analysis safely
        score = image_result.get('score', 0.5)
        explain = image_result.get('explain', {})
        face_detected = explain.get('face_detected', False)
        dominant_emotion = explain.get('dominant_emotion', 'neutral')
        top_emotions = image_result.get('top_emotions', [])
        
        prompt = f"""You are a compassionate mental health assistant analyzing facial expressions.

**Analysis Data:**
Face Detected: {face_detected}
Dominant Emotion: {dominant_emotion}
Top Emotions: {json.dumps(top_emotions)}
Stress Score: {score:.2f} (0=calm, 1=stressed)

**Instructions:**
Provide empathetic, practical feedback. NO EMOJIS. Be concise and supportive.

**Required JSON Response:**
{{
  "interpretation": "1-2 sentences on what expression suggests about emotional state",
  "concern_level": "Low|Moderate|High",
  "supportive_message": "1 sentence acknowledging their state",
  "key_observations": ["observation 1", "observation 2"],
  "suggestions": [
    "Immediate: [quick technique]",
    "Activity: [mood-shifting activity]",
    "Practice: [wellness strategy]"
  ],
  "needs_attention": true|false
}}"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400,
            response_format={"type": "json_object"}
        )
        
        llm_output = json.loads(response.choices[0].message.content)
        
        return {
            "enhanced": True,
            "original_score": score,
            "dominant_emotion": dominant_emotion,
            "face_detected": face_detected,
            "llm_feedback": {
                "interpretation": llm_output.get('interpretation', ''),
                "concern_level": llm_output.get('concern_level', ''),
                "supportive_message": llm_output.get('supportive_message', ''),
                "key_observations": llm_output.get('key_observations', []),
                "suggestions": llm_output.get('suggestions', []),
                "needs_attention": llm_output.get('needs_attention', False)
            },
            "top_emotions": top_emotions
        }
    
    except Exception as e:
        print(f"Image LLM enhancement failed: {e}")
        return {
            "enhanced": False,
            "original_result": image_result,
            "error": str(e)
        }


def enhance_daily_fusion(fusion_result: Dict, modality_details: Dict) -> Dict:
    """
    Enhance multi-modal fusion with comprehensive LLM analysis
    
    Args:
        fusion_result: Output from fusion module
        modality_details: Individual modality results for context
    
    Returns:
        Enhanced comprehensive assessment
    """
    client = _get_groq_client()
    
    if client is None:
        return {
            "enhanced": False,
            "original_result": fusion_result
        }
    
    try:
        prompt = f"""You are an expert mental health AI. Provide a comprehensive daily assessment.

**Multi-Modal Analysis:**
- Final risk score: {fusion_result['final_score']} (0=good, 1=concerning)
- Risk bucket: {fusion_result['bucket']}
- Text analysis score: {fusion_result['modality_scores'].get('text', 'N/A')}
- Audio analysis score: {fusion_result['modality_scores'].get('audio', 'N/A')}
- Image analysis score: {fusion_result['modality_scores'].get('image', 'N/A')}

Provide a holistic assessment:
1. **Overall Status**: One sentence summary of their mental wellbeing today
2. **Risk Assessment**: Justify the risk level (Low/Moderate/High)
3. **Trend Analysis**: What patterns emerged across modalities?
4. **Top Priority**: The #1 thing they should focus on today
5. **Action Plan**: 3 specific, prioritized actions for today/this week
6. **Professional Help**: Do they need to speak with a therapist? (Yes/No/Maybe)

Be warm, supportive, and actionable. Avoid medical jargon.

Respond in JSON:
{{
  "overall_status": "One sentence summary",
  "risk_level": "Low|Moderate|High",
  "risk_justification": "Why this level?",
  "cross_modal_patterns": "What patterns do you see?",
  "top_priority": "The #1 focus area",
  "action_plan": ["action1", "action2", "action3"],
  "professional_help_needed": "Yes|No|Maybe",
  "professional_help_reason": "Brief explanation",
  "encouraging_message": "Brief positive note"
}}"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600,
            response_format={"type": "json_object"}
        )
        
        llm_output = json.loads(response.choices[0].message.content)
        
        return {
            "enhanced": True,
            "original_fusion": fusion_result,
            "comprehensive_assessment": {
                "overall_status": llm_output.get('overall_status', ''),
                "risk_level": llm_output.get('risk_level', fusion_result['bucket']),
                "risk_justification": llm_output.get('risk_justification', ''),
                "cross_modal_patterns": llm_output.get('cross_modal_patterns', ''),
                "top_priority": llm_output.get('top_priority', ''),
                "action_plan": llm_output.get('action_plan', []),
                "professional_help_needed": llm_output.get('professional_help_needed', 'Maybe'),
                "professional_help_reason": llm_output.get('professional_help_reason', ''),
                "encouraging_message": llm_output.get('encouraging_message', '')
            }
        }
    
    except Exception as e:
        print(f"Fusion LLM enhancement failed: {e}")
        return {
            "enhanced": False,
            "original_result": fusion_result,
            "error": str(e)
        }
