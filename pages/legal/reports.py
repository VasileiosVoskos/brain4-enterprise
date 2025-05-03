import streamlit as st, pandas as pd, os
from fpdf import FPDF
st.header("📑 Legal – Reports")
if os.path.exists("data/legal_data.csv"):
    df = pd.read_csv("data/legal_data.csv")
    st.dataframe(df)
    if st.button("PDF Report"):
        pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Legal Report", ln=1, align="C")
        for col in df.columns:
            pdf.cell(200, 10, f"{col}: {', '.join(map(str, df[col].unique()[:3]))}", ln=1)
        pdf.output("legal_report.pdf")
        st.download_button("Download", open("legal_report.pdf","rb"), "legal_report.pdf")
else:
    st.info("Upload legal excel first")
# Placeholder for reports.py
