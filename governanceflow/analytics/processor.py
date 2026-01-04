import os
import json
import pandas as pd
from governanceflow.agents.super_agent import SuperAgent

def run_batch_analytics(title, files_data):
    """
    Synchronous batch processor for GovernanceFlow.
    Reliable and immediate for Streamlit UI.
    """
    agent = SuperAgent()
    results = []
    
    # Simple aggregation logic for batch
    all_comments = []
    total_quality = 0
    count = 0
    
    all_debug_info = []

    for filename, content in files_data.items():
        try:
            # Flexible CSV Loading - Normalize headers
            df = pd.read_csv(content)
            df.columns = [str(c).strip() for c in df.columns]
            
            current_cols = list(df.columns)
            all_debug_info.append(f"{filename}: {current_cols}")

            # Fuzzy detection for comments
            # Added 'area', 'location', 'surveyor' based on user feedback
            comment_keywords = ['comment', 'feedback', 'text', 'detail', 'reason', 'response', 'answer', 'observation', 'notes', 'description', 'opinion', 'remarks', 'suggestion', 'issue', 'complaint', 'message', 'area', 'location', 'surveyor']
            comm_col = next((c for c in df.columns if any(kw in c.lower() for kw in comment_keywords)), None)
            
            # Fuzzy detection for quality score
            # Added 'functional', 'present' based on sanitation data
            quality_keywords = ['quality', 'score', 'rating', 'value', 'level', 'grade', 'rank', 'points', 'satisfaction', 'stars', 'status', 'condition', 'state', 'func', 'working', 'present', 'count', 'number']
            qual_col = next((c for c in df.columns if any(kw in c.lower() for kw in quality_keywords)), None)
            
            if not comm_col or not qual_col:
                print(f"⚠️ Column mismatch in {filename}. Found columns: {current_cols}")
                continue

            all_comments.extend(df[comm_col].dropna().astype(str).tolist())
            total_quality += pd.to_numeric(df[qual_col], errors='coerce').sum()
            count += len(df)
            
        except Exception as e:
            all_debug_info.append(f"{filename}: Error ({str(e)})")
            print(f"❌ Error processing {filename}: {str(e)}")
            
    if count == 0:
        # Provide a helpful error message with the columns we DID find in the last file (if any)
        debug_msg = " | ".join(all_debug_info)
        raise ValueError(f"No valid data extracted. Keywords (comment/score) not found. Saw columns: [{debug_msg}]. Please rename columns to include 'comment' or 'score'.")

    avg_quality = total_quality / count if count > 0 else 0
    
    # Call the SuperAgent to generate the report
    # We mock the policy/stats json for the agent prompt context
    stats_json = json.dumps({"avg_quality": avg_quality, "total_surveyed": count})
    policy_json = json.dumps({"target_metric": 8, "sector": "Sanitation"}) # Mock policy
    
    print(f"Aggregating {count} responses for: {title}")
    report_content = agent.generate_formal_report(
        title=title,
        observed=avg_quality,
        policy_json=policy_json,
        stats_json=stats_json,
        comments=" | ".join(all_comments[:10]) # Send first 10 comments for context
    )
    
    report_entry = {
        "survey_title": title,
        "final_report": report_content
    }
    
    # Save to the reports file (append mode for JSON lines)
    report_path = "governanceflow/data/intelligence_reports.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "a") as f:
        f.write(json.dumps(report_entry) + "\n")
        
    return report_entry
