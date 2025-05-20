import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import pytesseract
from PIL import Image
import io
from utils.helpers import load_json, save_json, get_current_time
from utils.config import OCR_DIR

def show():
    st.title("OCR Document Analysis")
    
    # File upload section
    st.header("Upload Document")
    uploaded_file = st.file_uploader(
        "Upload image or PDF",
        type=['png', 'jpg', 'jpeg', 'pdf'],
        help="Upload document for OCR processing"
    )
    
    if uploaded_file:
        try:
            # Save the file
            file_path = OCR_DIR / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"File {uploaded_file.name} uploaded successfully!")
            
            # OCR Processing section
            st.header("OCR Processing")
            
            if st.button("Process Document"):
                with st.spinner("Processing document..."):
                    # Read the image
                    image = Image.open(uploaded_file)
                    
                    # Perform OCR
                    text = pytesseract.image_to_string(image)
                    
                    # Display results
                    st.subheader("Extracted Text")
                    st.text_area("OCR Result", text, height=200)
                    
                    # Save OCR results
                    ocr_results = {
                        'timestamp': str(get_current_time()),
                        'filename': uploaded_file.name,
                        'text': text,
                        'confidence': 0.85,  # Simulated confidence score
                        'language': 'eng',
                        'word_count': len(text.split())
                    }
                    
                    save_json('data/ocr_results.json', ocr_results)
                    
                    # Display statistics
                    st.subheader("OCR Statistics")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Word Count", ocr_results['word_count'])
                    with col2:
                        st.metric("Confidence", f"{ocr_results['confidence']*100:.1f}%")
                    with col3:
                        st.metric("Language", ocr_results['language'])
                    
                    # AI Analysis section
                    st.header("AI Analysis")
                    
                    # Simulate AI analysis
                    analysis_results = {
                        'document_type': 'Invoice',
                        'key_information': {
                            'date': '2024-03-15',
                            'amount': '$1,234.56',
                            'vendor': 'Sample Vendor Inc.'
                        },
                        'entities': [
                            'Invoice Number',
                            'Date',
                            'Amount',
                            'Vendor Name'
                        ],
                        'confidence_scores': {
                            'date': 0.95,
                            'amount': 0.98,
                            'vendor': 0.92
                        }
                    }
                    
                    # Display analysis results
                    st.subheader("Document Analysis")
                    
                    # Document type
                    st.info(f"Detected Document Type: {analysis_results['document_type']}")
                    
                    # Key information
                    st.subheader("Key Information")
                    for key, value in analysis_results['key_information'].items():
                        st.write(f"**{key.title()}:** {value}")
                    
                    # Entity confidence
                    st.subheader("Entity Confidence")
                    fig = px.bar(
                        x=list(analysis_results['confidence_scores'].keys()),
                        y=list(analysis_results['confidence_scores'].values()),
                        title="Entity Detection Confidence",
                        labels={'x': 'Entity', 'y': 'Confidence'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Save analysis results
                    save_json('data/ocr_analysis.json', {
                        'timestamp': str(get_current_time()),
                        'filename': uploaded_file.name,
                        'analysis': analysis_results
                    })
                    
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    # Historical Analysis Section
    st.header("Historical Analysis")
    
    try:
        historical_data = load_json('data/ocr_analysis.json')
        if historical_data:
            st.subheader("Previous Analysis")
            st.write(f"Last analyzed document: {historical_data['filename']}")
            st.write(f"Analysis timestamp: {historical_data['timestamp']}")
            
            # Display previous analysis results
            st.subheader("Previous Analysis Results")
            for key, value in historical_data['analysis'].items():
                if isinstance(value, dict):
                    st.write(f"**{key.replace('_', ' ').title()}:**")
                    for subkey, subvalue in value.items():
                        st.write(f"• {subkey}: {subvalue}")
                elif isinstance(value, list):
                    st.write(f"**{key.replace('_', ' ').title()}:**")
                    for item in value:
                        st.write(f"• {item}")
                else:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    except:
        st.info("No previous analysis available")
