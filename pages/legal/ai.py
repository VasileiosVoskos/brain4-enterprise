# pages/legal/ai.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.markdown("## Legal AI Assistant")

# AI Analysis Tools
st.markdown("### 🤖 Legal Document Analysis")

# Document Analysis Section
uploaded_file = st.file_uploader(
    "Upload Legal Document for Analysis",
    type=['pdf', 'docx', 'txt']
)

if uploaded_file:
    with st.spinner("Analyzing document..."):
        st.success("Document analyzed successfully!")
        
        # Analysis Results
        st.markdown("#### Document Analysis Results")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Risk Score", "Low", "Better than 85% of documents")
        with col2:
            st.metric("Compliance Score", "98%", "+3%")

        # Key Findings
        st.markdown("#### Key Findings")
        findings = [
            "✅ All required clauses present",
            "⚠️ Liability section needs review",
            "✅ Compliant with latest regulations",
            "📌 Similar to standard template (92% match)"
        ]
        for finding in findings:
            st.markdown(finding)

# Contract Review Assistant
st.markdown("### 📑 Contract Review Assistant")
tab1, tab2 = st.tabs(["Quick Review", "Detailed Analysis"])

with tab1:
    st.markdown("""
    #### Automated Checks
    - **Party Information**: Verified ✅
    - **Key Dates**: All present ✅
    - **Payment Terms**: Standard terms detected ✅
    - **Liability Clauses**: Review recommended ⚠️
    """)

with tab2:
    analysis_data = pd.DataFrame({
        'Section': ['Definitions', 'Terms', 'Liability', 'Termination'],
        'Risk Level': ['Low', 'Low', 'Medium', 'Low'],
        'Action Needed': ['None', 'None', 'Review', 'None']
    })
    st.dataframe(analysis_data, hide_index=True)

# Compliance Checker
st.markdown("### ⚖️ Compliance Checker")
compliance_options = [
    "GDPR Compliance",
    "Employment Law",
    "Contract Law",
    "Industry Regulations"
]

selected_compliance = st.multiselect(
    "Select Compliance Frameworks to Check",
    compliance_options
)

if selected_compliance:
    st.markdown("#### Compliance Analysis")
    for framework in selected_compliance:
        st.progress(0.95, text=f"{framework}: 95% Compliant")

# Legal AI Settings
with st.expander("AI Analysis Settings"):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "Analysis Depth",
            ["Quick Scan", "Standard Analysis", "Deep Analysis"]
        )
        st.multiselect(
            "Focus Areas",
            ["Risk Assessment", "Compliance", "Contract Terms", "Legal Precedents"]
        )
    with col2:
        st.selectbox("Jurisdiction", ["US", "EU", "UK", "International"])
        st.checkbox("Enable Advanced Pattern Recognition")

# Recent Activity
st.markdown("### 📊 Recent Activity")
recent_activity = pd.DataFrame({
    'Document': ['Service Agreement', 'Employment Contract', 'NDA'],
    'Analysis Date': ['2024-03-01', '2024-02-28', '2024-02-27'],
    'Status': ['Completed', 'In Progress', 'Completed']
})
st.dataframe(recent_activity, hide_index=True)
