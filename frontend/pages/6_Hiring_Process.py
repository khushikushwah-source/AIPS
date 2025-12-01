import streamlit as st
import streamlit.components.v1 as components

from firebase_config import users_ref  # agar use nahi ho raha to hata bhi sakte ho

st.set_page_config(page_title="AIPS — Hiring Process", page_icon="📋", layout="wide")

# ------------- AUTH GUARD -------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("pages/2_Login.py")

user = st.session_state.get("user", {})
email = user.get("email")
domain = user.get("domain")
company = user.get("company")

if not email or not domain or not company:
    st.warning("Please complete your domain and company selection first.")
    st.switch_page("pages/4_Dashboard.py")

# ------------- GLOBAL STYLES -------------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility:hidden;}
    section[data-testid="stSidebar"] {display:none !important;}

    html, body, [data-testid="stAppViewContainer"], .main {
        height: 100vh !important;
        overflow: hidden !important;
        background: #020617;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* remove unwanted top horizontal line */
    hr {
    display: none !important;
    border: none !important;
    height: 0px !important;
    }

    .block-container {
        padding-top: 0.4rem !important;
    }

    /* top header row */
    .hp-header {
        width: 100%;
        padding: 8px 16px 0 16px;
        box-sizing: border-box;
    }
    .hp-back-btn {
        border-radius: 999px;
        padding: 6px 16px;
        border: 1px solid rgba(226,232,240,0.6);
        background: #064e3b;
        color: #ecfeff;
        font-weight: 600;
        font-size: 14px;
    }
    .hp-avatar-btn {
        width: 40px;
        height: 40px;
        border-radius: 999px;
        background: #dc2626;
        color: white;
        border: none;
        font-weight: 700;
        font-size: 18px;
        box-shadow: 0 8px 22px rgba(15,23,42,0.8);
    }

    /* title + message card */
    .hp-title-card {
        max-width: 980px;
        margin: 40px auto 18px auto;
        padding: 18px 22px;
        border-radius: 18px;
        background: rgba(15,23,42,0.96);
        border: 1px solid rgba(148,163,184,0.6);
        box-shadow: 0 24px 60px rgba(15,23,42,0.9);
    }
    .hp-title-main {
        font-size: 22px;
        font-weight: 700;
        color: #e5e7eb;
        margin-bottom: 4px;
    }
    .hp-title-sub {
        font-size: 14px;
        color: #a5b4fc;
    }

    /* React chart wrapper */
    .hp-chart-wrapper {
        max-width: 1200px;
        margin: 18px auto 28 auto;
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(148,163,184,0.4);
        box-shadow: 0 24px 55px rgba(15,23,42,0.9);
        background: transparent;
    }

    /* ------------ NEXT BUTTON BOTTOM RIGHT ------------ */
    .hp-next-row {
        max-width: 1200px;
        margin: 0 auto 32px auto;
        width: 100%;
        text-align: right;
    }

    .hp-next-btn {
        padding: 10px 26px;
        border-radius: 999px;
        background: #2563eb !important;
        color: white !important;
        font-weight: 600;
        font-size: 15px;
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------- HEADER (Back + Profile) -------------
st.markdown('<div class="hp-header">', unsafe_allow_html=True)
c1, c_mid, c2 = st.columns([1, 6, 1])

with c1:
    # use the html style but Streamlit button for action
    back = st.button("← Back", key="hp_back_btn")
with c2:
    avatar_label = (user.get("name") or "U")[0].upper()
    # popover like previous pages
    with st.popover(avatar_label):
        st.write(f"**{user.get('name','User')}**")
        st.write(user.get("email", ""))
        #st.markdown("---")
        if st.button("My Profile 👤"):
            st.switch_page("pages/5_My_Profile.py")
        if st.button("Logout ⏻"):
            st.session_state.clear()
            st.switch_page("pages/0_Welcome.py")

st.markdown("</div>", unsafe_allow_html=True)

# style override for the header buttons (apply classes)
st.markdown(
    """
    <script>
    const btns = window.parent.document.querySelectorAll("button");
    btns.forEach(b => {
      if (b.innerText.trim() === "← Back") {
        b.classList.add("hp-back-btn");
      }
    });
    </script>
    """,
    unsafe_allow_html=True,
)

if back:
    st.switch_page("pages/4_Dashboard.py")


# ------------- HIRING PROCESS CHART (React iframe) -------------
# ⚠️ Make sure you are serving your React build at http://localhost:5000
st.markdown('<div class="hp-chart-wrapper">', unsafe_allow_html=True)

components.iframe("http://localhost:5000", height=700)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- NEXT BUTTON (Bottom Right) ----------------
st.markdown('<div class="hp-next-row">', unsafe_allow_html=True)
next_clicked = st.button("Next ➜", key="hp_next_btn")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <script>
    const nbtns = window.parent.document.querySelectorAll("button");
    nbtns.forEach(b => {
      if (b.innerText.trim() === "Next ➜") {
        b.classList.add("hp-next-btn");
      }
    });
    </script>
    """,
    unsafe_allow_html=True,
)

if next_clicked:
    st.switch_page("pages/7_Test_Session.py")