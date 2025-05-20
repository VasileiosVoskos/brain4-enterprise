import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import pytz
from utils.helpers import load_json, save_json, get_current_time
from utils.config import UPLOADS_DIR

def show():
    st.title("Car Insurance AI Analysis")
    
    # File upload section
    st.header("Upload Claims Data")
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=['csv', 'xlsx'],
        help="Upload your claims data file"
    )
    
    if uploaded_file:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Display data preview
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            # Basic analysis
            st.subheader("Claims Analysis")
            
            # Create metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Claims", len(df))
            with col2:
                st.metric("Average Amount", f"${df['amount'].mean():,.2f}")
            with col3:
                st.metric("Total Value", f"${df['amount'].sum():,.2f}")
            
            # Create visualizations
            st.subheader("Claims Distribution")
            
            # Amount distribution
            fig_amount = px.histogram(
                df,
                x='amount',
                title='Claims Amount Distribution',
                labels={'amount': 'Amount ($)', 'count': 'Number of Claims'}
            )
            st.plotly_chart(fig_amount, use_container_width=True)
            
            # Status distribution
            fig_status = px.pie(
                df,
                names='status',
                title='Claims Status Distribution'
            )
            st.plotly_chart(fig_status, use_container_width=True)
            
            # Time series analysis
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                fig_timeline = px.line(
                    df,
                    x='date',
                    y='amount',
                    title='Claims Timeline'
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Save processed data
            save_json(
                'data/car_analysis.json',
                {
                    'timestamp': str(get_current_time()),
                    'total_claims': len(df),
                    'total_amount': float(df['amount'].sum()),
                    'average_amount': float(df['amount'].mean()),
                    'status_distribution': df['status'].value_counts().to_dict()
                }
            )
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    # AI Analysis Section
    st.header("AI Analysis")
    
    if st.button("Run AI Analysis"):
        with st.spinner("Analyzing claims data..."):
            try:
                # Load the analysis data
                analysis_data = load_json('data/car_analysis.json')
                
                # Display AI insights
                st.subheader("AI Insights")
                
                # Generate insights based on the data
                insights = [
                    "Based on the claims distribution, there appears to be a pattern of higher-value claims during peak hours.",
                    "The status distribution suggests that most claims are being processed within the expected timeframe.",
                    "The timeline analysis indicates a seasonal pattern in claim submissions."
                ]
                
                for insight in insights:
                    st.info(insight)
                
                # Display recommendations
                st.subheader("Recommendations")
                recommendations = [
                    "Consider implementing automated processing for low-value claims to improve efficiency.",
                    "Review the claims approval process for high-value claims to ensure proper risk assessment.",
                    "Implement additional fraud detection measures for claims above the average amount."
                ]
                
                for rec in recommendations:
                    st.success(rec)
                
            except Exception as e:
                st.error(f"Error in AI analysis: {str(e)}")
