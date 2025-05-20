import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
from utils.helpers import load_json, save_json, get_current_time
from utils.config import LEGAL_DIR

def show():
    st.title("Legal Document AI Analysis")
    
    # File upload section
    st.header("Upload Legal Documents")
    uploaded_file = st.file_uploader(
        "Upload legal document",
        type=['pdf', 'docx', 'txt'],
        help="Upload your legal document for analysis"
    )
    
    if uploaded_file:
        try:
            # Save the file
            file_path = LEGAL_DIR / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"File {uploaded_file.name} uploaded successfully!")
            
            # Document analysis section
            st.header("Document Analysis")
            
            if st.button("Analyze Document"):
                with st.spinner("Analyzing document..."):
                    # Simulate document analysis
                    analysis_results = {
                        'document_type': 'Contract',
                        'key_entities': [
                            'Party A',
                            'Party B',
                            'Effective Date',
                            'Termination Clause'
                        ],
                        'risk_level': 'Medium',
                        'key_points': [
                            'Standard contract terms',
                            'Clear termination conditions',
                            'Standard liability clauses'
                        ],
                        'recommendations': [
                            'Review termination clause',
                            'Verify party information',
                            'Check for compliance with regulations'
                        ]
                    }
                    
                    # Save analysis results
                    save_json('data/legal_analysis.json', {
                        'timestamp': str(get_current_time()),
                        'filename': uploaded_file.name,
                        'analysis': analysis_results
                    })
                    
                    # Display results
                    st.subheader("Document Type")
                    st.info(analysis_results['document_type'])
                    
                    st.subheader("Key Entities")
                    for entity in analysis_results['key_entities']:
                        st.write(f"• {entity}")
                    
                    st.subheader("Risk Assessment")
                    risk_color = {
                        'Low': 'green',
                        'Medium': 'orange',
                        'High': 'red'
                    }
                    st.markdown(f"<h3 style='color: {risk_color[analysis_results['risk_level']]}'>"
                              f"Risk Level: {analysis_results['risk_level']}</h3>",
                              unsafe_allow_html=True)
                    
                    st.subheader("Key Points")
                    for point in analysis_results['key_points']:
                        st.write(f"• {point}")
                    
                    st.subheader("Recommendations")
                    for rec in analysis_results['recommendations']:
                        st.success(rec)
                    
                    # Generate visualizations
                    st.subheader("Document Analysis Visualization")
                    
                    # Create a sample visualization
                    data = {
                        'Category': ['Clarity', 'Completeness', 'Risk', 'Compliance'],
                        'Score': [85, 90, 75, 88]
                    }
                    df = pd.DataFrame(data)
                    
                    fig = px.bar(
                        df,
                        x='Category',
                        y='Score',
                        title='Document Quality Metrics',
                        color='Score',
                        color_continuous_scale='RdYlGn'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    # Historical Analysis Section
    st.header("Historical Analysis")
    
    try:
        historical_data = load_json('data/legal_analysis.json')
        if historical_data:
            st.subheader("Previous Analysis")
            st.write(f"Last analyzed document: {historical_data['filename']}")
            st.write(f"Analysis timestamp: {historical_data['timestamp']}")
            
            # Display previous analysis results
            st.subheader("Previous Analysis Results")
            for key, value in historical_data['analysis'].items():
                if isinstance(value, list):
                    st.write(f"**{key.replace('_', ' ').title()}:**")
                    for item in value:
                        st.write(f"• {item}")
                else:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    except:
        st.info("No previous analysis available")
