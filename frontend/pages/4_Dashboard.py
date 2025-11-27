import streamlit as st
from firebase_config import users_ref

st.set_page_config(page_title="AIPS — Dashboard", page_icon="🤖", layout="wide")

# ----------------- AUTH GUARD -----------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("pages/2_Login.py")

user = st.session_state.get("user", {})
email = user.get("email")
if not email:
    st.error("User email missing. Please login again.")
    st.stop()

# ----------------- CONSTANTS -----------------
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

# ----------------- GLOBAL STYLES (dark, no scroll) -----------------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility:hidden;}
    section[data-testid="stSidebar"] {display:none !important;}

    html, body, [data-testid="stAppViewContainer"], .main {
        height: 100vh !important;
        overflow: hidden !important;
        background: #020617;
    }

    .block-container {
        padding-top: 0.5rem !important;
    }

    /* header row */
    .dash-header {
        width: 100%;
        padding: 8px 16px 0 16px;
        box-sizing: border-box;
    }

    /* center card */
    .dash-card {
        max-width: 600px;
        margin: 80px auto 0 auto;  /* below header */
        padding: 26px 24px;
        border-radius: 16px;
        background: rgba(15,23,42,0.96);
        border: 1px solid rgba(148,163,184,0.6);
        box-shadow: 0 24px 60px rgba(15,23,42,0.8);
    }

    .dash-card h2 {
        margin-top:0;
        margin-bottom: 18px;
    }

    /* Back button look */
    .dash-back button {
        border-radius: 999px;
        padding: 6px 16px;
        border: 1px solid rgba(226,232,240,0.7);
        background: #064e3b;
        color: #ecfeff;
        font-weight: 600;
    }

    /* Profile button look */
    .dash-prof button {
        width: 40px;
        height: 40px;
        border-radius: 999px;
        background: #dc2626;
        color: white;
        border: none;
        font-weight: 700;
        font-size: 18px;
        box-shadow: 0 8px 24px rgba(15,23,42,0.7);
    }

    /* fix Next button bottom-right */
    .next-fixed-btn{
        position: fixed;
        right: 24px ;
        bottom: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- HEADER: Back (left) + Profile popover (right) -----------------
st.markdown('<div class="dash-header">', unsafe_allow_html=True)
h_left, h_spacer, h_right = st.columns([1, 6, 1])

with h_left:
    with st.container():
        back_clicked = st.button("← Back", key="back_btn")
    st.markdown('<div class="dash-back"></div>', unsafe_allow_html=True)

with h_right:
    avatar_label = (user.get("name") or "U")[0].upper()
    # st.popover → proper floating box, content fixed
    with st.popover(avatar_label):
        st.write(f"**{user.get('name','User')}**")
        st.write(user.get("email",""))
        st.markdown("---")
        if st.button("My Profile 👤", key="pp_my_profile"):
            st.switch_page("pages/5_My_Profile.py")
        if st.button("Logout ⏻", key="pp_logout"):
            st.session_state.clear()
            st.switch_page("pages/0_Welcome.py")
    st.markdown('<div class="dash-prof"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# back behaviour (previous page, else login)
if back_clicked:
    prev = st.session_state.get("prev_page", "pages/2_Login.py")
    try:
        st.switch_page(prev)
    except Exception:
        st.switch_page("pages/2_Login.py")

# ----------------- CENTER CARD -----------------
st.markdown('<div class="dash-card" style="text-align: centre;"><h3>Select Your Domain and Company</h3></div>', unsafe_allow_html=True)

#st.subheader("Select Your Domain and Company")

current_domain = user.get("domain")
current_company = user.get("company")

domain = st.selectbox(
    "Domain",
    ["Select Domain"] + DOMAIN_OPTIONS,
    index=(["Select Domain"] + DOMAIN_OPTIONS).index(current_domain)
    if current_domain in DOMAIN_OPTIONS
    else 0,
)

company = st.selectbox(
    "Company Name",
    ["Select Company"] + COMPANY_OPTIONS,
    index=(["Select Company"] + COMPANY_OPTIONS).index(current_company)
    if current_company in COMPANY_OPTIONS
    else 0,
)

if st.button("Submit", key="submit_dc"):
    if domain == "Select Domain" or company == "Select Company":
        st.error("Please select both Domain and Company.")
    else:
        users_ref.document(email).set(
            {**user, "domain": domain, "company": company},
            merge=True,
        )
        user["domain"] = domain
        user["company"] = company
        st.session_state["user"] = user
        st.success("Domain and company saved successfully ✔")

st.markdown("</div>", unsafe_allow_html=True)

# ----------------- NEXT BUTTON (bottom-right fixed) -----------------
next_clicked = st.button("Next ➜", key="next_btn")

if next_clicked:
    if not user.get("domain") or not user.get("company"):
        st.warning("Please submit domain & company first.")
    else:
        st.switch_page("pages/6_Hiring_Process.py")
