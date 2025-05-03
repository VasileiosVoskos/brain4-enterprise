import streamlit as st, pytesseract, os
from PIL import Image
from openai import OpenAI
st.header("🧾 OCR & ΚΟΚ Analyzer")
client = OpenAI(api_key=st.secrets["openai"]["openai_api_key"])
img = st.file_uploader("Upload image", ["jpg", "png", "jpeg"])
if img:
    im = Image.open(img); st.image(im, use_column_width=True)
    text = pytesseract.image_to_string(im, lang="ell")
    st.text_area("OCR:", text, height=200)
    if st.button("Analyze KOK"):
        rsp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Είσαι ειδικός ΚΟΚ"},
                {"role": "user", "content": text},
            ],
        )
        st.success(rsp.choices[0].message.content)
# Placeholder for ocr_ai.py
