import streamlit as st, pandas as pd, os
st.header("🚗  Car – Dashboard")
if os.path.exists("data/car_data.csv"):
    df = pd.read_csv("data/car_data.csv")
    st.metric("Σύνολο Ζημιών", len(df))
    if "Ποσό" in df.columns:
        st.bar_chart(df["Ποσό"])
else:
    st.info("Upload data first (Car → Upload)")
# Placeholder for dashboard.py
