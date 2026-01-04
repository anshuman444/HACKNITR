from config.llm import run_llm
import json

class SuperAgent:
    def generate_formal_report(self, title, observed, policy_json, stats_json, comments) -> str:
        prompt = f"Context: {title} Observed: {observed} Policy: {policy_json} Stats: {stats_json} \nGenerate Risk Report JSON."
        return run_llm(prompt)
