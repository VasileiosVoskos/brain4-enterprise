import streamlit as st, pandas as pd, os
st.header("📁 Car – Upload & Analysis")
up = st.file_uploader("Excel", ["xlsx"])
if up:
    df = pd.read_excel(up, engine="openpyxl")
    df.to_csv("data/car_data.csv", index=False)
    st.success("Αποθηκεύτηκε!")
    st.dataframe(df)
# Placeholder for upload.py
