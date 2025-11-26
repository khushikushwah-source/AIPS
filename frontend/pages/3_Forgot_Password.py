import streamlit as st
from firebase_config import users_ref
from common_ui import setup_page

# ---------------- Page Setup ----------------
setup_page("Forgot Password", "pages/3_Forgot_Password.py")

# ---------------- Form ----------------
email = st.text_input("Enter Registered Email")
new_password = st.text_input("New Password", type="password")
confirm_new_password = st.text_input("Confirm New Password", type="password")

email_error = st.empty()
password_error = st.empty()

update_clicked = st.button("Update Password")

if update_clicked:
    email_error.empty()
    password_error.empty()
    ok = True

    if not email:
        email_error.markdown("<span style='color:#f87171;'>Enter your registered email.</span>", unsafe_allow_html=True)
        ok = False

    if not new_password or not confirm_new_password:
        password_error.markdown("<span style='color:#f87171;'>Enter both password fields.</span>", unsafe_allow_html=True)
        ok = False

    elif new_password != confirm_new_password:
        password_error.markdown("<span style='color:#f87171;'>Passwords do not match.</span>", unsafe_allow_html=True)
        ok = False

    if ok:
        user_doc = users_ref.document(email).get()

        if not user_doc.exists:
            email_error.markdown("<span style='color:#f87171;'>This email is not registered.</span>", unsafe_allow_html=True)
        else:
            users_ref.document(email).update({"password": new_password})
            st.success("Password updated successfully ✔")
            st.info("You can now login with your new password.")

# back to login
if st.button("Back to Login"):
    st.switch_page("pages/2_Login.py")
