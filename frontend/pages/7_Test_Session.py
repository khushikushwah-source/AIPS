import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AIPS — Test Selection", page_icon="📝", layout="wide")

# ---------------- AUTH GUARD ----------------
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.switch_page("pages/2_Login.py")

user = st.session_state.get("user", {})
name = user.get("name", "User")
email = user.get("email", "")
avatar_label = name[0].upper()

domain = user.get("domain")
company = user.get("company")

if not email or not domain or not company:
    st.warning("Please complete your domain and company selection first.")
    st.switch_page("pages/4_Dashboard.py")

# ---------------- TEST CONFIG DEFINITION ----------------
TEST_CONFIG = {
    "quantitative": {
        "title": "Quantitative Aptitude",
        "description": "Numbers, ratios, work & time, percentages",
        "num_questions": 15,
        "time_limit_minutes": 20,
        "difficulty": "Mixed",
    },
    "logical": {
        "title": "Logical Reasoning",
        "description": "Puzzles, patterns, seating arrangement",
        "num_questions": 15,
        "time_limit_minutes": 20,
        "difficulty": "Mixed",
    },
    "verbal": {
        "title": "Verbal Ability",
        "description": "Reading comprehension, grammar, vocabulary",
        "num_questions": 15,
        "time_limit_minutes": 20,
        "difficulty": "Mixed",
    },
    "aptitude_mix": {
        "title": "Aptitude – Full Mix",
        "description": "Quant + Logical + Verbal combined",
        "num_questions": 30,
        "time_limit_minutes": 40,
        "difficulty": "Mixed",
    },
    "technical_mcq": {
        "title": "Technical Assessment (MCQ)",
        "description": "CS fundamentals, OS, DBMS, OOPs, basic DSA",
        "num_questions": 20,
        "time_limit_minutes": 30,
        "difficulty": "Mixed",
    },
    "tech_interview": {
        "title": "Technical Interview Simulation",
        "description": "Conceptual + scenario-based questions",
        "num_questions": 10,
        "time_limit_minutes": 25,
        "difficulty": "Moderate",
    },
    "hr_interview": {
        "title": "HR Interview Simulation",
        "description": "Behavioural and HR questions",
        "num_questions": 10,
        "time_limit_minutes": 20,
        "difficulty": "Easy–Moderate",
    },
}

if "selected_test_key" not in st.session_state:
    st.session_state["selected_test_key"] = None

# ---------------- GLOBAL CSS ----------------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility:hidden;}
    section[data-testid="stSidebar"] {display:none !important;}

    html, body, [data-testid="stAppViewContainer"], .main {
        background: #020617;
        font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    }

    /* remove any default Streamlit horizontal rules */
    hr,
    div[data-testid="stDivider"],
    div[data-testid="stHorizontalBlock"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        border: none !important;
    }

    /* HEADER (Back + Profile) */
    .tp-header {
        width: 100%;
        padding: 10px 18px 4px 18px;
        box-sizing: border-box;
    }

    .tp-back-btn {
        border-radius: 999px;
        padding: 6px 18px;
        border: 1px solid rgba(226,232,240,0.6);
        background: #064e3b;
        color: #ecfeff;
        font-weight: 600;
        font-size: 14px;
    }

    .tp-avatar-btn {
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

    /* TITLE */
    .tp-title-wrap {
        max-width: 900px;
        margin: 24px auto 18px auto;
        text-align: center;
    }
    .tp-title-main {
        font-size: 22px;
        font-weight: 700;
        color: #e5e7eb;
        margin-bottom: 4px;
    }
    .tp-title-sub {
        font-size: 14px;
        color: #9ca3af;
    }

    /* CARDS GRID */
    .tp-card {
        border-radius: 16px;
        border: 1px solid rgba(148,163,184,0.35);
        background: radial-gradient(circle at top left, #1f2937 0, #020617 55%);
        padding: 14px 16px;
        box-shadow: 0 16px 40px rgba(15,23,42,0.9);
        transition: transform 0.12s ease-out, box-shadow 0.12s ease-out, border-color 0.12s;
        height: 100%;
    }
    .tp-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 55px rgba(15,23,42,1);
        border-color: #38bdf8;
    }
    .tp-card-title {
        font-size: 16px;
        font-weight: 700;
        color: #e5e7eb;
        margin-bottom: 6px;
    }
    .tp-card-desc {
        font-size: 13px;
        color: #9ca3af;
        margin-bottom: 10px;
        min-height: 34px;
    }
    .tp-card-meta {
        font-size: 12px;
        color: #a5b4fc;
        margin-bottom: 10px;
    }

    .tp-next-row {
        max-width: 1200px;
        margin: 12px auto 32px auto;
        width: 100%;
        text-align: right;
    }
    .tp-next-btn {
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

# ---------------- HEADER (Back + Profile) ----------------
st.markdown('<div class="tp-header">', unsafe_allow_html=True)
c1, c_mid, c3 = st.columns([1, 6, 1])

with c1:
    back_clicked = st.button("← Back", key="tp_back_btn")

with c3:
    with st.popover(avatar_label):
        st.write(f"**{name}**")
        st.write(email or "")
        st.markdown("---")
        if st.button("My Profile 👤"):
            st.switch_page("pages/5_My_Profile.py")
        if st.button("Logout ⏻"):
            st.session_state.clear()
            st.switch_page("pages/0_Welcome.py")

st.markdown("</div>", unsafe_allow_html=True)

# Style the header buttons
st.markdown(
    f"""
    <script>
    const btns = window.parent.document.querySelectorAll("button");
    btns.forEach(b => {{
      if (b.innerText.trim() === "← Back") {{
        b.classList.add("tp-back-btn");
      }}
      if (b.innerText.trim() === "{avatar_label}") {{
        b.classList.add("tp-avatar-btn");
      }}
    }});
    </script>
    """,
    unsafe_allow_html=True,
)

if back_clicked:
    st.switch_page("pages/6_Hiring_Process.py")

# ---------------- TITLE ----------------
st.markdown(
    """
    <div class="tp-title-wrap">
      <div class="tp-title-main">Choose your test</div>
      <div class="tp-title-sub">
        Pick a section or stage from your hiring process to practice.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- CARDS GRID ----------------

# Aptitude row
st.markdown("<br>", unsafe_allow_html=True)
apt_cols = st.columns(4)

apt_keys = ["quantitative", "logical", "verbal", "aptitude_mix"]

for col, key in zip(apt_cols, apt_keys):
    cfg = TEST_CONFIG[key]
    with col:
        with st.container(border=False):
            st.markdown(
                f"""
                <div class="tp-card">
                  <div class="tp-card-title">{cfg['title']}</div>
                  <div class="tp-card-desc">{cfg['description']}</div>
                  <div class="tp-card-meta">
                    {cfg['num_questions']} questions · {cfg['time_limit_minutes']} minutes
                  </div>
                """,
                unsafe_allow_html=True,
            )
            start = st.button("Start this test", key=f"start_{key}")
            st.markdown("</div>", unsafe_allow_html=True)
            if start:
                st.session_state["selected_test_key"] = key
                st.experimental_rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Technical + Interview row
row2_cols = st.columns(3)
row2_keys = ["technical_mcq", "tech_interview", "hr_interview"]

for col, key in zip(row2_cols, row2_keys):
    cfg = TEST_CONFIG[key]
    with col:
        with st.container(border=False):
            st.markdown(
                f"""
                <div class="tp-card">
                  <div class="tp-card-title">{cfg['title']}</div>
                  <div class="tp-card-desc">{cfg['description']}</div>
                  <div class="tp-card-meta">
                    {cfg['num_questions']} questions · {cfg['time_limit_minutes']} minutes
                  </div>
                """,
                unsafe_allow_html=True,
            )
            start = st.button("Start this test", key=f"start_{key}")
            st.markdown("</div>", unsafe_allow_html=True)
            if start:
                st.session_state["selected_test_key"] = key
                st.experimental_rerun()

# ---------------- CONFIRMATION MODAL ----------------
selected_key = st.session_state.get("selected_test_key")
if selected_key:
    cfg = TEST_CONFIG[selected_key]
    with st.modal(f"{cfg['title']}"):
        st.write(f"### {cfg['title']}")
        st.write(cfg["description"])
        st.markdown(
            f"- **Questions:** {cfg['num_questions']}\n"
            f"- **Time limit:** {cfg['time_limit_minutes']} minutes\n"
            f"- **Difficulty:** {cfg['difficulty']}"
        )
        st.info("Once you start, the timer will begin and the test must be completed in one sitting.")

        col_a, col_b = st.columns(2)
        with col_a:
            confirm = st.button("Start Test ✅", key="confirm_start_test")
        with col_b:
            cancel = st.button("Cancel ✖", key="cancel_start_test")

        if cancel:
            st.session_state["selected_test_key"] = None
            st.experimental_rerun()

        if confirm:
            # Prepare session state for the actual test screen
            st.session_state["active_test"] = {
                "category": selected_key,
                "title": cfg["title"],
                "num_questions": cfg["num_questions"],
                "time_limit_minutes": cfg["time_limit_minutes"],
                "difficulty": cfg["difficulty"],
            }
            # Placeholders for questions and user answers
            st.session_state["questions"] = []       # to be filled by AI / DB on test screen
            st.session_state["user_answers"] = []    # user selections

            st.session_state["selected_test_key"] = None
            st.switch_page("pages/8_Test_Screen.py")

# ---------------- NEXT BUTTON (bottom-right) ----------------
st.markdown('<div class="tp-next-row">', unsafe_allow_html=True)
next_clicked = st.button("Next ➜", key="tp_next_btn")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <script>
    const nbtns = window.parent.document.querySelectorAll("button");
    nbtns.forEach(b => {
      if (b.innerText.trim() === "Next ➜") {
        b.classList.add("tp-next-btn");
      }
    });
    </script>
    """,
    unsafe_allow_html=True,
)

if next_clicked:
    # Placeholder – this will be your results / progress page
    st.switch_page("pages/8_Test_Results.py")
