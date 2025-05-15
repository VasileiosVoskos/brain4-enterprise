import importlib, json, os, streamlit as st
from pathlib import Path
from openai import OpenAI
from datetime import datetime, timedelta

# Professional page configuration
st.set_page_config(
    page_title="brain4 Enterprise",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'brain4 Enterprise - Professional Business Intelligence Platform',
        'Get Help': 'mailto:support@brain4enterprise.com',
        'Report a bug': 'mailto:support@brain4enterprise.com'
    }
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 2.5rem;
    }
    .st-emotion-cache-16idsys p {
        font-size: 1.1rem;
    }
    .st-emotion-cache-1wmy9hl {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

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
    # Professional branding
    col1, col2 = st.sidebar.columns([1, 3])
    with col1:
        st.image("assets/logo.png", use_container_width=True)
    with col2:
        st.markdown("### brain4 Enterprise")
    
    users, invites = load(USERS), load(INV)

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        user_info = users[st.session_state.user]
        st.sidebar.success(f"Welcome, {st.session_state.user}")
        st.sidebar.info(f"Role: {user_info['role'].title()}")
        if st.sidebar.button("Sign Out"):
            st.session_state.user = None
            st.experimental_rerun()
        return True

    st.markdown("## Welcome to brain4 Enterprise")
    st.markdown("Please sign in to access the platform.")

    tab_login, tab_reg = st.tabs(["🔑 Sign In", "🆕 Create Account"])

    # Professional login interface
    with tab_login:
        with st.form("login_form"):
            st.markdown("### Sign In to Your Account")
            u = st.text_input("Username/Email")
            p = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In", use_container_width=True)
            if submit and u in users and users[u]["pwd"] == p:
                st.session_state.user = u
                st.experimental_rerun()
            elif submit:
                st.error("Invalid credentials. Please try again.")

    # Professional registration interface
    with tab_reg:
        with st.form("register_form"):
            st.markdown("### Create New Account")
            u = st.text_input("Username/Email")
            p = st.text_input("Set Password", type="password")
            p2 = st.text_input("Confirm Password", type="password")
            code = st.text_input("Enterprise Invitation Code")
            submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit:
                if u in users:
                    st.error("Username already exists.")
                elif p != p2:
                    st.error("Passwords do not match.")
                elif code in invites:
                    users[u] = {
                        "pwd": p,
                        "role": "admin" if code == "ADMINCODE" else "user",
                        "created_at": str(datetime.now())
                    }
                    dump(USERS, users)
                    st.success("✅ Account created successfully! Please sign in.")
                else:
                    st.error("Invalid invitation code. Please contact your administrator.")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("Need help? Contact support@brain4enterprise.com")
    st.stop()

# Run authentication
auth()

# Professional navigation structure
SECTIONS = {
    "Enterprise Dashboard": ["pages.dashboard.overview"],
    "Fleet Management": [
        "pages.car.dashboard",
        "pages.car.ai",
        "pages.car.reports",
        "pages.car.upload"
    ],
    "Document Center": [
        "pages.legal.ai",
        "pages.legal.reports",
        "pages.legal.upload"
    ],
    "Monitoring": [
        "pages.alerts.live"
    ],
    "Business Intelligence": [
        "pages.ocr.ocr_ai"
    ]
}

page_labels = {
    # Fleet Management
    "pages.car.dashboard": "Fleet Dashboard",
    "pages.car.ai": "AI Fleet Advisor",
    "pages.car.reports": "Fleet Reports",
    "pages.car.upload": "Document Upload",
    # Document Center
    "pages.legal.ai": "Legal AI Assistant",
    "pages.legal.reports": "Legal Reports",
    "pages.legal.upload": "Document Upload",
    # Monitoring
    "pages.alerts.live": "Live Alerts",
    # Business Intelligence
    "pages.ocr.ocr_ai": "Document Processing"
}

# Professional navigation UI
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
section = st.sidebar.selectbox(
    "Select Department",
    list(SECTIONS.keys()),
    key="nav_section"
)

page_key = st.sidebar.selectbox(
    "Select Function",
    SECTIONS[section],
    format_func=lambda k: page_labels.get(k, k),
    key="nav_page"
)

# Load selected module
try:
    module_name = page_key.replace("/", ".")
    page_module = importlib.import_module(module_name)
    
    # Display breadcrumb navigation
    st.markdown(f"**{section}** > {page_labels[page_key]}")
    st.markdown("---")
    
except Exception as e:
    st.error(f"Error loading page: {str(e)}")
    st.info("Please contact system administrator if this error persists.")
