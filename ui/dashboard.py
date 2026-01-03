import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from agents.litigation_agent import llm_litigation_delta
from agents.covenant_agent import covenant_sentinel_llm
from agents.verifier_agent import verify_agent
#from analytics.ragas_eval import run_ragas_evaluation

st.set_page_config(page_title="AuditFlow", layout="wide")
st.title("AuditFlow – Live M&A Due Diligence")

# --- Live Document Feed Sidebar ---
from indexing.document_store import get_all_documents
docs = get_all_documents()

st.sidebar.title("📡 Live Document Feed")
if not docs:
    st.sidebar.info("No documents ingested yet. Run `main.py` to ingest PDFs.")
else:
    doc_names = list(docs.keys())
    selected_doc_name = st.sidebar.selectbox("Select Ingested Document", ["None"] + doc_names)
    
    if selected_doc_name != "None":
        selected_doc = docs[selected_doc_name]
        st.sidebar.success(f"Selected: {selected_doc_name}")
        if st.sidebar.button("Load into 'Current Filing'"):
            st.session_state["new_text"] = selected_doc["text"]
            st.sidebar.info("Document loaded!")

# --- Main Interface ---
if "new_text" not in st.session_state:
    st.session_state["new_text"] = ""
if "old_text" not in st.session_state:
    st.session_state["old_text"] = ""

old = st.text_area("Previous Filing", key="old_text")
new = st.text_area("Current Filing", key="new_text")

from agents.master_agent import run_master_analysis

if st.button("Run Analysis"):
    with st.spinner("🔍 Master Agent is performing a consolidated analysis... (Only 1 API call)"):
        result = run_master_analysis(old, new)
    
    if "error" in result:
        st.error(f"Analysis failed: {result['error']}")
        st.code(result.get("raw_response", ""))
    else:
        st.success("✅ Analysis Complete!")

        # Display results from the Master Agent consolidated response
        st.subheader("Litigation Agent")
        st.json(result.get("litigation", {}))

        st.subheader("Covenant Agent")
        st.json(result.get("covenant", {}))

        st.subheader("Verifier")
        st.json(result.get("verifier", {}))

#    st.subheader("RAGAS Score")
 #   st.json(score)
