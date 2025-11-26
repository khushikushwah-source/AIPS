import streamlit as st
from firebase_config import users_ref
from common_ui import setup_page

# ---------------- Page Setup ----------------
setup_page("Login", "pages/2_Login.py")

# ---------------- Form ----------------
email = st.text_input("Email")
password = st.text_input("Password", type="password")
error = st.empty()  # inline error placeholder

login_clicked = st.button("Login")

if login_clicked:
    error.empty()

    if not email or not password:
        error.markdown("<span style='color:#f87171;'>Enter both Email and Password.</span>", unsafe_allow_html=True)

    else:
        user_doc = users_ref.document(email).get()
        if not user_doc.exists:
            error.markdown("<span style='color:#f87171;'>This email is not registered.</span>", unsafe_allow_html=True)
        else:
            user_data = user_doc.to_dict()
            if user_data["password"] == password:
                st.success("Successfully Logged In 🎉")

                # store session for dashboard
                st.session_state["logged_in"] = True
                st.session_state["user"] = user_data

                # redirect to next page (create later)
                st.switch_page("pages/4_Dashboard.py")
            else:
                error.markdown("<span style='color:#f87171;'>Invalid Email or Password.</span>", unsafe_allow_html=True)

st.write("")
forgot = st.button("Forgot Password?")
if forgot:
    st.switch_page("pages/3_Forgot_Password.py")

st.write("")
no_acc = st.button("Go to Register")
if no_acc:
    st.switch_page("pages/1_Register.py")
