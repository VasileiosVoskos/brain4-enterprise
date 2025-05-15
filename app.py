import importlib, json, os, streamlit as st
from pathlib import Path
from openai import OpenAI

# ▸ Βασικές ρυθμίσεις σελίδας
st.set_page_config(page_title="brain4 Enterprise", layout="wide")

# --------- 1. Very-simple Auth (JSON) ------------------------------
DATA_DIR = Path("data")
USERS = DATA_DIR / "users.json"
INV   = DATA_DIR / "invite_codes.json"
for f in (USERS, INV):
    if not f.exists():
        f.write_text("{}")

load  = lambda p: json.loads(p.read_text())
dump  = lambda p,d: p.write_text(json.dumps(d, indent=2, ensure_ascii=False))

def auth():
    """Login / Register με invite codes — αποθηκεύονται σε JSON."""
    st.sidebar.image("assets/logo.png", width=160)
    users, invites = load(USERS), load(INV)

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        st.sidebar.success(f"👋 Καλωσήρθες {st.session_state.user}")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.experimental_rerun()
        return True

    tab_login, tab_reg = st.tabs(["🔑 Login", "🆕 Register"])

    # --- login
    with tab_login:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login") and u in users and users[u]["pwd"] == p:
            st.session_state.user = u
            st.experimental_rerun()

    # --- register
    with tab_reg:
        u = st.text_input("Νέο username")
        p = st.text_input("Νέο password", type="password")
        code = st.text_input("Invite code")
        if st.button("Register"):
            if code in invites:
                users[u] = {"pwd": p, "role": "admin" if code == "ADMINCODE" else "user"}
                dump(USERS, users)
                st.success("Ο λογαριασμός δημιουργήθηκε · κάνε login!")
            else:
                st.error("Μη έγκυρο invite code")
    st.stop()

auth()  # αν δεν γίνει login σταματάει εδώ

# --------- 2. Sidebar Navigation -----------------------------------
SECTIONS = {
    "Car":   ["pages.car.dashboard",
              "pages.car.upload",
              "pages.car.ai",
              "pages.car.reports"],
    "Legal": ["pages.legal.upload",
              "pages.legal.ai",
              "pages.legal.reports"],
    "Alerts": ["pages.alerts.live"],
    "OCR":   ["pages.ocr.analyser"],
}

page_labels = {
    "pages.car.dashboard":     "Dashboard",
    "pages.car.upload":        "Upload & Analysis",
    "pages.car.ai":            "AI Advisor",
    "pages.car.reports":       "Reports",
    "pages.legal.upload":      "Upload & Analysis",
    "pages.legal.ai":          "Legal AI",
    "pages.legal.reports":     "Reports",
    "pages.alerts.live":       "Live Alerts",
    "pages.ocr.analyser":      "OCR Analyser",
}

section = st.sidebar.selectbox("Section", list(SECTIONS.keys()))
page_key = st.sidebar.selectbox(
    "Page", SECTIONS[section],
    format_func=lambda k: page_labels.get(k, k)
)

# --------- 3. Load & run το ζητούμενο sub-module -------------------
module_name = page_key.replace("/", ".")
importlib.import_module(module_name)
