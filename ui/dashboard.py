import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json
from agents.master_agent import run_master_analysis

# Page Configuration
st.set_page_config(
    page_title="AuditFlow | High-Impact Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-Contrast / Dark-ish Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #3d4455;
    }
    .stTextArea textarea {
        background-color: #1e2130 !important;
        color: #ffffff !important;
        border: 1px solid #3d4455 !important;
        font-family: 'Courier New', monospace;
    }
    .risk-section {
        background-color: #1e2130;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #3d4455;
        margin-bottom: 25px;
    }
    .result-box {
        background-color: #262a3b;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #007bff;
        margin-top: 15px;
        font-size: 16px;
        line-height: 1.6;
    }
    .risk-header {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .risk-badge {
        padding: 8px 18px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: 800;
        text-transform: uppercase;
        color: white;
    }
    .badge-high { background-color: #ff4b4b; box-shadow: 0 0 15px rgba(255, 75, 75, 0.4); }
    .badge-medium { background-color: #ffa500; box-shadow: 0 0 15px rgba(255, 165, 0, 0.4); }
    .badge-low { background-color: #28a745; box-shadow: 0 0 15px rgba(40, 167, 69, 0.4); }
    
    .evidence-text {
        color: #a0a8c0;
        font-style: italic;
        margin-top: 10px;
        border-top: 1px solid #3d4455;
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("⚖️ AuditFlow")
    st.markdown("**M&A Risk Intelligence Engine**")
    st.markdown("---")
    
    from indexing.document_store import get_all_documents
    docs = get_all_documents()
    
    if not docs:
        st.info("No documents found in store.")
    else:
        doc_names = list(docs.keys())
        # The user requested "no dropdown menu", but for document selection in a list of 50+, 
        # a selectbox is necessary. I will assume they meant the "expander" dropdowns for results.
        selected_doc_name = st.selectbox("📁 Select Source Document", ["-- Manual Paste --"] + doc_names)
        
        if selected_doc_name != "-- Manual Paste --":
            selected_doc = docs[selected_doc_name]
            if st.button("📥 Load Document into Analysis"):
                st.session_state["new_text"] = selected_doc["text"]
                st.rerun()

# --- Main Interface ---
st.title("AuditFlow: Risk Intelligence Report")
st.markdown("Direct analysis of legal and financial deltas between document filings.")

# --- Text Input Section ---
col1, col2 = st.columns(2)
with col1:
    old = st.text_area("📄 Baseline (Previous Filing)", height=220, key="old_text", placeholder="Paste historical document text here...")
with col2:
    new = st.text_area("📄 Target (Current Filing)", height=220, value=st.session_state.get("new_text", ""), key="new_text", placeholder="Paste current document text here...")

# --- Analysis Action ---
if st.button("🔥 START COMPREHENSIVE ANALYSIS", type="primary", use_container_width=True):
    if not new:
        st.error("⚠️ Error: Target document is empty. Please provide text to analyze.")
    else:
        with st.spinner("🚀 Master Agent is processing... Analyzing Litigation, Covenants, and Verifying Sources."):
            result = run_master_analysis(old, new)
        
        if "error" in result:
            st.error(f"❌ Analysis failed: {result['error']}")
        else:
            st.session_state["analysis_result"] = result
            st.success("🎯 Analysis Complete!")

# --- Direct Results Rendering (No Dropdowns) ---
if "analysis_result" in st.session_state:
    res = st.session_state["analysis_result"]
    
    st.markdown("---")
    st.markdown("## 📊 Agent Intelligence Reports")
    
    def get_risk_config(level):
        level = str(level).upper()
        if "HIGH" in level: return 100, "HIGH", "badge-high"
        if "MEDIUM" in level: return 60, "MEDIUM", "badge-medium"
        return 20, "LOW", "badge-low"

    # 1. Litigation Risk Section
    lit = res.get("litigation", {})
    l_val, l_lab, l_cls = get_risk_config(lit.get("risk_level", "LOW"))
    
    st.markdown(f"""
        <div class="risk-section">
            <div class="risk-header">
                ⚖️ Litigation Risk Analysis: <span class="risk-badge {l_cls}">{l_lab}</span>
            </div>
    """, unsafe_allow_html=True)
    st.progress(l_val/100)
    st.markdown(f"""
            <div class="result-box">
                <b>Detailed Assessment:</b><br/>
                {lit.get('explanation', 'No explanation provided.')}
                <div class="evidence-text">
                    <b>Evidence from source:</b> {lit.get('evidence', 'No specific evidence cited.')}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Covenant Risk Section
    cov = res.get("covenant", {})
    c_val, c_lab, c_cls = get_risk_config(cov.get("risk_level", "LOW"))
    
    st.markdown(f"""
        <div class="risk-section">
            <div class="risk-header">
                📜 Debt Covenant Analysis: <span class="risk-badge {c_cls}">{c_lab}</span>
            </div>
    """, unsafe_allow_html=True)
    st.progress(c_val/100)
    st.markdown(f"""
            <div class="result-box" style="border-left-color: #ffa500;">
                <b>Detailed Assessment:</b><br/>
                {cov.get('explanation', 'No explanation provided.')}
                <div class="evidence-text">
                    <b>Evidence from source:</b> {cov.get('evidence', 'No specific evidence cited.')}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. Verification Section
    ver = res.get("verifier", {})
    v_verdict = str(ver.get("verdict")).upper()
    v_cls = "badge-verified" if "VERIFIED" in v_verdict else "badge-high"
    
    st.markdown(f"""
        <div class="risk-section" style="border-color: #007bff;">
            <div class="risk-header">
                ✅ Consistency Verification: <span class="risk-badge {v_cls}">{v_verdict}</span>
            </div>
            <div class="result-box" style="border-left-color: #28a745;">
                {ver.get('explanation', 'No verification details available.')}
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("---")
    st.markdown("### 🚦 System Ready")
    st.info("💡 **Instructions:** Paste your baseline and target documents above, then click the blue analysis button to generate visual risk reports.")
