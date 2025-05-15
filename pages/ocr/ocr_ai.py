import streamlit as st
import pytesseract
from PIL import Image
from openai import OpenAI

st.header("🧾 OCR & Document Analysis")

# Upload Section
st.markdown("### 📑 Document Upload")

doc_type = st.selectbox(
    "Document Type",
    ["Invoice", "Receipt", "Contract", "ID Document", "Form"]
)

img = st.file_uploader(
    "Upload Document",
    type=['pdf', 'png', 'jpg', 'jpeg']
)

if img:
    try:
        im = Image.open(img)
        st.image(im, use_container_width=True)  # Using the correct parameter
        
        text = pytesseract.image_to_string(im, lang="ell")
        st.text_area("Extracted Text:", text, height=200)
        
        if st.button("Analyze Document"):
            try:
                client = OpenAI(api_key=st.secrets["openai"]["openai_api_key"])
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a document analysis expert"},
                        {"role": "user", "content": text},
                    ]
                )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

# Document Statistics
st.markdown("### 📊 Processing Statistics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Documents Processed", "45", "+3")
with col2:
    st.metric("Success Rate", "98%", "+1%")
with col3:
    st.metric("Average Processing Time", "2.3s", "-0.1s")
