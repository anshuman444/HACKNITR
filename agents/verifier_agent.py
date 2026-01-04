from config.llm import run_llm

def verify_agent(analysis, source):
    prompt = f"""Verify analysis against source.

ANALYSIS:
{analysis}

SOURCE:
{source}

Return JSON verdict and explanation.
"""
    return run_llm(prompt)
