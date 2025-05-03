import streamlit as st, pandas as pd, os
from openai import OpenAI
st.header("⚖️ Legal – AI Suggestions")
client = OpenAI(api_key=st.secrets["openai"]["openai_api_key"])
if os.path.exists("data/legal_data.csv"):
    df = pd.read_csv("data/legal_data.csv")
    st.dataframe(df.head())
    case = st.text_area("Περιγραφή υπόθεσης")
    if st.button("Πρόταση Αποζημίωσης"):
        rsp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Είσαι νομικός σύμβουλος"},
                {"role": "user", "content": case},
            ],
        )
        st.success(rsp.choices[0].message.content)
else:
    st.info("Upload legal excel first")
# Placeholder for ai.py
