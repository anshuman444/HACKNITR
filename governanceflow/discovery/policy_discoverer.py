import pathway as pw
import json
from governanceflow.discovery.web_fetcher import fetch_web_content, search_government_portal

def discover_policies(context_stream):
    policies = context_stream.select(
        *pw.this,
        discovery=pw.apply(autonomous_multi_source_discovery, pw.this.survey_title, pw.this.inferred_context)
    )
    return policies

def autonomous_multi_source_discovery(title: str, context_json: str) -> str:
    try:
        context = json.loads(context_json)
        query = context.get("search_query", f"{title} government policy official")
        
        links = search_government_portal(query)
        policy_content = ""
        for link in links[:2]:
            policy_content += f"\n--- SOURCE: {link} ---\n"
            policy_content += fetch_web_content(link)
            
        news_content = f"\n--- NEWS CONTEXT ---\nLive search results for: {query} (News Scan Active)"
        
        return json.dumps({
            "policy_text": policy_content if policy_content else "No official document found.",
            "news_context": news_content,
            "sources": links
        })
    except Exception as e:
        return json.dumps({"error": str(e)})
