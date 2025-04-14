import streamlit as st
from PIL import Image
from openai import OpenAI
import pandas as pd
import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import sendgrid
from sendgrid.helpers.mail import Mail

# Set up page config
st.set_page_config(page_title="brain4 Enterprise", layout="wide")

# Load logo
logo = Image.open("assets/logo.png")
st.sidebar.image(logo, use_column_width=True)

# Sidebar navigation
page = st.sidebar.selectbox("Επιλογή Σελίδας", ("Dashboard", "Ανέβασμα & Ανάλυση", "AI Σύμβουλος", "Reports", "Settings"))

# OpenAI API setup
client = OpenAI(api_key=st.secrets["openai"]["openai_api_key"])

# Email setup
SENDGRID_API_KEY = st.secrets["sendgrid"]["sendgrid_api_key"]
FROM_EMAIL = st.secrets["sendgrid"]["sender_email"]
TO_EMAIL = st.secrets["sendgrid"]["receiver_email"]

# App pages
if page == "Dashboard":
    st.title("📊 Dashboard")
    st.write("Καλώς ήρθες στο brain4 Enterprise Dashboard!")

elif page == "Ανέβασμα & Ανάλυση":
    st.title("📁 Ανέβασμα & Ανάλυση Δεδομένων")
    uploaded_file = st.file_uploader("Ανέβασε το αρχείο Excel", type=["xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.subheader("📊 Τα δεδομένα σου:")
            st.dataframe(df)

            st.subheader("📈 Ανάλυση Δεδομένων")
            st.bar_chart(df.select_dtypes(include=['number']))

            df.to_csv("uploaded_data.csv", index=False)

        except Exception as e:
            st.error(f"Προέκυψε πρόβλημα με το αρχείο: {e}")

elif page == "AI Σύμβουλος":
    st.title("🤖 AI Σύμβουλος")

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

elif page == "Reports":
    st.title("📄 Reports")
    if os.path.exists("uploaded_data.csv"):
        df = pd.read_csv("uploaded_data.csv")

        st.subheader("Δημιουργία Report σε PDF")
        if st.button("Δημιουργία PDF Report"):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("DejaVu", size=12)

                pdf.cell(200, 10, txt="brain4 Enterprise Report", ln=True, align='C')

                for col in df.columns:
                    pdf.cell(200, 10, txt=f"{col}: {df[col].astype(str).unique()[:5]}", ln=True)

                pdf.output("brain4_report.pdf")
                st.success("Το PDF δημιουργήθηκε επιτυχώς!")
                with open("brain4_report.pdf", "rb") as f:
                    st.download_button("📥 Κατέβασε το PDF Report", f, file_name="brain4_report.pdf")

            except Exception as e:
                st.error(f"Προέκυψε πρόβλημα με το αρχείο: {e}")

        st.subheader("Αποστολή Report μέσω Email")
        if st.button("Αποστολή Report"):
            try:
                message = Mail(
                    from_email=FROM_EMAIL,
                    to_emails=TO_EMAIL,
                    subject='brain4 Enterprise Report',
                    html_content='<strong>Δες το επισυναπτόμενο Report.</strong>'
                )
                with open("brain4_report.pdf", "rb") as f:
                    message.add_attachment(f.read(), maintype='application', subtype='pdf', filename='brain4_report.pdf')

                sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
                response = sg.send(message)

                if response.status_code == 202:
                    st.success("Το email στάλθηκε επιτυχώς!")
                else:
                    st.error(f"Σφάλμα κατά την αποστολή email: {response.status_code}")

            except Exception as e:
                st.error(f"Σφάλμα κατά την αποστολή email: {e}")

    else:
        st.warning("Παρακαλώ ανέβασε πρώτα δεδομένα στην ενότητα 'Ανέβασμα & Ανάλυση'.")

elif page == "Settings":
    st.title("⚙️ Ρυθμίσεις")
    st.write("Διαχειρίσου τις ρυθμίσεις του brain4 Enterprise.")

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
