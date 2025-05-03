import streamlit as st, pandas as pd, os
st.header("📑 Legal – Upload & Analysis")
up = st.file_uploader("Excel", ["xlsx"])
if up:
    df = pd.read_excel(up, engine="openpyxl")
    df.to_csv("data/legal_data.csv", index=False)
    st.success("Αποθηκεύτηκε!")
    st.dataframe(df)
# Placeholder for upload.py
