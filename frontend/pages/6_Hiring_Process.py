import streamlit as st
import streamlit.components.v1 as components
import json
import os

st.set_page_config(page_title="AIPS — Hiring Process", page_icon="📋", layout="wide")

# ----------- AUTH GUARD ----------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("pages/2_Login.py")

# ----------- GET USER ----------
user = st.session_state.get("user", {})

if not user:
    st.warning("Please login again.")
    st.switch_page("pages/2_Login.py")

name = user.get("name", "User")
email = user.get("email", "")
company = user.get("company")
domain = user.get("domain")

if not company or not domain:
    st.warning("Please complete domain + company selection first.")
    st.switch_page("pages/4_Dashboard.py")

# ----------- GLOBAL CSS ----------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    section[data-testid="stSidebar"] {display:none !important;}
    html, body, [data-testid="stAppViewContainer"] {
        background: #020617;
        font-family: system-ui;
        overflow: hidden;
    }
    .block-container { padding-top: 0.4rem !important; }
    .hp-header { width: 100%; padding: 8px 16px 0 16px; }
    .hp-back-btn { border-radius: 999px; padding: 6px 14px;
        border: 1px solid rgba(226,232,240,0.6);
        background: #064e3b; color: #ecfeff; font-weight: 600; }
    .hp-avatar-btn { width: 40px; height: 40px; border-radius: 50%;
        background: #dc2626; color: white; border: none;
        font-weight: 700; font-size: 18px; }
    .hp-chart-wrapper {
        max-width: 1200px; margin: 15px auto;
        border: 1px solid rgba(148,163,184,0.4);
        border-radius: 16px; overflow: hidden;
        box-shadow: 0 24px 55px rgba(15,23,42,0.9);
    }
    .hp-next-btn { background: #2563eb !important; color:white !important;
        padding: 10px 26px; border-radius: 999px; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------- HEADER (BACK + PROFILE) ----------
st.markdown('<div class="hp-header">', unsafe_allow_html=True)
c1, _, c2 = st.columns([1, 6, 1])

with c1:
    back = st.button("← Back", key="hp_back")

with c2:
    avatar = name[0].upper()
    with st.popover(avatar):
        st.write(f"**{name}**")
        st.write(email)
        if st.button("My Profile 👤"):
            st.switch_page("pages/5_My_Profile.py")
        if st.button("Logout ⏻"):
            st.session_state.clear()
            st.switch_page("pages/0_Welcome.py")

st.markdown("</div>", unsafe_allow_html=True)

if back:
    st.switch_page("pages/4_Dashboard.py")

# ----------- LOAD HIRING PROCESS JSON ----------
json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "hiring_process_data.json")

with open(json_path, "r", encoding="utf-8") as f:
    hp_data = json.load(f)

key = f"{company}_{domain}"
stages = hp_data.get(key)

if not stages:
    st.error("⚠ This company + domain does not have hiring process data yet.")
    st.stop()

chart_json = json.dumps(stages)

# ----------- IFRAME (REACT CHART) ----------
import urllib.parse

chart_json = json.dumps(stages)  # list ko JSON me convert
encoded = urllib.parse.quote(chart_json)  # URL encoding

components.iframe(
    f"http://localhost:5000?data={encoded}&company={company}&domain={domain}",
    height=700
)

# ----------- NEXT BUTTON ----------
c = st.container()
with c:
    next_btn = st.button("Next ➜", key="hp_next")
if next_btn:
    st.switch_page("pages/7_Test_Page.py")
