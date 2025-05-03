import streamlit as st
from pathlib import Path
import json, importlib, sys, os

# ───────────────── Glassmorphism CSS ─────────────────
st.markdown(
    """
    <style>
    section[data-testid='stSidebar'] > div:first-child{
        background:rgba(255,255,255,.15)!important;
        backdrop-filter:blur(12px)!important;border-right:1px
        solid rgba(255,255,255,.25);}
    [data-testid="stAppViewContainer"]>.main{
        background:linear-gradient(135deg,#dff1ff 0%,#f4fafe 100%);
        animation:grad 15s ease infinite;background-size:400% 400%;}
    @keyframes grad{0%{background-position:0% 50%}
      50%{background-position:100% 50%}100%{background-position:0% 50%}}
    .glass-card{padding:1.2rem 1.6rem;border-radius:22px;
      background:rgba(255,255,255,.25);backdrop-filter:blur(6px);
      box-shadow:0 8px 32px rgba(31,38,135,.2);border:1px solid rgba(255,255,255,.25);
      transition:.3s} .glass-card:hover{transform:translateY(-4px);
      box-shadow:0 12px 40px rgba(31,38,135,.25)}
    header,footer{visibility:hidden}
    </style>
    """,
    unsafe_allow_html=True,
)

# ───────────────── Auth helpers ─────────────────
USERS = Path("data/users.json")
INV   = Path("data/invite_codes.json")
USERS.parent.mkdir(parents=True, exist_ok=True)
if not USERS.exists(): USERS.write_text("{}")
if not INV.exists():   INV.write_text(json.dumps({"ADMINCODE": "admin"}))

load = lambda p: json.loads(p.read_text())
save = lambda p,d: p.write_text(json.dumps(d, indent=2))

def auth():
    st.sidebar.image("assets/logo.png", width=160)
    mode = st.sidebar.radio("Auth", ["Login", "Register"], horizontal=True)

    users, invites = load(USERS), load(INV)
    if mode == "Login":
        u = st.sidebar.text_input("User")
        p = st.sidebar.text_input("Pass", type="password")
        if st.sidebar.button("Login"):
            if u in users and users[u]["pw"] == p:
                st.session_state.user = u
                st.session_state.role = users[u]["role"]
            else:
                st.sidebar.error("❌")
    else:
        u = st.sidebar.text_input("New user")
        p = st.sidebar.text_input("Pass", type="password")
        code = st.sidebar.text_input("Invite")
        if st.sidebar.button("Register"):
            if code in invites:
                users[u] = {"pw": p, "role": invites[code]}
                save(USERS, users)
                st.sidebar.success("🎉 Τώρα κάνε Login")
            else:
                st.sidebar.error("Invalid invite")

auth()
if "user" not in st.session_state:
    st.stop()

# ───────────────── Navigation ─────────────────
sections = {
    "Car":   ["Dashboard", "Upload", "AI", "Reports"],
    "Legal": ["Upload", "AI", "Reports"],
    "Alerts":["Live"],
    "OCR":   ["OCR & KOK"],
}
sec  = st.sidebar.selectbox("Section", list(sections))
page = st.sidebar.selectbox("Page",   sections[sec])

module = (
    "pages."
    + sec.lower()
    + "."
    + page.lower().replace(" & ", "_").replace(" ", "_")
)
if module not in sys.modules:
    importlib.import_module(module)
else:
    importlib.reload(sys.modules[module])

st.sidebar.caption(f"👤 {st.session_state.user}")
# Placeholder for app.py
