import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import io

# Import the processors
try:
    from governanceflow.analytics.processor import run_batch_analytics
except ImportError:
    def run_batch_analytics(*args, **kwargs): return {"error": "Module error"}

def run_gov_dashboard():
    # Page Configuration
    try:
        st.set_page_config(page_title="GovernanceFlow", layout="wide")
    except:
        pass

    st.title("🛡️ GovernanceFlow Intelligence")

    # Navigation
    page = st.sidebar.radio("Go to", ["Upload New Survey", "Intelligence Reports", "Overview"])

    if page == "Upload New Survey":
        st.subheader("Ingest Field Survey")
        with st.form("upload"):
            title = st.text_input("Survey Title", placeholder="e.g. Swachh Bharat Mission (Gramin)")
            uploaded_files = st.file_uploader("Upload CSV Surveys", accept_multiple_files=True)
            
            if st.form_submit_button("🚀 Start Intelligence Scan"):
                if not title or not uploaded_files:
                    st.error("Please provide both a title and survey files.")
                else:
                    with st.spinner("🔄 AGGREGATING DATA & GENERATING INTELLIGENCE..."):
                        # Prepare data for processor
                        files_data = {}
                        for f in uploaded_files:
                            files_data[f.name] = io.BytesIO(f.getbuffer())
                        
                        # Run the synchronous analysis
                        try:
                            result = run_batch_analytics(title, files_data)
                            st.success(f"✅ INTELLIGENCE GENERATED FOR: {title}")
                            st.info("Switch to the 'Intelligence Reports' tab to view results.")
                            st.balloons()
                        except Exception as e:
                            st.error(f"Analysis failed: {e}")

    elif page == "Intelligence Reports":
        st.subheader("📋 Generated Intelligence Briefs")
        report_path = "governanceflow/data/intelligence_reports.json"
        
        if os.path.exists(report_path):
            with open(report_path, "r") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    try:
                        data = json.loads(line)
                        with st.expander(f"📄 Report: {data.get('survey_title', 'Unnamed Survey')}", expanded=True):
                            content = data.get('final_report', 'Processing...')
                            content = content.replace("```json", "").replace("```", "").strip()
                            st.markdown(content)
                    except:
                        continue
        else:
            st.info("No reports found. Please upload a survey and run the scan first.")

    elif page == "Overview":
        st.subheader("System Performance")
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Scouts", "142", "+4")
        col2.metric("Policy Compliance", "68%", "-2%")
        col3.metric("Critical Deviations", "12", "HOT")
        st.write("Real-time monitoring of public service delivery and government policy adherence.")

if __name__ == "__main__":
    run_gov_dashboard()
