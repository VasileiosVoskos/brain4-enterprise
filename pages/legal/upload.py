# pages/legal/upload.py
import streamlit as st
import pandas as pd
from datetime import datetime

st.markdown("## Legal Document Management")

# Upload Section
st.markdown("### 📤 Document Upload")

doc_type = st.selectbox(
    "Document Type",
    ["Contract", "Agreement", "Policy", "License", "Regulatory Filing"]
)

uploaded_files = st.file_uploader(
    "Upload Legal Documents",
    accept_multiple_files=True,
    type=['pdf', 'docx', 'txt']
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} documents uploaded successfully!")
    
    # Processing Status
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
st.markdown("### 📁 Document Library")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Categories**")
    categories = {
        "Contracts": 45,
        "Agreements": 32,
        "Policies": 18,
        "Licenses": 24,
        "Regulatory": 15
    }
    
    for category, count in categories.items():
        st.button(f"{category} ({count})", use_container_width=True)

with col2:
    st.markdown("**Recent Documents**")
    recent_docs = pd.DataFrame({
        'Document': ['Service Agreement', 'Privacy Policy', 'License'],
        'Date': ['2024-03-01', '2024-02-28', '2024-02-27'],
        'Status': ['Active', 'Under Review', 'Active']
    })
    st.dataframe(recent_docs, hide_index=True)

# Document Tracking
st.markdown("### 📊 Document Status")
tab1, tab2 = st.tabs(["Overview", "Expiration Tracking"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", "134", "+5")
    with col2:
        st.metric("Pending Review", "7", "-2")
    with col3:
        st.metric("Expiring Soon", "3", "+1")

with tab2:
    expiring_docs = pd.DataFrame({
        'Document': ['License A', 'Contract B', 'Agreement C'],
        'Expiration': ['2024-04-15', '2024-04-30', '2024-05-15'],
        'Days Left': [45, 60, 75]
    })
    st.dataframe(expiring_docs, hide_index=True)

# Document Actions
st.markdown("### 🔧 Document Actions")
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
                      ["By Type", "By Department", "By Status"])
    with col2:
        st.selectbox("Storage Location", ["Secure Cloud", "Local Server"])
        st.checkbox("Enable Auto-Classification")
