import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import pytz
import time
from utils.helpers import load_json, save_json, get_current_time

def show():
    st.title("Live Alerts Dashboard")
    
    # Initialize session state for alerts
    if 'alerts' not in st.session_state:
        st.session_state.alerts = []
    
    # Alert types
    alert_types = {
        'High Risk': '🔴',
        'Medium Risk': '🟡',
        'Low Risk': '🟢',
        'Info': 'ℹ️'
    }
    
    # Real-time alerts section
    st.header("Real-time Alerts")
    
    # Create a placeholder for live updates
    alert_placeholder = st.empty()
    
    # Simulate real-time alerts
    def generate_alert():
        alert_types = ['High Risk', 'Medium Risk', 'Low Risk', 'Info']
        alert_categories = ['Fraud Detection', 'System Alert', 'Compliance', 'Performance']
        
        return {
            'timestamp': str(get_current_time()),
            'type': alert_types[hash(str(get_current_time())) % len(alert_types)],
            'category': alert_categories[hash(str(get_current_time())) % len(alert_categories)],
            'message': f"Alert message {len(st.session_state.alerts) + 1}",
            'severity': hash(str(get_current_time())) % 100
        }
    
    # Alert monitoring section
    st.header("Alert Monitoring")
    
    # Alert filters
    col1, col2 = st.columns(2)
    with col1:
        selected_type = st.multiselect(
            "Filter by Alert Type",
            list(alert_types.keys()),
            default=list(alert_types.keys())
        )
    with col2:
        selected_category = st.multiselect(
            "Filter by Category",
            ['Fraud Detection', 'System Alert', 'Compliance', 'Performance'],
            default=['Fraud Detection', 'System Alert', 'Compliance', 'Performance']
        )
    
    # Alert statistics
    st.subheader("Alert Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Alerts", len(st.session_state.alerts))
    with col2:
        st.metric("High Risk", len([a for a in st.session_state.alerts if a['type'] == 'High Risk']))
    with col3:
        st.metric("Medium Risk", len([a for a in st.session_state.alerts if a['type'] == 'Medium Risk']))
    with col4:
        st.metric("Low Risk", len([a for a in st.session_state.alerts if a['type'] == 'Low Risk']))
    
    # Alert timeline
    st.subheader("Alert Timeline")
    
    if st.session_state.alerts:
        # Create timeline data
        timeline_data = pd.DataFrame(st.session_state.alerts)
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
    
    # Alert management section
    st.header("Alert Management")
    
    # Alert actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Test Alert"):
            new_alert = generate_alert()
            st.session_state.alerts.append(new_alert)
            st.success("Test alert generated!")
    
    with col2:
        if st.button("Clear All Alerts"):
            st.session_state.alerts = []
            st.success("All alerts cleared!")
    
    # Display filtered alerts
    st.subheader("Recent Alerts")
    
    filtered_alerts = [
        alert for alert in st.session_state.alerts
        if alert['type'] in selected_type and alert['category'] in selected_category
    ]
    
    for alert in filtered_alerts:
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.write(alert_types[alert['type']])
            with col2:
                st.write(f"**{alert['category']}** - {alert['message']}")
            with col3:
                st.write(alert['timestamp'])
            st.divider()
    
    # Alert settings
    st.header("Alert Settings")
    
    with st.expander("Notification Settings"):
        st.checkbox("Email Notifications", value=True)
        st.checkbox("SMS Notifications", value=False)
        st.checkbox("System Notifications", value=True)
    
    with st.expander("Alert Thresholds"):
        st.slider("High Risk Threshold", 0, 100, 80)
        st.slider("Medium Risk Threshold", 0, 100, 50)
        st.slider("Low Risk Threshold", 0, 100, 20)
    
    # Save alert configuration
    if st.button("Save Settings"):
        st.success("Alert settings saved!")
