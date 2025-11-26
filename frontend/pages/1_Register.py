import streamlit as st
import smtplib
import random
import string

st.set_page_config(page_title="Register | AIPS", page_icon="📝", layout="wide")

# ---------------- Gmail SMTP Config ----------------
SENDER_EMAIL = "workmail.khushikushwah@gmail.coM"            # replace
SENDER_PASSWORD = "fmfzqrcgvfcxnugr"           # replace (not gmail password, APP password)

def send_otp_email(receiver, otp):
    subject = "Your AIPS Email Verification OTP"
    body = f"Your OTP for AIPS email verification is: {otp}"
    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver, message)

# ---------------- Session Values ----------------
if "reg_otp" not in st.session_state:
    st.session_state["reg_otp"] = None
if "reg_email_verified" not in st.session_state:
    st.session_state["reg_email_verified"] = False
if "reg_email_for_otp" not in st.session_state:
    st.session_state["reg_email_for_otp"] = None

st.title("Register")

name = st.text_input("Name")

# EMAIL + SEND OTP beside email input
col1, col2 = st.columns([4, 1])
with col1:
    email = st.text_input("Email (Gmail only)")
with col2:
    send_otp = st.button("Send OTP")


# OTP field under it
otp_input = st.text_input("Enter OTP received on email")

if st.button("Verify OTP"):
    if not st.session_state.get("reg_otp"):
        st.error("Send OTP first.")
    elif otp_input == st.session_state["reg_otp"]:
        st.session_state["reg_email_verified"] = True
        st.session_state["reg_otp"] = None  # remove otp (like firebase delete)
        st.success("Email verified successfully ✔")
    else:
        st.error("Incorrect OTP ❌")

phone = st.text_input("Phone Number (10 digits)")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

# --- Send OTP Button Action ---
if send_otp:
    if not email:
        st.warning("Enter email first.")
    elif not email.lower().endswith("@gmail.com"):
        st.warning("Email must end with @gmail.com")
    else:
        otp = "".join(random.choices(string.digits, k=6))
        st.session_state["reg_otp"] = otp
        st.session_state["reg_email_for_otp"] = email
        st.session_state["reg_email_verified"] = False

        try:
            send_otp_email(email, otp)
            st.success(f"OTP sent to {email}")
        except Exception as e:
            st.error("Failed to send OTP. Check Gmail & App Password in code.")
            st.stop()


st.markdown("---")

def validate_phone(num):
    return num.isdigit() and len(num) == 10

# Final Register
if st.button("Register"):
    if not all([name, email, phone, password, confirm_password]):
        st.error("Fill all fields correctly ❌")
    elif not email.lower().endswith("@gmail.com"):
        st.error("Invalid Gmail ❌")
    elif not validate_phone(phone):
        st.error("Invalid 10‑digit phone number ❌")
    elif password != confirm_password:
        st.error("Password & Confirm Password do not match ❌")
    elif not st.session_state["reg_email_verified"]:
        st.error("Verify your email before registering ❌")
    else:
        st.session_state["registered_email"] = email
        st.session_state["registered_password"] = password

        st.success(f"{name}, you registered successfully 🎉")
        st.info("You can now login.")

go_login = st.button("Go to Login")
if go_login:
    st.switch_page("pages/2_Login.py")

        # TODO: Add user to Firebase Backend
