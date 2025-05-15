import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

st.markdown("## Fleet Dashboard")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Vehicles", "127", "+3 this month")
with col2:
    st.metric("Active Vehicles", "112", "-2")
with col3:
    st.metric("Maintenance Due", "15", "+5")
with col4:
    st.metric("Fleet Health", "94%", "+2%")

# Fleet Status Overview
st.markdown("### Fleet Status Overview")
status_data = pd.DataFrame({
    'Status': ['Active', 'Maintenance', 'Repair', 'Idle'],
    'Count': [112, 8, 4, 3],
    'Percentage': [88, 6, 3, 3]
})

col1, col2 = st.columns([2, 1])
with col1:
    fig = px.pie(status_data, values='Count', names='Status', 
                 title='Fleet Status Distribution')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.dataframe(status_data, hide_index=True, use_container_width=True)

# Performance Metrics
st.markdown("### Performance Metrics")
tabs = st.tabs(["Fuel Efficiency", "Maintenance Costs", "Utilization"])

with tabs[0]:
    # Generate sample data for fuel efficiency
    dates = pd.date_range(start='2024-01-01', end='2024-03-01', freq='D')
    efficiency = pd.DataFrame({
        'Date': dates,
        'Efficiency': [85 + i * 0.1 + np.random.randn() * 2 for i in range(len(dates))]
    })
    fig = px.line(efficiency, x='Date', y='Efficiency', 
                  title='Fleet Fuel Efficiency Trend')
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    costs = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar'],
        'Planned': [12000, 15000, 13000],
        'Unplanned': [3000, 2000, 4000]
    })
    fig = px.bar(costs, x='Month', y=['Planned', 'Unplanned'],
                 title='Maintenance Costs')
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    util = pd.DataFrame({
        'Vehicle Type': ['Trucks', 'Vans', 'Cars'],
        'Utilization': [85, 78, 92]
    })
    fig = px.bar(util, x='Vehicle Type', y='Utilization',
                 title='Fleet Utilization (%)')
    st.plotly_chart(fig, use_container_width=True)

# Recent Alerts
st.markdown("### Recent Alerts")
alerts = pd.DataFrame({
    'Time': ['10:30 AM', '09:15 AM', '08:45 AM'],
    'Vehicle': ['TRK-001', 'VAN-023', 'CAR-115'],
    'Alert Type': ['Maintenance Due', 'Low Fuel', 'Service Required'],
    'Priority': ['High', 'Medium', 'Low']
})
st.dataframe(alerts, hide_index=True, use_container_width=True)

# Dashboard Settings
with st.expander("Dashboard Settings"):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Update Frequency", 
                    ["Real-time", "Every 5 minutes", "Every 15 minutes", "Every hour"])
        st.multiselect("Vehicle Types to Display",
                      ["All", "Trucks", "Vans", "Cars"])
    with col2:
        st.selectbox("Time Range",
                    ["Last 24 hours", "Last 7 days", "Last 30 days", "Custom"])
        st.multiselect("Metrics to Show",
                      ["Fuel Efficiency", "Maintenance", "Utilization", "Costs"])
