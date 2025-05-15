import importlib, json, os, streamlit as st, time
from pathlib import Path
from openai import OpenAI

# Basic page settings
st.set_page_config(page_title="brain4 Enterprise", layout="wide")

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
    """Login / Register with invite codes - stored in JSON."""
    st.sidebar.image("assets/logo.png", width=160)
    users, invites = load(USERS), load(INV)

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        st.sidebar.success(f"👋 Welcome {st.session_state.user}")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.experimental_rerun()
        return True

    tab_login, tab_reg = st.tabs(["🔑 Login", "🆕 Register"])

    # --- login
    with tab_login:
        u = st.text_input("Username", key="login_username")
        p = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if u in users and users[u]["pwd"] == p:
                st.session_state.user = u
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    # --- register
    with tab_reg:
        u = st.text_input("New username", key="reg_username")
        p = st.text_input("New password", type="password", key="reg_password")
        code = st.text_input("Invite code")
        if st.button("Register"):
            if u in users:
                st.error("Username already exists")
            elif code in invites:
                users[u] = {
                    "pwd": p,
                    "role": "admin" if code == "ADMINCODE" else "user",
                    "created_at": str(int(time.time()))
                }
                dump(USERS, users)
                st.success("Account created successfully! Please login.")
            else:
                st.error("Invalid invite code")
    st.stop()

# Run authentication
auth()

# Navigation Structure
SECTIONS = {
    "Car": [
        "pages.car.dashboard",
        "pages.car.upload",
        "pages.car.ai",
        "pages.car.reports"
    ],
    "Legal": [
        "pages.legal.upload",
        "pages.legal.ai",
        "pages.legal.reports"
    ],
    "Alerts": ["pages.alerts.live"],
    "OCR": ["pages.ocr.ocr_ai"]  # Updated to match your actual file
}

page_labels = {
    "pages.car.dashboard": "Dashboard",
    "pages.car.upload": "Upload & Analysis",
    "pages.car.ai": "AI Advisor",
    "pages.car.reports": "Reports",
    "pages.legal.upload": "Upload & Analysis",
    "pages.legal.ai": "Legal AI",
    "pages.legal.reports": "Reports",
    "pages.alerts.live": "Live Alerts",
    "pages.ocr.ocr_ai": "OCR Analyser"  # Updated to match your actual file
}

# Navigation UI
section = st.sidebar.selectbox("Section", list(SECTIONS.keys()))
page_key = st.sidebar.selectbox(
    "Page",
    SECTIONS[section],
    format_func=lambda k: page_labels.get(k, k)
)

# Load and run the selected module
try:
    module_name = page_key.replace("/", ".")
    importlib.import_module(module_name)
except Exception as e:
    st.error(f"Error loading page: {str(e)}")
    st.info("Please check if all required files exist")
