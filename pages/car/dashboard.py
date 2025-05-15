# pages/car/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.markdown("## Fleet Management Dashboard")

# Dashboard Layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Vehicles",
        "127",
        "+3 this month",
        help="Total number of vehicles in fleet"
    )

with col2:
    st.metric(
        "Active Vehicles",
        "112",
        "-2 from yesterday",
        help="Currently active vehicles"
    )

with col3:
    st.metric(
        "Maintenance Due",
        "15",
        "+5",
        help="Vehicles due for maintenance"
    )

with col4:
    st.metric(
        "Fuel Efficiency",
        "92%",
        "+2%",
        help="Fleet-wide fuel efficiency"
    )

# Fleet Status Overview
st.markdown("### Fleet Status Overview")
status_data = {
    'Status': ['Active', 'Maintenance', 'Repair', 'Idle'],
    'Count': [112, 8, 4, 3]
}
fig = px.pie(status_data, values='Count', names='Status', title='Fleet Status Distribution')
st.plotly_chart(fig, use_container_width=True)

# Vehicle Analytics
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Maintenance Schedule")
    maintenance_data = {
        'Vehicle': ['Truck 001', 'Van 023', 'Car 115', 'Truck 042', 'Van 007'],
        'Due Date': ['2024-03-15', '2024-03-18', '2024-03-20', '2024-03-22', '2024-03-25'],
        'Type': ['Regular', 'Extended', 'Regular', 'Regular', 'Extended']
    }
    st.dataframe(pd.DataFrame(maintenance_data), hide_index=True)

with col2:
    st.markdown("### Recent Alerts")
    alerts_data = {
        'Time': ['10:30 AM', '09:15 AM', '08:45 AM', '08:00 AM'],
        'Vehicle': ['Van 023', 'Truck 001', 'Car 115', 'Van 007'],
        'Alert': ['Low Fuel', 'Service Due', 'GPS Offline', 'Battery Low']
    }
    st.dataframe(pd.DataFrame(alerts_data), hide_index=True)

# Performance Metrics
st.markdown("### Performance Metrics")
tab1, tab2, tab3 = st.tabs(["Fuel Efficiency", "Maintenance Costs", "Utilization"])

with tab1:
    # Sample fuel efficiency data
    dates = pd.date_range(start='2024-01-01', end='2024-03-01', freq='D')
    efficiency = pd.DataFrame({
        'Date': dates,
        'Efficiency': [85 + i * 0.1 + np.random.randn() * 2 for i in range(len(dates))]
    })
    fig = px.line(efficiency, x='Date', y='Efficiency', title='Fleet Fuel Efficiency Trend')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Sample maintenance cost data
    costs = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar'],
        'Planned': [12000, 15000, 13000],
        'Unplanned': [3000, 2000, 4000]
    })
    fig = px.bar(costs, x='Month', y=['Planned', 'Unplanned'], title='Maintenance Costs')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Sample utilization data
    util = pd.DataFrame({
        'Vehicle Type': ['Trucks', 'Vans', 'Cars'],
        'Utilization': [85, 78, 92]
    })
    fig = px.bar(util, x='Vehicle Type', y='Utilization', title='Fleet Utilization (%)')
    st.plotly_chart(fig, use_container_width=True)

# Settings and Filters (collapsible)
with st.expander("Dashboard Settings"):
    st.markdown("### Configure Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last Quarter", "Year to Date"])
        st.multiselect("Vehicle Types", ["All", "Trucks", "Vans", "Cars"])
    with col2:
        st.selectbox("Refresh Rate", ["5 minutes", "15 minutes", "30 minutes", "1 hour"])
        st.multiselect("Metrics to Display", ["Fuel Efficiency", "Maintenance", "Utilization", "Costs"])
