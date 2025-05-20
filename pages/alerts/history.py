import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import pytz
from utils.helpers import load_json, get_current_time

def show():
    st.title("Alert History")
    
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
    
    # Alert type filter
    alert_types = ['High Risk', 'Medium Risk', 'Low Risk', 'Info']
    selected_types = st.multiselect(
        "Filter by Alert Type",
        alert_types,
        default=alert_types
    )
    
    # Load and filter alerts
    try:
        alerts = load_json('data/alerts_history.json')
    except:
        alerts = []
    
    filtered_alerts = [
        alert for alert in alerts
        if alert['type'] in selected_types
    ]
    
    # Alert statistics
    st.header("Alert Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Alerts", len(filtered_alerts))
    with col2:
        st.metric("High Risk", len([a for a in filtered_alerts if a['type'] == 'High Risk']))
    with col3:
        st.metric("Medium Risk", len([a for a in filtered_alerts if a['type'] == 'Medium Risk']))
    with col4:
        st.metric("Low Risk", len([a for a in filtered_alerts if a['type'] == 'Low Risk']))
    
    # Alert distribution
    st.subheader("Alert Distribution")
    
    if filtered_alerts:
        # Create distribution data
        distribution_data = pd.DataFrame(filtered_alerts)
        
        # Create distribution visualization
        fig = px.pie(
            distribution_data,
            names='type',
            title='Alert Type Distribution',
            color='type',
            color_discrete_map={
                'High Risk': 'red',
                'Medium Risk': 'yellow',
                'Low Risk': 'green',
                'Info': 'blue'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Alert timeline
    st.subheader("Alert Timeline")
    
    if filtered_alerts:
        # Create timeline data
        timeline_data = pd.DataFrame(filtered_alerts)
        timeline_data['timestamp'] = pd.to_datetime(timeline_data['timestamp'])
        
        # Create timeline visualization
        fig = px.scatter(
            timeline_data,
            x='timestamp',
            y='severity',
            color='type',
            title='Alert Timeline',
            labels={'timestamp': 'Time', 'severity': 'Severity'},
            color_discrete_map={
                'High Risk': 'red',
                'Medium Risk': 'yellow',
                'Low Risk': 'green',
                'Info': 'blue'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Alert list
    st.header("Alert History")
    
    for alert in filtered_alerts:
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.write(alert['type'])
            with col2:
                st.write(f"**{alert['category']}** - {alert['message']}")
            with col3:
                st.write(alert['timestamp'])
            st.divider()
    
    # Export options
    st.subheader("Export History")
    if st.button("Download Alert History"):
        st.info("Alert history download functionality would be implemented here")
