import streamlit as st
import os
import sys
import importlib
from dotenv import load_dotenv

# --- Platform Configuration ---
PLATFORM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PLATFORM_ROOT, ".env"))

# --- Strict Isolation Helper ---
def purge_modules(prefix):
    """
    Purges all modules from sys.modules that start with a specific prefix.
    This guarantees zero memory footprint for the inactive app.
    """
    to_delete = [name for name in sys.modules if name.startswith(prefix)]
    for name in to_delete:
        del sys.modules[name]

# --- Page Setup (Universal) ---
st.set_page_config(
    page_title="AI Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    .main { background-color: #0c0e12; color: #e0e6ed; font-family: 'Inter', sans-serif; }
    .launcher-title { font-family: 'JetBrains Mono', monospace; color: #00d4ff; text-align: center; margin-top: 50px; letter-spacing: 2px; }
    .card { background: linear-gradient(145deg, #161b22, #0d1117); border: 1px solid #30363d; border-radius: 12px; padding: 40px; text-align: center; transition: all 0.3s ease; height: 100%; }
    .card:hover { border-color: #00d4ff; box-shadow: 0 0 30px rgba(0, 212, 255, 0.15); transform: translateY(-8px); }
    .feature-list { text-align: left; margin-top: 30px; font-size: 14px; color: #c9d1d9; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)

# --- Navigation State ---
if "platform_mode" not in st.session_state:
    st.session_state.platform_mode = "launcher"

def set_mode(mode):
    # Purge existing modules before switching to ensure isolation
    if st.session_state.platform_mode == "auditflow": purge_modules("auditflow")
    if st.session_state.platform_mode == "governanceflow": purge_modules("governanceflow")
    st.session_state.platform_mode = mode

# Sidebar Hub Control
if st.session_state.platform_mode != "launcher":
    if st.sidebar.button("🏠 RETURN TO PLATFORM HUB", use_container_width=True):
        set_mode("launcher")
        st.rerun()
    st.sidebar.markdown("---")

# --- Hub Layout ---
if st.session_state.platform_mode == "launcher":
    st.markdown("<h1 class='launcher-title'>AI INTELLIGENCE PLATFORM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>STRICT ISOLATION GATEWAY v3.0</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h2>AUDITFLOW</h2><p>Enterprise Risk Intelligence</p><div class="feature-list">• Risk Delta Analysis<br/>• Master Agent Monitoring<br/>• SVG Risk Gauges</div></div>', unsafe_allow_html=True)
        if st.button("LAUNCH AUDITFLOW", use_container_width=True, type="primary"):
            set_mode("auditflow")
            st.rerun()

    with col2:
        st.markdown('<div class="card"><h2>GOVERNANCEFLOW</h2><p>Public Sector Intelligence</p><div class="feature-list">• Corruption Discovery<br/>• Fuzzy CSV Ingestion<br/>• Policy Compliance</div></div>', unsafe_allow_html=True)
        if st.button("LAUNCH GOVERNANCEFLOW", use_container_width=True, type="primary"):
            set_mode("governanceflow")
            st.rerun()

# --- Isolated Routing Logic ---
if PLATFORM_ROOT not in sys.path:
    sys.path.insert(0, PLATFORM_ROOT)

if st.session_state.platform_mode == "auditflow":
    # Change working directory to module root for internal file paths
    os.chdir(os.path.join(PLATFORM_ROOT, "auditflow"))
    
    # Lazy Import from the project root
    import auditflow.ui.dashboard as audit_ui
    importlib.reload(audit_ui) # Force reload to ensure a fresh state if returning
    audit_ui.run_audit_dashboard()

elif st.session_state.platform_mode == "governanceflow":
    os.chdir(os.path.join(PLATFORM_ROOT, "governanceflow"))
    
    import governanceflow.ui.dashboard as gov_ui
    importlib.reload(gov_ui)
    gov_ui.run_gov_dashboard()
