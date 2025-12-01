import streamlit as st
import streamlit.components.v1 as components

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
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
section[data-testid="stSidebar"] {display:none !important;}

html, body, [data-testid="stAppViewContainer"], .main {
    height: 100vh !important;
    overflow: hidden !important;
    background: #020617;
    font-family: system-ui, -apple-system, Segoe UI, sans-serif;
}

hr { display:none !important; visibility:hidden !important; height:0 !important; }

/* top bar */
.hp-header { width:100%; padding: 8px 16px 0 16px; box-sizing:border-box; }
.hp-back-btn {
    border-radius:999px; padding:6px 16px;
    border:1px solid rgba(226,232,240,0.6);
    background:#064e3b; color:#ecfeff; font-weight:600; font-size:14px;
}
.hp-avatar-btn {
    width:40px; height:40px; border-radius:50%;
    background:#dc2626; color:white; border:none;
    font-size:18px; font-weight:700;
    box-shadow:0 8px 22px rgba(15,23,42,0.8);
}

/* title card */
.hp-title-card {
    max-width: 980px;
    margin: 40px auto 18px auto;
    padding: 18px 22px;
    border-radius: 18px;
    background: rgba(15,23,42,0.96);
    border: 1px solid rgba(148,163,184,0.6);
    box-shadow: 0 24px 60px rgba(15,23,42,0.9);
    text-align:center;
}
.hp-title-main { font-size:22px; font-weight:700; color:#e5e7eb; }
.hp-title-sub { font-size:14px; color:#a5b4fc; margin-top:4px; }

/* React container */
.hp-chart-wrapper {
    max-width:1100px;
    margin: 12px auto 0 auto;
    border-radius:18px;
    overflow:hidden;
    border:1px solid rgba(148,163,184,0.4);
    box-shadow:0 24px 55px rgba(15,23,42,0.9);
}

/* fixed NEXT button */
.hp-next-btn {
    position:fixed;
    right:28px;
    bottom:28px;
    background:#0891b2;
    color:white;
    font-weight:600;
    border-radius:50px;
    padding:10px 26px;
    font-size:15px;
    border:none;
    box-shadow:0 8px 22px rgba(0,0,0,0.6);
    cursor:pointer;
}
.hp-next-btn:hover { background:#0e7490; }
</style>
""", unsafe_allow_html=True)

# ------------- HEADER (Back + Profile) -------------
st.markdown('<div class="hp-header">', unsafe_allow_html=True)
c1, _, c2 = st.columns([1, 6, 1])

with c1:
    back = st.button("← Back", key="back_btn")

with c2:
    avatar = (user.get("name") or "U")[0].upper()
    with st.popover(avatar):
        st.write(f"**{user.get('name','User')}**")
        st.write(email)
        st.markdown("---")
        if st.button("My Profile 👤"):
            st.switch_page("pages/5_My_Profile.py")
        if st.button("Logout ⏻"):
            st.session_state.clear()
            st.switch_page("pages/0_Welcome.py")

st.markdown("</div>", unsafe_allow_html=True)

# Apply button style
st.markdown(f"""
<script>
let btns = window.parent.document.querySelectorAll("button");
btns.forEach(b => {{
    if (b.innerText.trim() === "← Back") b.classList.add("hp-back-btn");
    if (b.innerText.trim() === "{avatar}") b.classList.add("hp-avatar-btn");
}});
</script>
""", unsafe_allow_html=True)

if back:
    st.switch_page("pages/4_Dashboard.py")

# ------------- REACT FLOWCHART -------------
st.markdown('<div class="hp-chart-wrapper">', unsafe_allow_html=True)
components.iframe("http://localhost:5000", height=520)     # <── React app serving here
st.markdown("</div>", unsafe_allow_html=True)

# ------------- NEXT BUTTON (fixed) -------------

next_clicked = st.button("Next ➜", key="next_btn")

if next_clicked:
    if not user.get("domain") or not user.get("company"):
        st.warning("Please submit domain & company first.")
    else:
        st.switch_page("pages/7_Test_Session.py")

# JS listener for next click → Streamlit action
st.markdown("""
<script>
window.addEventListener("message", (event) => {
  if (event.data === "NEXT_CLICK") {
    window.parent.location.href = window.parent.location.origin + "/?page=pages/7_Test_Session.py";
  }
});
</script>
""", unsafe_allow_html=True)
