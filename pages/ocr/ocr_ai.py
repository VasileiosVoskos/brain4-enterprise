import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.markdown("## Document Processing Center")

# Upload Section
st.markdown("### 📑 Document Upload")

doc_type = st.selectbox(
    "Document Type",
    ["Invoice", "Receipt", "Contract", "ID Document", "Form"]
)

uploaded_files = st.file_uploader(
    "Upload Documents for Processing",
    accept_multiple_files=True,
    type=['pdf', 'png', 'jpg', 'jpeg']
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} documents uploaded for processing")
    
    # Processing Status
    st.markdown("### 🔄 Processing Status")
    for file in uploaded_files:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.text(file.name)
        with col2:
            st.success("Processed")
        with col3:
            st.button("View Results", key=file.name)

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
            ["English", "Spanish", "French", "German", "Chinese"]
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
