import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

st.markdown("## AI Fleet Advisor")

# AI Insights Section
st.markdown("### 🤖 AI-Powered Insights")

# Real-time Analysis
col1, col2 = st.columns([2, 1])
with col1:
    st.info("🔄 **Real-time Fleet Analysis**\n\n"
            "AI system is actively monitoring 127 vehicles\n"
            "Last update: Just now")
    
with col2:
    st.metric("AI Confidence Score", "98%", "+2%")

# Predictive Maintenance
st.markdown("### 🔍 Predictive Maintenance Recommendations")

maintenance_predictions = pd.DataFrame({
    'Vehicle ID': ['TRK-001', 'VAN-023', 'CAR-115'],
    'Probability': [0.92, 0.87, 0.76],
    'Component': ['Brake System', 'Engine Oil', 'Battery'],
    'Recommended Action': ['Replace', 'Change', 'Inspect'],
    'Urgency': ['High', 'Medium', 'Low']
})

st.dataframe(
    maintenance_predictions.style.apply(lambda x: ['background: #ffcdd2' if x['Urgency'] == 'High' 
    else 'background: #fff59d' if x['Urgency'] == 'Medium'
    else 'background: #c8e6c9' for i in x], axis=1),
    hide_index=True,
    use_container_width=True
)

# Route Optimization
st.markdown("### 🛣️ Route Optimization")
tab1, tab2 = st.tabs(["Recommendations", "Efficiency Analysis"])

with tab1:
    st.markdown("""
    #### Today's Route Recommendations
    - **Route A**: Optimize for TRK-001, TRK-002 (Estimated savings: 12%)
    - **Route B**: Combine deliveries for VAN-023, VAN-024 (Estimated savings: 8%)
    - **Route C**: Adjust schedule for CAR-115 (Estimated savings: 5%)
    """)

with tab2:
    efficiency_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', end='2024-03-01', freq='D'),
        'Efficiency': [85 + i * 0.1 for i in range(60)]
    })
    fig = px.line(efficiency_data, x='Date', y='Efficiency', 
                  title='Route Efficiency Trends')
    st.plotly_chart(fig, use_container_width=True)

# Driver Behavior Analysis
st.markdown("### 👤 Driver Behavior Analysis")
driver_data = pd.DataFrame({
    'Metric': ['Safety Score', 'Fuel Efficiency', 'Schedule Adherence', 'Vehicle Care'],
    'Score': [92, 88, 95, 90],
    'Trend': ['+2%', '+1%', '-1%', '+3%']
})

for idx, row in driver_data.iterrows():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**{row['Metric']}**")
    with col2:
        st.progress(row['Score']/100)
    with col3:
        st.markdown(row['Trend'])

# AI Settings
with st.expander("AI Model Settings"):
    st.markdown("### Configure AI Parameters")
    col1, col2 = st.columns(2)
    with col1:
        st.slider("Prediction Confidence Threshold", 0.0, 1.0, 0.8)
        st.selectbox("Update Frequency", ["Real-time", "Hourly", "Daily"])
    with col2:
        st.multiselect("Active Monitoring Features", 
                      ["Maintenance Prediction", "Route Optimization", 
                       "Driver Behavior", "Fuel Efficiency"])
        st.checkbox("Enable Automated Alerts")
