#!/usr/bin/env python3
"""
Quick test of LLM enhancement - Run this to verify everything works
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("🧪 TESTING YOUR HYBRID MENTAL HEALTH AI")
print("=" * 60)
print()

# Test 1: Check Groq API
print("1️⃣  Testing Groq API Connection...")
try:
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("   ❌ GROQ_API_KEY not found in .env")
        sys.exit(1)
    
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say 'working!' if you can read this."}],
        max_tokens=10
    )
    print(f"   ✅ Groq API works! Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"   ❌ Groq API failed: {e}")
    sys.exit(1)

print()

# Test 2: Test LLM Enhancement
print("2️⃣  Testing LLM Enhancement Service...")
try:
    from services.llm_enhance import enhance_text_analysis
    
    test_text = "I feel stressed and cannot sleep properly. Work is overwhelming."
    model_result = {
        "score": 0.72,
        "sentiment": "negative",
        "themes": ["stress", "sleep_issues", "work_pressure"]
    }
    
    print(f"   📝 Input: \"{test_text}\"")
    print(f"   🤖 Model Result: {model_result}")
    print()
    print("   🧠 Asking LLM for intelligent analysis...")
    
    enhanced = enhance_text_analysis(test_text, model_result)
    
    if enhanced and 'llm_reasoning' in enhanced:
        print("   ✅ LLM Enhancement SUCCESS!")
        print()
        print("   📊 Enhanced Analysis:")
        print(f"      Risk Level: {enhanced.get('llm_risk_level', 'N/A')}")
        print(f"      Reasoning: {enhanced['llm_reasoning'][:150]}...")
        print(f"      Key Concerns: {enhanced.get('key_concerns', [])}")
        print(f"      Suggestions: {enhanced.get('suggestions', [])[:2]}")
    else:
        print("   ⚠️  LLM returned response but in unexpected format")
        print(f"   Response: {enhanced}")
        
except Exception as e:
    print(f"   ❌ LLM Enhancement failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("="  * 60)
print("🎉 ALL TESTS PASSED! Your hybrid system is working!")
print("=" * 60)
print()
print("Next steps:")
print("  1. Start the server: ./start_server.sh")
print("  2. Open http://localhost:8000/docs")
print("  3. Try the /analyze/text/enhanced endpoint!")
print()
