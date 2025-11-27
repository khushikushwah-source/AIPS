import streamlit as st
from firebase_config import users_ref

st.set_page_config(page_title="AIPS — My Profile", page_icon="👤", layout="wide")

# ---------- Guard ----------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()

user = st.session_state.get("user", {})
email = user.get("email")

if not email:
    st.error("No user email found in session. Please login again.")
    st.stop()

DOMAIN_OPTIONS = [
    "Software Developer",
    "Software Tester",
    "Data Analyst",
    "Support Engineer",
]

COMPANY_OPTIONS = [
    "TCS",
    "Infosys",
    "Wipro",
]

st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      section[data-testid="stSidebar"] {display:none !important;}
      .block-container {padding-top: 1rem;}

      .top-bar {
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding: 8px 4px;
      }

      .profile-card {
        max-width: 600px;
        margin: 40px auto 0 auto;
        padding: 26px 24px;
        border-radius: 12px;
        border: 1px solid rgba(148,163,184,0.7);
        background: rgba(15,23,42,0.95);
      }

      .profile-card h2 {
        margin-top:0;
        margin-bottom: 18px;
      }

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- TOP BAR ----------
st.markdown('<div class="top-bar">', unsafe_allow_html=True)
tb_left, tb_right = st.columns([1, 1])

with tb_left:
    if st.button("← Back", key="back_to_dashboard"):
        st.switch_page("pages/4_Dashboard.py")

with tb_right:
    st.write("")  # spacing

st.markdown("</div>", unsafe_allow_html=True)

# ---------- PROFILE CARD ----------
st.markdown('<div class="profile-card">', unsafe_allow_html=True)
st.subheader("My Profile")

# read-only fields
st.text_input("Name", value=user.get("name", ""), disabled=True)
st.text_input("Email", value=user.get("email", ""), disabled=True)
st.text_input("Phone", value=user.get("phone", ""), disabled=True)

st.markdown("---")

# editable fields
course = st.text_input("Course ✏", value=user.get("course", ""))

# domain with selectbox
domain = st.selectbox(
    "Domain ✏",
    ["Select Domain"] + DOMAIN_OPTIONS,
    index=(["Select Domain"] + DOMAIN_OPTIONS).index(user.get("domain"))
    if user.get("domain") in DOMAIN_OPTIONS
    else 0,
)

# company with selectbox
company = st.selectbox(
    "Company ✏",
    ["Select Company"] + COMPANY_OPTIONS,
    index=(["Select Company"] + COMPANY_OPTIONS).index(user.get("company"))
    if user.get("company") in COMPANY_OPTIONS
    else 0,
)

if st.button("Update", key="update_profile"):
    updates = {}
    updates["course"] = course.strip()

    if domain != "Select Domain":
        updates["domain"] = domain
    if company != "Select Company":
        updates["company"] = company

    # Update Firebase
    users_ref.document(email).set({**user, **updates}, merge=True)

    # Update local session user
    user.update(updates)
    st.session_state["user"] = user

    st.success("Profile updated successfully ✅")
    # My profile page close (go back to Dashboard)
    st.switch_page("pages/4_Dashboard.py")

st.markdown("</div>", unsafe_allow_html=True)
