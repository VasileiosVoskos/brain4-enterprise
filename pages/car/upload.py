# pages/car/upload.py
import streamlit as st
import pandas as pd
from datetime import datetime

st.markdown("## Document Management & Analysis")

# File Upload Section
st.markdown("### 📎 Upload Documents")

upload_type = st.selectbox(
    "Document Type",
    ["Vehicle Registration", "Insurance", "Maintenance Records", 
     "Driver Documents", "Inspection Reports"]
)

uploaded_files = st.file_uploader(
    "Upload Files", 
    accept_multiple_files=True,
    type=['pdf', 'docx', 'xlsx', 'jpg', 'png']
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} files uploaded successfully!")
    
    # Document Processing Status
    st.markdown("### 🔄 Processing Status")
    for file in uploaded_files:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.text(file.name)
        with col2:
            st.success("Processed")
        with col3:
            st.button("View", key=file.name)

# Document Organization
st.markdown("### 📁 Document Organization")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Quick Access Categories**")
    categories = {
        "Vehicle Documents": 45,
        "Insurance Papers": 23,
        "Maintenance Records": 67,
        "Driver Files": 34,
        "Inspection Reports": 12
    }
    
    for category, count in categories.items():
        st.button(f"{category} ({count})", use_container_width=True)

with col2:
    st.markdown("**Recent Uploads**")
    recent_docs = pd.DataFrame({
        'Document': ['Vehicle Reg - TRK001', 'Insurance - Fleet', 'Maintenance Log'],
        'Date': ['2024-03-01', '2024-02-28', '2024-02-27'],
        'Status': ['Verified', 'Pending', 'Verified']
    })
    st.dataframe(recent_docs, hide_index=True)

# Document Analysis
st.markdown("### 📊 Document Analysis")
tab1, tab2 = st.tabs(["Status Overview", "Expiration Tracking"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", "181", "+12")
    with col2:
        st.metric("Pending Review", "8", "-3")
    with col3:
        st.metric("Expiring Soon", "5", "+2")

with tab2:
    expiring_docs = pd.DataFrame({
        'Document': ['Insurance - VAN023', 'License - Driver004', 'Reg - TRK001'],
        'Expiration': ['2024-04-15', '2024-04-20', '2024-05-01'],
        'Days Left': [45, 50, 61]
    })
    st.dataframe(expiring_docs, hide_index=True)

# Batch Operations
st.markdown("### 🔧 Batch Operations")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Download Selected", use_container_width=True)
with col2:
    st.button("Share Selected", use_container_width=True)
with col3:
    st.button("Archive Selected", use_container_width=True)

# Settings
with st.expander("Document Management Settings"):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Default Category", list(categories.keys()))
        st.multiselect("Auto-categorize Rules", 
                      ["By Vehicle", "By Document Type", "By Date"])
    with col2:
        st.selectbox("Storage Location", ["Cloud Storage", "Local Server"])
        st.checkbox("Enable Auto-OCR")
