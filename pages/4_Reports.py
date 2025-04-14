import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import sendgrid
from sendgrid.helpers.mail import Mail

st.title("📄 Reports")

# 🔥 Secrets
SENDGRID_API_KEY = st.secrets["sendgrid"]["sendgrid_api_key"]
FROM_EMAIL = st.secrets["sendgrid"]["sender_email"]
TO_EMAIL = st.secrets["sendgrid"]["receiver_email"]

# ✅ Διαβάζουμε το αποθηκευμένο dataset
if os.path.exists("uploaded_data.csv"):
    df = pd.read_csv("uploaded_data.csv")

    st.subheader("Δημιουργία Report σε PDF")
    if st.button("Δημιουργία PDF Report"):
        try:
            pdf = FPDF()
            pdf.add_page()

            # ✅ Χρήση Unicode γραμματοσειράς από το assets
            font_path = os.path.join("assets", "DejaVuSans.ttf")
            pdf.add_font('DejaVu', '', font_path, uni=True)
            pdf.set_font("DejaVu", size=12)

            pdf.cell(200, 10, txt="brain4 Enterprise Report", ln=True, align='C')

            for col in df.columns:
                values = ', '.join(map(str, df[col].astype(str).unique()[:5]))
                pdf.multi_cell(0, 10, f"{col}: {values}")

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
