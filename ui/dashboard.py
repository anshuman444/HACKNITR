import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json
from agents.master_agent import run_master_analysis

# Page Configuration
st.set_page_config(
    page_title="AuditFlow Intelligence Console",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Intelligence Console Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    .main {
        background-color: #0c0e12;
        color: #e0e6ed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Global Container */
    .console-header {
        font-family: 'JetBrains Mono', monospace;
        color: #00d4ff;
        border-bottom: 2px solid #1f2937;
        padding-bottom: 10px;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }
    
    /* Intelligence Brief Cards */
    .brief-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .brief-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        color: #8b949e;
        text-transform: uppercase;
        border-bottom: 1px solid #30363d;
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    
    .brief-content {
        font-size: 15px;
        line-height: 1.6;
        color: #c9d1d9;
    }
    
    .brief-evidence {
        margin-top: 12px;
        padding: 10px;
        background-color: rgba(0, 212, 255, 0.05);
        border-left: 2px solid #00d4ff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #58a6ff;
    }

    /* Gauge Container */
    .gauge-wrapper {
        text-align: center;
        margin-bottom: 10px;
    }
    
    .risk-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: bold;
        padding: 2px 10px;
        border-radius: 4px;
        margin-left: 10px;
    }
    .tag-high { color: #ff4b4b; border: 1px solid #ff4b4b; background: rgba(255, 75, 75, 0.1); }
    .tag-medium { color: #ffa500; border: 1px solid #ffa500; background: rgba(255, 165, 0, 0.1); }
    .tag-low { color: #23d18b; border: 1px solid #23d18b; background: rgba(35, 209, 139, 0.1); }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #30363d;
    }
    
    /* Input areas */
    .stTextArea textarea {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: #c9d1d9 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SVG Gauge Helper ---
def draw_gauge(value, label, level_class):
    # Map level to color
    color = "#23d18b" # Default Low
    if "HIGH" in level_class.upper(): color = "#ff4b4b"
    elif "MEDIUM" in level_class.upper(): color = "#ffa500"
    
    # Calculate needle rotation (0-100 to -90 to 90 degrees)
    rotation = (value * 1.8) - 90
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                background-color: transparent;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 120px;
                overflow: hidden;
            }}
            .gauge-wrapper {{
                text-align: center;
            }}
            @keyframes needle-anim {{
                from {{ transform: rotate(-90deg); }}
                to {{ transform: rotate({rotation}deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="gauge-wrapper">
            <svg width="200" height="120" viewBox="0 0 200 120">
                <!-- Background Arc -->
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#21262d" stroke-width="12" stroke-linecap="round"/>
                <!-- Value Arc (Partial) -->
                <path d="M 20 100 A 80 80 0 0 1 {20 + (160 * value/100)} 100" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" style="opacity: 0.3;"/>
                
                <!-- Scale Indicators -->
                <text x="15" y="115" fill="#8b949e" font-size="10" font-family="monospace">LOW</text>
                <text x="170" y="115" fill="#8b949e" font-size="10" font-family="monospace">HIGH</text>
                
                <!-- Center Label -->
                <text x="100" y="80" fill="#e0e6ed" font-size="16" font-weight="bold" font-family="sans-serif" text-anchor="middle">{label}</text>
                <text x="100" y="100" fill="{color}" font-size="12" font-weight="bold" font-family="monospace" text-anchor="middle">{value}% RISK</text>
                
                <!-- Needle -->
                <g transform="translate(100, 100)">
                    <line x1="0" y1="0" x2="0" y2="-75" stroke="#e0e6ed" stroke-width="3" stroke-linecap="round" 
                          style="animation: needle-anim 1.5s ease forwards; transform-origin: center bottom;">
                    </line>
                    <circle cx="0" cy="0" r="6" fill="#00d4ff"/>
                </g>
            </svg>
        </div>
    </body>
    </html>
    """
    return html_content

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff; font-family: JetBrains Mono;'>AUDITFLOW</h1>", unsafe_allow_html=True)
    st.markdown("`INTELLIGENCE CONSOLE V2.0`")
    st.markdown("---")
    
    from indexing.document_store import get_all_documents
    docs = get_all_documents()
    
    if not docs:
        st.info("DATA STORE EMPTY")
    else:
        doc_names = list(docs.keys())
        selected_doc_name = st.selectbox("SOURCE SELECTION", ["NONE"] + doc_names)
        
        if selected_doc_name != "NONE":
            selected_doc = docs[selected_doc_name]
            if st.button("LOAD TARGET TEXT", use_container_width=True):
                st.session_state["new_text"] = selected_doc["text"]
                st.rerun()

# --- Main Interface ---
st.markdown("<div class='console-header'>> SYSTEM STATUS: ONLINE | ANALYSIS MODE: ACCELERATED</div>", unsafe_allow_html=True)

# Input Layout
col_in1, col_in2 = st.columns(2)
with col_in1:
    old = st.text_area("BASELINE FILING", height=200, key="old_text", placeholder="INPUT PREVIOUS FILING DATA...")
with col_in2:
    new = st.text_area("TARGET FILING", height=200, key="new_text", placeholder="INPUT CURRENT FILING DATA...")

# Command Bar
if st.button("EXECUTE RISK INTELLIGENCE SCAN", type="primary", use_container_width=True):
    if not new:
        st.error("CRITICAL ERROR: TARGET BUFFER EMPTY")
    else:
        with st.status("INITIALIZING AGENTS...", expanded=True) as status:
            st.write("Fetching document deltas...")
            st.write("Analyzing master risk profile...")
            result = run_master_analysis(old, new)
            status.update(label="ANALYSIS COMPLETE", state="complete", expanded=False)
        
        if "error" in result:
            st.error(f"SCAN FAILED: {result['error']}")
        else:
            st.session_state["p_analysis"] = result
            st.success("SCAN SEQUENCE SUCCESSFUL")

# --- Intelligence Output ---
if "p_analysis" in st.session_state:
    res = st.session_state["p_analysis"]
    
    st.markdown("<h2 class='console-header'>ANALYSIS INTELLIGENCE BRIEF</h2>", unsafe_allow_html=True)
    
    # Risk Metrics Control Row
    met_col1, met_col2 = st.columns(2)
    
    def get_risk_meta(level):
        l = str(level).upper()
        if "HIGH" in l: return 92, "HIGH", "tag-high"
        if "MEDIUM" in l: return 54, "MEDIUM", "tag-medium"
        return 18, "LOW", "tag-low"

    # Litigation Gauge
    with met_col1:
        val, lab, tag = get_risk_meta(res.get("litigation", {}).get("risk_level", "LOW"))
        st.components.v1.html(draw_gauge(val, "LITIGATION", lab), height=130)
        
        # Brief
        lit = res.get("litigation", {})
        st.markdown(f"""
        <div class="brief-card">
            <div class="brief-title">LITIGATION ASSESSMENT <span class="risk-tag {tag}">{lab}</span></div>
            <div class="brief-content">{lit.get('explanation')}</div>
            <div class="brief-evidence">> {lit.get('evidence')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Covenant Gauge
    with met_col2:
        val, lab, tag = get_risk_meta(res.get("covenant", {}).get("risk_level", "LOW"))
        st.components.v1.html(draw_gauge(val, "COVENANT", lab), height=130)
        
        # Brief
        cov = res.get("covenant", {})
        st.markdown(f"""
        <div class="brief-card">
            <div class="brief-title">COVENANT SENTINEL <span class="risk-tag {tag}">{lab}</span></div>
            <div class="brief-content">{cov.get('explanation')}</div>
            <div class="brief-evidence">> {cov.get('evidence')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Verification Section
    ver = res.get("verifier", {})
    st.markdown(f"""
    <div class="brief-card" style="border-top: 2px solid #00d4ff;">
        <div class="brief-title">INTEGRITY VERIFICATION: {str(ver.get('verdict')).upper()}</div>
        <div class="brief-content">{ver.get('explanation')}</div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #8b949e; font-family: JetBrains Mono; padding: 40px;'>READY FOR COMMAND. INPUT FILINGS AND EXECUTE SCAN.</div>", unsafe_allow_html=True)
