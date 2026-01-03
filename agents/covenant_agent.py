from config.llm import run_llm

def covenant_sentinel_llm(text):
    prompt = f"""Analyze debt covenant risk.

TEXT:
{text}

Return JSON with risk_level, explanation, evidence.
"""
    return run_llm(prompt)
