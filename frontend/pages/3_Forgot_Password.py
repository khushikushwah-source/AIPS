import streamlit as st

st.set_page_config(page_title="Forgot Password | AIPS", page_icon="🔐", layout="wide")

# hide streamlit UI
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Forgot Password")

email = st.text_input("Enter Registered Email")
new_password = st.text_input("New Password", type="password")
confirm_new_password = st.text_input("Confirm New Password", type="password")

if st.button("Update Password"):
    registered_email = st.session_state.get("registered_email")

    if not registered_email:
        st.error("No user is registered yet.")
    elif email != registered_email:
        st.error("This email is not registered ❌")
    elif new_password != confirm_new_password:
        st.error("New password and confirm password do not match ❌")
    else:
        # update session password
        st.session_state["registered_password"] = new_password
        st.success("Password changed successfully ✔")
        st.info("You can now login with your new password.")
        
# back to login
if st.button("Back to Login"):
    st.switch_page("pages/2_Login.py")
