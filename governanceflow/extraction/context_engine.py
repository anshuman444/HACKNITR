import pathway as pw
from config.llm import run_llm

def infer_survey_context(survey_stream):
    """
    Uses LLM to infer the sector, location, and key objective of the survey.
    """
    context = survey_stream.groupby(pw.this.survey_title).reduce(
        survey_title=pw.this.survey_title,
        inferred_context=pw.apply(llm_context_inference, pw.this.survey_title)
    )
    return context

def llm_context_inference(title: str) -> str:
    """
    Calls LLM to determine survey parameters.
    """
    prompt = f"""
    Analyze this survey title: "{title}"
    Identify:
    1. Sector (e.g., Sanitation, Health, Education)
    2. Primary KPI (e.g., Toilet construction, Vaccine coverage)
    3. Optimal Search Query for government policies.
    
    Return JSON only:
    {{
      "sector": "string",
      "kpi": "string",
      "search_query": "string"
    }}
    """
    return run_llm(prompt)
