import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

USE_MOCK = False   # ✅ Switched to real Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️ GEMINI_API_KEY not found in environment. Falling back to mock.")
    USE_MOCK = True

import time
import random

def run_llm(prompt: str, temperature: float = 0, max_retries: int = 10):
    if USE_MOCK:
        return json.dumps({
            "agent": "mock_llm",
            "risk_level": "MEDIUM",
            "explanation": "Mock response – system wiring is correct.",
            "evidence": "This output confirms all components are connected."
        }, indent=2)

    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel("gemini-flash-latest") 
            response = model.generate_content(
                prompt + "\n\nIMPORTANT: Return valid JSON ONLY with fields: risk_level (HIGH/MEDIUM/LOW), explanation, and evidence.",
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    response_mime_type="application/json"
                )
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower():
                # For Free Tier, we need substantial cooling time
                # Exponential backoff + fixed 30s base
                wait_time = (2 ** (attempt // 2)) + random.random() + 30 
                print(f"⏳ API Quota reached (429). Cooling down for {wait_time:.1f}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
                continue
            
            print(f"❌ Gemini Error: {e}")
            return json.dumps({
                "error": str(e),
                "status": "FAILED"
            })
    
    return json.dumps({
        "error": "Max retries exceeded for Gemini API. The Free Tier is currently too saturated. Please try again in 1-2 minutes.",
        "status": "FAILED"
    })
