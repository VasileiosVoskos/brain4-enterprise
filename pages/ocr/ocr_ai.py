import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytesseract
from PIL import Image
from openai import OpenAI

st.header("🧾 OCR & Document Analysis")

# Upload Section
st.markdown("### 📑 Document Upload")

doc_type = st.selectbox(
    "Document Type",
    ["Invoice", "Receipt", "Contract", "ID Document", "Form"]
)

img = st.file_uploader(
    "Upload Documents for Processing",
    type=['pdf', 'png', 'jpg', 'jpeg']
)

if img:
    im = Image.open(img)
    st.image(im, use_container_width=True)  # Using the correct parameter
    try:
        text = pytesseract.image_to_string(im, lang="ell")
        st.text_area("Extracted Text:", text, height=200)
        
        if st.button("Analyze Document"):
            with st.spinner("Analyzing..."):
                st.success("Analysis complete!")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

# OCR Analytics
st.markdown("### 📊 OCR Analytics")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Documents Processed", "1,234", "+12")
with col2:
    st.metric("Success Rate", "98.5%", "+0.5%")
with col3:
    st.metric("Avg. Processing Time", "2.3s", "-0.1s")
with col4:
    st.metric("Accuracy Score", "99.2%", "+0.3%")

# Detailed Analytics
tab1, tab2 = st.tabs(["Processing Statistics", "Quality Metrics"])

with tab1:
    # Processing stats
    stats_data = pd.DataFrame({
        'Document Type': ['Invoice', 'Receipt', 'Contract', 'ID', 'Form'],
        'Count': [450, 320, 280, 124, 60],
        'Avg. Time (s)': [2.1, 1.8, 2.5, 2.0, 2.2]
    })
    fig = px.bar(stats_data, x='Document Type', y='Count',
                 title='Documents Processed by Type')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Quality metrics
    quality_data = pd.DataFrame({
        'Metric': ['Character Accuracy', 'Word Accuracy', 'Layout Recognition'],
        'Score': [99.2, 98.8, 97.5],
        'Previous': [98.9, 98.5, 97.2]
    })
    st.dataframe(quality_data, hide_index=True, use_container_width=True)

# Recent Processing History
st.markdown("### 📜 Recent Processing History")
history = pd.DataFrame({
    'Document': ['invoice_001.pdf', 'receipt_123.jpg', 'contract_456.pdf'],
    'Type': ['Invoice', 'Receipt', 'Contract'],
    'Status': ['Completed', 'Completed', 'In Progress'],
    'Confidence': ['98%', '97%', '95%']
})
st.dataframe(history, hide_index=True, use_container_width=True)

# OCR Settings
with st.expander("OCR Settings"):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "OCR Engine",
            ["Standard", "Enhanced", "High Precision"]
        )
        st.multiselect(
            "Language Support",
            ["English", "Greek", "French", "German", "Spanish"]
        )
    with col2:
        st.selectbox(
            "Output Format",
            ["PDF", "JSON", "TXT", "XML"]
        )
        st.slider(
            "Quality Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.8
        )

# Batch Processing
st.markdown("### 🔧 Batch Operations")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Process All", use_container_width=True)
with col2:
    st.button("Download Results", use_container_width=True)
with col3:
    st.button("Clear Queue", use_container_width=True)

# Export Options
with st.expander("Export Settings"):
    col1, col2 = st.columns(2)
    with col1:
        st.multiselect(
            "Export Format",
            ["PDF with Text Layer", "Searchable PDF", "Plain Text", "JSON"]
        )
    with col2:
        st.multiselect(
            "Additional Processing",
            ["Table Detection", "Form Recognition", "Layout Analysis"]
        )
