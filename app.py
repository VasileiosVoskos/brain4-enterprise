import importlib
import json
import os
import time
import streamlit as st
from pathlib import Path
from openai import OpenAI

# Professional page configuration
st.set_page_config(
    page_title="brain4 Enterprise",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data management setup
DATA_DIR = Path("data")
USERS = DATA_DIR / "users.json"
INV = DATA_DIR / "invite_codes.json"

# Create data directory if it doesn't exist
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)

# Initialize files if they don't exist
for f in (USERS, INV):
    if not f.exists():
        f.write_text("{}")

load = lambda p: json.loads(p.read_text())
dump = lambda p, d: p.write_text(json.dumps(d, indent=2, ensure_ascii=False))

def auth():
    """Secure authentication system with invite-based registration."""
    # Changed from use_column_width to use_container_width
    st.sidebar.image("assets/logo.png", width=160)  # Fixed width instead
    users, invites = load(USERS), load(INV)

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        user_info = users[st.session_state.user]
        st.sidebar.success(f"Welcome, {st.session_state.user}")
        if st.sidebar.button("Sign Out"):
            st.session_state.user = None
            st.experimental_rerun()
        return True

    st.markdown("## Welcome to brain4 Enterprise")
    st.markdown("Please sign in to access the platform.")

    tab_login, tab_reg = st.tabs(["🔑 Sign In", "🆕 Create Account"])

    # Login interface
    with tab_login:
        with st.form("login_form"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            if submit and u in users and users[u]["pwd"] == p:
                st.session_state.user = u
                st.experimental_rerun()
            elif submit:
                st.error("Invalid credentials")

    # Registration interface
    with tab_reg:
        with st.form("register_form"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            code = st.text_input("Invite Code")
            submit = st.form_submit_button("Register")
            if submit:
                if code in invites:
                    users[u] = {
                        "pwd": p,
                        "role": "admin" if code == "ADMINCODE" else "user",
                        "created_at": str(int(time.time()))
                    }
                    dump(USERS, users)
                    st.success("Account created! Please sign in.")
                else:
                    st.error("Invalid invite code")
    st.stop()

# Run authentication
auth()

# Navigation structure
SECTIONS = {
    "Fleet Management": [
        "pages.car.dashboard",
        "pages.car.ai",
        "pages.car.reports",
        "pages.car.upload"
    ],
    "Legal": [
        "pages.legal.ai",
        "pages.legal.reports",
        "pages.legal.upload"
    ],
    "Alerts": ["pages.alerts.live"],
    "OCR": ["pages.ocr.ocr_ai"]
}

# Navigation UI
section = st.sidebar.selectbox("Section", list(SECTIONS.keys()))
page_key = st.sidebar.selectbox("Page", SECTIONS[section])

# Load selected module
try:
    module_name = page_key.replace("/", ".")
    page_module = importlib.import_module(module_name)
except Exception as e:
    st.error(f"Error loading page: {str(e)}")
