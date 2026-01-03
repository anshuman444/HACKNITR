from config.llm import run_llm

def llm_litigation_delta(old_text, new_text):
    prompt = f"""Compare legal risk changes.

OLD:
{old_text}

NEW:
{new_text}

Return JSON with risk_level, explanation, evidence.
"""
    return run_llm(prompt)
