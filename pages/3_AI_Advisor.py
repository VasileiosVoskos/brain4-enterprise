import streamlit as st
import pandas as pd
import os
from openai import OpenAI

st.title("🤖 AI Σύμβουλος")

# OpenAI API setup
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Ανάγνωση αποθηκευμένων δεδομένων
if os.path.exists("uploaded_data.csv"):
    df = pd.read_csv("uploaded_data.csv")
    st.write("📊 Δεδομένα προς ανάλυση:")
    st.dataframe(df)

    prompt = st.text_area("Τι θα ήθελες να ρωτήσεις τον AI Σύμβουλο;")

    if st.button("Αποστολή Ερώτησης"):
        with st.spinner("Ανάλυση από τον AI Σύμβουλο..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Είσαι ένας ειδικός σύμβουλος για ασφαλιστικές και οικονομικές αναλύσεις."},
                        {"role": "user", "content": prompt}
                    ]
                )
                answer = response.choices[0].message.content
                st.success(answer)
            except Exception as e:
                st.error(f"Προέκυψε σφάλμα κατά την επικοινωνία με το AI: {e}")
else:
    st.warning("Παρακαλώ ανέβασε πρώτα δεδομένα στην ενότητα 'Ανέβασμα & Ανάλυση'.")
