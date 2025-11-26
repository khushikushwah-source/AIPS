import streamlit as st

st.set_page_config(page_title="...", page_icon="...", layout="wide")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        section[data-testid="stSidebar"] {display: none !important;}  /* hide sidebar */
        .block-container {padding-top: 1.5rem;}
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AIPS — Welcome", page_icon="🤖", layout="wide")
#from streamlit_extras.switch_page_button import switch_page  # agar tum extension use karna chaho
# hide Streamlit menu/header/footer
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- TOP RIGHT LOGIN + REGISTER BUTTONS ---
colA, colB, colC = st.columns([6, 1, 1])

with colB:
    login = st.button("Login")

with colC:
    register = st.button("Register")

if register:
    st.switch_page("pages/1_Register.py")

if login:
    st.switch_page("pages/2_Login.py")  
# --- HEADING CENTER AREA ---
st.markdown(
    """
    <div style="text-align:center; padding-top:80px; font-family:monospace;">
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

# Handle button actions
if login:
    st.session_state["auth_mode"] = "login"

if register:
    st.session_state["auth_mode"] = "register"

# LOGIN & REGISTER FORMS BELOW THE HERO
if st.session_state.get("auth_mode") == "login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        st.success("Logged in (demo only)")

if st.session_state.get("auth_mode") == "register":
    st.subheader("Create your account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        st.success("Account created (demo only)")
