import streamlit as st
from openai import OpenAI

st.title("⚙️ Ρυθμίσεις")
st.write("Διαχειρίσου τις ρυθμίσεις του brain4 Enterprise.")

client = OpenAI(api_key=st.secrets["openai"]["openai_api_key"])
SENDGRID_API_KEY = st.secrets["sendgrid_api_key"]

if st.button("🔄 Αναβάθμιση App"):
    st.info("Αυτή η λειτουργία δεν είναι ακόμα διαθέσιμη.")

if st.button("🧩 Έλεγχος Συνδέσεων API"):
    try:
        if client and SENDGRID_API_KEY:
            st.success("Οι συνδέσεις API λειτουργούν σωστά!")
        else:
            st.error("Πρόβλημα με τις συνδέσεις API.")
    except Exception as e:
        st.error(f"Πρόβλημα με τις συνδέσεις API: {e}")
