import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import pytz
from utils.helpers import load_json, get_current_time

def show_dashboard():
    st.title("Car Insurance Dashboard")
    
    # Load data
    try:
        analysis_data = load_json('data/car_analysis.json')
    except:
        st.warning("No analysis data available. Please upload and analyze claims data first.")
        return
    
    # Key Metrics
    st.header("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Claims",
            analysis_data.get('total_claims', 0)
        )
    with col2:
        st.metric(
            "Total Amount",
            f"${analysis_data.get('total_amount', 0):,.2f}"
        )
    with col3:
        st.metric(
            "Average Amount",
            f"${analysis_data.get('average_amount', 0):,.2f}"
        )
    with col4:
        st.metric(
            "Last Updated",
            analysis_data.get('timestamp', 'N/A')
        )
    
    # Status Distribution
    st.header("Claims Status Distribution")
    status_data = analysis_data.get('status_distribution', {})
    
    if status_data:
        fig_status = px.pie(
            values=list(status_data.values()),
            names=list(status_data.keys()),
            title='Claims Status Distribution'
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Recent Activity
    st.header("Recent Activity")
    
    # Simulate recent activity
    recent_activity = [
        {
            'timestamp': (get_current_time() - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"),
            'action': 'Claim Processed',
            'details': f'Claim #{i+1} processed successfully'
        }
        for i in range(5)
    ]
    
    for activity in recent_activity:
        st.info(f"{activity['timestamp']} - {activity['action']}: {activity['details']}")
    
    # Performance Metrics
    st.header("Performance Metrics")
    
    # Simulate performance data
    performance_data = {
        'Processing Time': 85,
        'Customer Satisfaction': 92,
        'Fraud Detection Rate': 78,
        'Claim Resolution Rate': 88
    }
    
    for metric, value in performance_data.items():
        st.progress(value/100, text=f"{metric}: {value}%")
