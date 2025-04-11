import streamlit as st
import pandas as pd
import os

st.title("📁 Ανέβασμα & Ανάλυση Δεδομένων")

uploaded_file = st.file_uploader("Ανέβασε το αρχείο Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.subheader("📊 Τα δεδομένα σου:")
        st.dataframe(df)

        # Ανάλυση δεδομένων
        st.subheader("📈 Ανάλυση Δεδομένων")
        st.bar_chart(df.select_dtypes(include=['number']))

        # Αποθήκευση δεδομένων για άλλα pages
        df.to_csv("uploaded_data.csv", index=False)

        st.success("Το αρχείο ανέβηκε και αποθηκεύτηκε επιτυχώς!")

    except Exception as e:
        st.error(f"Προέκυψε πρόβλημα με το αρχείο: {e}")
else:
    st.info("Περιμένω να ανεβάσεις το αρχείο Excel για ανάλυση.")
