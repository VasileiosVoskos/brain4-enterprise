import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
from utils.helpers import load_json, get_current_time

def show():
    st.title("Legal Reports")
    
    # Report type selection
    report_type = st.selectbox(
        "Select Report Type",
        ["Document Analysis", "Risk Assessment", "Compliance Report"]
    )
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now()
        )
    
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            try:
                # Load analysis data
                analysis_data = load_json('data/legal_analysis.json')
                
                if not analysis_data:
                    st.warning("No analysis data available")
                    return
                
                # Generate report based on type
                if report_type == "Document Analysis":
                    st.subheader("Document Analysis Report")
                    
                    # Document statistics
                    st.write("### Document Statistics")
                    stats = {
                        "Total Documents": 1,
                        "Average Risk Level": "Medium",
                        "Compliance Rate": "88%"
                    }
                    
                    for stat, value in stats.items():
                        st.metric(stat, value)
                    
                    # Document types distribution
                    st.write("### Document Types")
                    fig = px.pie(
                        values=[1],
                        names=["Contract"],
                        title="Document Types Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif report_type == "Risk Assessment":
                    st.subheader("Risk Assessment Report")
                    
                    # Risk metrics
                    st.write("### Risk Metrics")
                    risk_data = {
                        "High Risk": 0,
                        "Medium Risk": 1,
                        "Low Risk": 0
                    }
                    
                    fig = px.bar(
                        x=list(risk_data.keys()),
                        y=list(risk_data.values()),
                        title="Risk Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif report_type == "Compliance Report":
                    st.subheader("Compliance Report")
                    
                    # Compliance metrics
                    st.write("### Compliance Metrics")
                    compliance_data = {
                        "Regulatory Compliance": 88,
                        "Internal Policy Compliance": 92,
                        "Documentation Compliance": 85
                    }
                    
                    for metric, value in compliance_data.items():
                        st.progress(value/100, text=f"{metric}: {value}%")
                
                # Export options
                st.subheader("Export Report")
                if st.button("Download Report"):
                    st.info("Report download functionality would be implemented here")
                
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
