import streamlit as st
import smtplib
import random
import string
from firebase_config import users_ref
from common_ui import setup_page

# ---------------- Page Setup ----------------
setup_page("Register", "pages/1_Register.py")

# ---------------- Email SMTP Config ----------------
SENDER_EMAIL = "workmail.khushikushwah@gmail.com"          # CHANGE
SENDER_PASSWORD = "fmfzqrcgvfcxnugr"         # CHANGE (NOT Gmail login password)

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

# ---------------- Registration Form ----------------
name = st.text_input("Name")

# email + send OTP button
col1, col2 = st.columns([4, 1])
with col1:
    email = st.text_input("Email (Gmail only)")
    email_error_ph = st.empty()
with col2:
    send_otp = st.button("Send OTP")


# ---------------- OTP Verification ----------------
otp_input = st.text_input("Enter OTP received on email")
if st.button("Verify OTP"):
    if otp_input == st.session_state["reg_otp"]:
        st.session_state["reg_email_verified"] = True
        st.session_state["reg_otp"] = None
        st.success("Email verified successfully ✔")
    else:
        st.error("Incorrect OTP ❌")

st.markdown("---")

# phone
phone = st.text_input("Phone Number (10 digits)")
phone_error_ph = st.empty()

# password + confirm password
colp1, colp2 = st.columns(2)
with colp1:
    password = st.text_input("Password", type="password")
with colp2:
    confirm_password = st.text_input("Confirm Password", type="password")
password_error_ph = st.empty()

# ---------------- Send OTP Logic ----------------
if send_otp:
    email_error_ph.empty()

    # check already registered in Firebase
    if users_ref.document(email).get().exists:
        email_error_ph.markdown(
            "<span style='color:#f87171; font-size:12px;'>This email is already registered. Please go to Login.</span>",
            unsafe_allow_html=True
        )
    elif not email:
        email_error_ph.markdown(
            "<span style='color:#facc15; font-size:12px;'>Please enter email.</span>",
            unsafe_allow_html=True
        )
    elif not email.lower().endswith("@gmail.com"):
        email_error_ph.markdown(
            "<span style='color:#f97316; font-size:12px;'>Email must end with @gmail.com.</span>",
            unsafe_allow_html=True
        )
    else:
        otp = "".join(random.choices(string.digits, k=6))
        st.session_state["reg_otp"] = otp
        st.session_state["reg_email_for_otp"] = email
        st.session_state["reg_email_verified"] = False

        try:
            send_otp_email(email, otp)
            st.success(f"OTP sent to {email}")
        except Exception:
            st.error("Failed to send OTP. Check Gmail App Password in code.")


# ---------------- Final Register Button ----------------
register_clicked = st.button("Register")

if register_clicked:
    email_error_ph.empty()
    phone_error_ph.empty()
    password_error_ph.empty()
    ok = True

    # Empty field validation
    if not all([name, email, phone, password, confirm_password]):
        st.error("Fill all fields correctly ❌")
        ok = False

    # Email validation
    if not email.lower().endswith("@gmail.com"):
        email_error_ph.markdown(
            "<span style='color:#f97316; font-size:12px;'>Email must end with @gmail.com.</span>",
            unsafe_allow_html=True
        )
        ok = False
    elif users_ref.document(email).get().exists:
        email_error_ph.markdown(
            "<span style='color:#f87171; font-size:12px;'>This email is already registered. Please go to Login.</span>",
            unsafe_allow_html=True
        )
        ok = False

    # Phone validation
    if not phone.isdigit() or len(phone) != 10:
        phone_error_ph.markdown(
            "<span style='color:#f97316; font-size:12px;'>Enter a valid 10‑digit phone number.</span>",
            unsafe_allow_html=True
        )
        ok = False

    # Password field validation
    if password != confirm_password:
        password_error_ph.markdown(
            "<span style='color:#f97316; font-size:12px;'>Password & Confirm Password do not match.</span>",
            unsafe_allow_html=True
        )
        ok = False

    # OTP verified
    if not st.session_state["reg_email_verified"]:
        st.error("Verify your email before registering ❌")
        ok = False

    # Save to Firebase
    if ok:
        users_ref.document(email).set({
            "name": name,
            "email": email,
            "phone": phone,
            "password": password
        })
        st.success(f"{name}, you registered successfully 🎉")
        st.info("You can now login.")
        st.switch_page("pages/2_Login.py")
        
# Go to login
st.write("")
st.write("Already have an account?")
if st.button("Go to Login"):
    st.switch_page("pages/2_Login.py")
