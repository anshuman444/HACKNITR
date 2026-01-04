import pathway as pw
from config.llm import run_llm
import json

def parse_policies(policy_stream):
    parsed = policy_stream.select(
        *pw.this,
        policy_targets=pw.apply(extract_policy_metadata, pw.this.discovery)
    )
    return parsed

def extract_policy_metadata(discovery_json: str) -> str:
    data = json.loads(discovery_json)
    content = data.get("policy_text", "")
    news = data.get("news_context", "")
    prompt = f"Analyze these sources and extract targets: {content} {news} \nOutput JSON with policy_name and target_metric."
    return run_llm(prompt)
