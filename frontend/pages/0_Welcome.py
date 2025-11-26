import streamlit as st

st.set_page_config(page_title="AIPS — Welcome", page_icon="🤖", layout="wide")

# --- hide streamlit menu / header ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Center layout
st.markdown(
    """
    <div style="text-align:center; padding-top:120px; font-family:monospace;">
        <h1 style="color:white;">AIPS</h1>
        <h2 style="color:#10b981; font-weight:400; margin-top:-10px;">
            AI Interview Preparation System
        </h2>
        <p style="color:#9ca3af; margin-top:20px;">
            Your Personalized AI‑Powered Interview Practice Assistant
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")

# Buttons centered
col1, col2, col3 = st.columns([1,1,1])

with col2:
    register = st.button("Register")
    login = st.button("Login")

# Handle clicks
if register:
    st.session_state["auth_mode"] = "register"
    st.experimental_rerun()

if login:
    st.session_state["auth_mode"] = "login"
    st.experimental_rerun()

# --- Simple forms under welcome ---
if st.session_state.get("auth_mode") == "register":
    st.subheader("Create your account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        st.success("Account created (demo only)")

if st.session_state.get("auth_mode") == "login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        st.success("Logged in (demo only)")