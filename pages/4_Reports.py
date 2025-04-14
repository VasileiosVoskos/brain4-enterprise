from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

# ✅ Προσθήκη Unicode γραμματοσειράς
pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
pdf.set_font("DejaVu", size=12)

pdf.cell(200, 10, txt="brain4 Enterprise Report", ln=True, align='C')

for col in df.columns:
    values = ', '.join(map(str, df[col].astype(str).unique()[:5]))
    pdf.multi_cell(0, 10, f"{col}: {values}")

pdf.output("brain4_report.pdf")
st.success("Το PDF δημιουργήθηκε επιτυχώς!")
with open("brain4_report.pdf", "rb") as f:
    st.download_button("📥 Κατέβασε το PDF Report", f, file_name="brain4_report.pdf")
