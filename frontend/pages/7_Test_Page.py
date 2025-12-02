import streamlit as st
from firebase_config import users_ref

st.set_page_config(page_title="AIPS — Dashboard", page_icon="🤖", layout="wide")


# ---------------- AUTH CHECK ----------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("pages/2_Login.py")

user = st.session_state.get("user", {})
email = user.get("email")
if not email:
    st.error("User email missing. Please login again.")
    st.stop()

# ---------------- HIDE DEFAULT STREAMLIT UI ----------------
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none !important;}
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
""", unsafe_allow_html=True)


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


# ---------------- GREETING TEXT ----------------
st.markdown(
    f"""
    <div style='text-align:center; margin-top:10px;'>
        <h2 style='color:white; font-size:34px;'>Every test you attempt takes you one step closer to your dream job.! 👋</h2>
        <h3 style='color:#e5e7eb; font-size:22px; margin-top:-8px;'>Choose your test</h3>
        <p style='color:#9ca3af; font-size:18px;'>Please select a test category below to begin your practice.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- CARD DATA ----------------
tests = [
    ("Quantitative Aptitude", "Numbers, ratios, time & work, percentages", 15, 20, "quantitative"),
    ("Logical Reasoning", "Puzzles, patterns, seating arrangement", 15, 20, "logical"),
    ("Verbal Ability", "Reading comprehension, grammar, vocabulary", 15, 20, "verbal"),
    ("Aptitude – Full Mix", "Quant + Logical + Verbal combined", 30, 40, "aptitude_mix"),
    ("Technical Assessment (MCQ)", "DBMS, OS, OOP, DS basics", 20, 30, "technical_mcq"),
    ("Technical Interview Simulation", "Conceptual + scenario-based questions", 10, 25, "tech_interview"),
    ("HR Interview Simulation", "Behavioural and HR questions", 10, 20, "hr_interview"),
]


# ---------------- CARD GRID ----------------
st.write("")
rows = [tests[i:i+3] for i in range(0, len(tests), 3)]

if "selected_test" not in st.session_state:
    st.session_state["selected_test"] = None

for row in rows:
    cols = st.columns(3)
    for col, (title, desc, q, t, key) in zip(cols, row):
        with col:
            if st.button(
                f"{title}\n\n{desc}\n{q} questions · {t} minutes",
                key=key,
                use_container_width=True

            ):
                
                st.markdown(
            f"""
            <script>
                var btn = window.parent.document.querySelector('button[data-testid="stButton-{key}"]');
                if(btn) btn.parentElement.classList.add("card-btn");
            </script>
            """,
            unsafe_allow_html=True
            )
                st.session_state["selected_test"] = (title, desc, q, t, key)

            st.markdown("""
                <style>
                div.stButton > button {
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.12);
                    border-radius: 16px;
                    color: white;
                    font-size: 17px;
                    padding: 18px;
                    height: 180px;
                    text-align: left;
                    transition: 0.2s;
                    white-space: normal;
                }
                div.stButton > button:hover {
                    transform: scale(1.03);
                    border-color: #3b82f6;
                    box-shadow: 0 0 12px rgba(59,130,246,0.4);
                }
                </style>
            """, unsafe_allow_html=True)

# ---------------- CONFIRMATION MODAL ----------------
if st.session_state["selected_test"]:
    title, desc, q, t, key = st.session_state["selected_test"]

    @st.dialog("Start Test")
    def start_popup():
        st.write(f"### {title}")
        st.write(desc)
        st.write(f"📝 **{q} Questions**")
        st.write(f"⏳ **{t} Minutes**")
        st.write("Once started, the timer will run without pause.")
        st.write("")

        if st.button("Start Test ✅"):
            st.session_state["active_test"] = {
                "category": key,
                "title": title,
                "num_questions": q,
                "time_limit": t
            }
            st.session_state["questions"] = []
            st.session_state["user_answers"] = []
            st.session_state["selected_test"] = None
            st.switch_page("pages/8_Test_Screen.py")

        if st.button("Cancel ❌"):
            st.session_state["selected_test"] = None

    start_popup()


# ---------------- NEXT BUTTON ----------------
st.write("")
if st.button("Next ➜"):
    st.switch_page("pages/8_Test_Results.py")

st.markdown("""
<style>
button[kind="secondary"] {
    display: block;
    margin-left: auto;
    background: #020b66;
    color: white;
    border-radius: 25px;
    font-weight: 600;
    padding: 6px 20px;
}
</style>
""", unsafe_allow_html=True)
