# pages/alerts/live.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.markdown("## Real-time Alert Center")

# Alert Overview
st.markdown("### 🚨 Active Alerts")

# Alert Statistics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Critical Alerts", "2", "-1")
with col2:
    st.metric("High Priority", "5", "+2")
with col3:
    st.metric("Medium Priority", "8", "-3")
with col4:
    st.metric("Low Priority", "12", "+1")

# Live Alert Feed
st.markdown("### 📊 Live Alert Feed")

# Sample alert data
alerts = pd.DataFrame({
    'Timestamp': [(datetime.now() - timedelta(minutes=x)).strftime('%H:%M:%S') 
                  for x in range(10)],
    'Type': ['System', 'Security', 'Performance', 'System', 'Security',
             'Performance', 'Security', 'System', 'Performance', 'Security'],
    'Priority': ['Critical', 'High', 'Medium', 'Low', 'High',
                 'Medium', 'High', 'Low', 'Medium', 'Low'],
    'Message': ['Server CPU at 95%', 'Failed login attempt', 'High latency detected',
                'Low disk space', 'Unusual network activity',
                'Database slow query', 'Firewall rule violation',
                'Service restart required', 'Memory usage high',
                'SSL certificate expiring']
})

# Display alerts with conditional formatting
def color_priority(val):
    colors = {
        'Critical': 'background-color: #ff0000; color: white',
        'High': 'background-color: #ff9900; color: white',
        'Medium': 'background-color: #ffcc00',
        'Low': 'background-color: #00cc00; color: white'
    }
    return colors.get(val, '')

st.dataframe(
    alerts.style.applymap(color_priority, subset=['Priority']),
    hide_index=True
)

# Alert Analytics
st.markdown("### 📈 Alert Analytics")
tab1, tab2 = st.tabs(["Distribution", "Trend Analysis"])

with tab1:
    # Alert distribution by type
    fig = px.pie(alerts, names='Type', title='Alert Distribution by Type')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Alert trend
    trend_data = pd.DataFrame({
        'Time': pd.date_range(start='2024-03-01', end='2024-03-02', freq='H'),
        'Alert Count': [4, 6, 3, 5, 7, 4, 3, 5, 6, 8, 5, 4,
                       3, 5, 4, 6, 7, 5, 4, 3, 5, 6, 4, 3]
    })
    fig = px.line(trend_data, x='Time', y='Alert Count',
                  title='24-Hour Alert Trend')
    st.plotly_chart(fig, use_container_width=True)

# Alert Configuration
st.markdown("### ⚙️ Alert Settings")
with st.expander("Configure Alerts"):
    col1, col2 = st.columns(2)
    with col1:
        st.multiselect(
            "Alert Types to Monitor",
            ["System", "Security", "Performance", "Network", "Database"]
        )
        st.selectbox(
            "Refresh Rate",
            ["5 seconds", "10 seconds", "30 seconds", "1 minute"]
        )
    with col2:
        st.multiselect(
            "Notification Channels",
            ["Email", "SMS", "Slack", "Teams"]
        )
        st.selectbox(
            "Priority Threshold",
            ["All", "High & Critical Only", "Critical Only"]
        )

# Response Actions
st.markdown("### 🔧 Quick Actions")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Acknowledge Selected", use_container_width=True)
with col2:
    st.button("Escalate Selected", use_container_width=True)
with col3:
    st.button("Clear Selected", use_container_width=True)

# Alert History
with st.expander("Alert History"):
    st.markdown("#### Recent Alert History")
    history_data = pd.DataFrame({
        'Date': ['2024-03-01', '2024-03-01', '2024-03-01'],
        'Alert': ['Server Overload', 'Network Outage', 'Security Breach'],
        'Resolution': ['Scaled resources', 'Router restart', 'Updated firewall'],
        'Duration': ['45 min', '30 min', '15 min']
    })
    st.dataframe(history_data, hide_index=True)
