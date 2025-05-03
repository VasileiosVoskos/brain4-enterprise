import streamlit as st, pandas as pd, os
from fpdf import FPDF
st.header("📄 Car – Reports")

if os.path.exists("data/car_data.csv"):
    df = pd.read_csv("data/car_data.csv")
    st.dataframe(df)
    if st.button("PDF Report"):
        pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Car Report", ln=1, align="C")
        for col in df.columns:
            pdf.cell(200, 10, f"{col}: {', '.join(map(str, df[col].unique()[:3]))}", ln=1)
        pdf.output("car_report.pdf")
        st.download_button("Download", open("car_report.pdf","rb"), "car_report.pdf")
else:
    st.info("Upload data first (Car → Upload)")
# Placeholder for reports.py
