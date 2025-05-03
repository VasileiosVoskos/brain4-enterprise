import streamlit as st, pandas as pd, os
from openai import OpenAI
st.header("🤖 Car – AI Advisor")
client = OpenAI(api_key=st.secrets["openai"]["openai_api_key"])
if os.path.exists("data/car_data.csv"):
    df = pd.read_csv("data/car_data.csv")
    st.dataframe(df.head())
    q = st.text_area("Ερώτηση")
    if st.button("Ρώτα"):
        rsp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Είσαι σύμβουλος ζημιών αυτοκινήτων"},
                {"role": "user", "content": q},
            ],
        )
        st.success(rsp.choices[0].message.content)
else:
    st.info("Upload data first (Car → Upload)")
# Placeholder for ai.py
