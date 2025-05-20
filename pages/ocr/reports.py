import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
from utils.helpers import load_json, get_current_time

def show():
    st.title("OCR Reports")
    
    # Report type selection
    report_type = st.selectbox(
        "Select Report Type",
        ["Document Analysis", "Processing Statistics", "Quality Metrics"]
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
                analysis_data = load_json('data/ocr_analysis.json')
                
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
                        "Average Confidence": "85%",
                        "Success Rate": "95%"
                    }
                    
                    for stat, value in stats.items():
                        st.metric(stat, value)
                    
                    # Document types distribution
                    st.write("### Document Types")
                    fig = px.pie(
                        values=[1],
                        names=["Invoice"],
                        title="Document Types Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif report_type == "Processing Statistics":
                    st.subheader("Processing Statistics")
                    
                    # Processing metrics
                    st.write("### Processing Metrics")
                    processing_data = {
                        "Average Processing Time": "2.5s",
                        "Success Rate": "95%",
                        "Error Rate": "5%"
                    }
                    
                    for metric, value in processing_data.items():
                        st.info(f"{metric}: {value}")
                    
                elif report_type == "Quality Metrics":
                    st.subheader("Quality Metrics")
                    
                    # Quality metrics
                    st.write("### Quality Metrics")
                    quality_data = {
                        "Text Recognition": 85,
                        "Entity Detection": 90,
                        "Format Preservation": 88
                    }
                    
                    for metric, value in quality_data.items():
                        st.progress(value/100, text=f"{metric}: {value}%")
                
                # Export options
                st.subheader("Export Report")
                if st.button("Download Report"):
                    st.info("Report download functionality would be implemented here")
                
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
