import streamlit as st
import json
import bcrypt
import os
from datetime import datetime

st.set_page_config(page_title="brain4 Access", layout="centered")

# Load assets
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .glass {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    </style>
""", unsafe_allow_html=True)

st.image("assets/logo.png", width=160)

if "mode" not in st.session_state:
    st.session_state.mode = "login"

# Load data
USERS_PATH = "data/users.json"
INVITES_PATH = "data/invite_codes.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def load_invites():
    if not os.path.exists(INVITES_PATH):
        return {}
    with open(INVITES_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

def save_invites(data):
    with open(INVITES_PATH, "w") as f:
        json.dump(data, f, indent=4)

def login(email, password):
    users = load_users()
    user = users.get(email)
    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        st.session_state.user = user
        st.success("✅ Είσοδος επιτυχής!")
        st.rerun()
    else:
        st.error("❌ Λάθος στοιχεία.")

def register(email, password, code):
    users = load_users()
    invites = load_invites()

    if email in users:
        st.warning("Ο χρήστης υπάρχει ήδη.")
        return

    invite = invites.get(code)
    if not invite:
        st.error("Μη έγκυρος κωδικός.")
        return

    if invite["status"] != "active":
        st.error("Ο invite code δεν είναι ενεργός.")
        return

    if invite["max_uses"] is not None and invite["uses"] >= invite["max_uses"]:
        st.error("Ο invite code έχει χρησιμοποιηθεί ήδη.")
        return

    if invite["expires"] and datetime.now().timestamp() > invite["expires"]:
        st.error("Ο invite code έχει λήξει.")
        invite["status"] = "expired"
        save_invites(invites)
        return

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[email] = {"email": email, "password": hashed_pw, "role": invite["role"]}
    invite["uses"] += 1
    if invite["max_uses"] is not None and invite["uses"] >= invite["max_uses"]:
        invite["status"] = "used"

    save_users(users)
    save_invites(invites)
    st.success("✅ Εγγραφή επιτυχής! Τώρα μπορείς να συνδεθείς.")
    st.session_state.mode = "login"

with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    if st.session_state.mode == "login":
        st.subheader("🔐 Είσοδος")
        email = st.text_input("Email")
        password = st.text_input("Κωδικός", type="password")
        if st.button("Είσοδος"):
            login(email, password)
        st.markdown("Δεν έχεις λογαριασμό; [Κάνε εγγραφή](#)", unsafe_allow_html=True)
        if st.button("➕ Μετάβαση σε Εγγραφή"):
            st.session_state.mode = "register"

    elif st.session_state.mode == "register":
        st.subheader("🆕 Εγγραφή με Invite")
        email = st.text_input("Email για εγγραφή")
        password = st.text_input("Κωδικός", type="password")
        code = st.text_input("Invite Code")
        if st.button("Εγγραφή"):
            register(email, password, code)
        if st.button("⬅️ Επιστροφή σε Login"):
            st.session_state.mode = "login"

    st.markdown('</div>', unsafe_allow_html=True)

