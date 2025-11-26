import streamlit as st

st.set_page_config(page_title="Login | AIPS", page_icon="🔑", layout="wide")

# hide menu/header/footer
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    registered_email = st.session_state.get("registered_email")
    registered_password = st.session_state.get("registered_password")

    if not registered_email or not registered_password:
        st.error("No account found. Register first.")
    elif email == registered_email and password == registered_password:
        st.success("Successfully logged in 🎉")
        st.session_state["logged_in"] = True
    else:
        st.error("Invalid email or password ❌")

# forgot password button
if st.button("Forgot Password?"):
    st.switch_page("pages/3_Forgot_Password.py")

st.write("")
st.write("Don't have an account?")
if st.button("Go to Register"):
    st.switch_page("pages/1_Register.py")
