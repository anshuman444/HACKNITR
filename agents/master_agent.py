import json
from config.llm import run_llm

def run_master_analysis(old_text, new_text):
    """
    Runs a consolidated analysis combining Litigation, Covenant, and Verification agents.
    Returns a structured dictionary with all results.
    """
    prompt = f"""You are an M&A Due Diligence Master Agent. Analyze the provided texts for:
1. LITIGATION RISKS: Compare legal risk changes between OLD and NEW text.
2. COVENANT RISKS: Analyze debt covenant risk in the NEW text.
3. VERIFICATION: Verify if the analysis is consistent with the provided source text.

OLD TEXT:
{old_text}

NEW TEXT:
{new_text}

IMPORTANT: You must return valid JSON ONLY.
Expected JSON Structure:
{{
  "litigation": {{
    "risk_level": "HIGH/MEDIUM/LOW",
    "explanation": "concise explanation",
    "evidence": "evidence from text"
  }},
  "covenant": {{
    "risk_level": "HIGH/MEDIUM/LOW",
    "explanation": "concise explanation",
    "evidence": "evidence from text"
  }},
  "verifier": {{
    "verdict": "VERIFIED/DISCREPANCY",
    "explanation": "reasoning for verdict"
  }}
}}
"""
    response_text = run_llm(prompt)
    
    try:
        # Clean response text in case of markdown blocks
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        return data
    except Exception as e:
        print(f"❌ Master Agent Parsing Error: {e}")
        return {
            "error": "Failed to parse Master Agent response",
            "raw_response": response_text
        }
