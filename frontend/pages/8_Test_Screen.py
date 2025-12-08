import streamlit as st
import time
import json
import os
import random
from datetime import datetime

st.set_page_config(page_title="AIPS — Test", page_icon="📝", layout="wide")

# ---------------- AUTH CHECK ----------------
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.switch_page("pages/2_Login.py")

user = st.session_state.get("user", {})
email = user.get("email")
if not email:
    st.error("User email missing. Please login again.")
    st.stop()

# ---------------- ACTIVE TEST CHECK ----------------
if "active_test" not in st.session_state:
    st.error("No test selected. Please pick a test first.")
    st.switch_page("pages/7_Test_Page.py")

test_info = st.session_state["active_test"]
category = test_info["category"]
num_questions = test_info["num_questions"]
time_limit = test_info["time_limit"] * 60  # seconds

# ---------------- TIMER SETUP ----------------
if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()

elapsed = int(time.time() - st.session_state["start_time"])
remaining = max(time_limit - elapsed, 0)

# time khatam -> auto submit flag
if remaining <= 0:
    st.session_state["auto_submit"] = True

# ---------------- UI CSS ----------------
st.markdown(
    """
<style>
#MainMenu, header, footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: none !important;}
html, body, [data-testid="stAppViewContainer"], .main { background: #020617; }

.timer-box {
    position: fixed;
    top: 18px;
    right: 24px;
    background: #1e293b;
    padding: 10px 18px;
    border-radius: 12px;
    font-size: 20px;
    color: #38bdf8;
    font-weight: 700;
    border: 1px solid #334155;
}

/* radio ko card jaisa look */
div[data-testid="stRadio"] > div {
    background: transparent;
}
div[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 10px;
    width: 100%;
    cursor: pointer;
}
div[data-testid="stRadio"] label:hover {
    transform: scale(1.01);
    border-color: #3b82f6;
}

/* pehla dummy option hide kar do (taaki visible options sab unselected lagen) */
div[data-testid="stRadio"] > div > label:first-child {
    display: none !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------- HEADER ----------------
st.write("")
st.markdown(
    f"<h3 style='color:white;'>📝 {test_info['title']}</h3>",
    unsafe_allow_html=True,
)

# ---------------- TIMER DISPLAY ----------------
mins = remaining // 60
secs = remaining % 60
st.markdown(
    f"<div class='timer-box'>⏳ {mins:02d}:{secs:02d}</div>",
    unsafe_allow_html=True,
)

# ---------------- LOAD QUESTIONS (FROM JSON, ONCE) ----------------
if "questions" not in st.session_state or len(st.session_state["questions"]) == 0:
    # 8_Test_Screen.py is in: frontend/pages/
    base_dir = os.path.dirname(os.path.dirname(__file__))  # .../frontend
    questions_path = os.path.join(base_dir, "questions_bank.json")

    try:
        with open(questions_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        st.error("questions_bank.json not found. Please check file path.")
        st.stop()

    all_questions = []

    # JSON dict: { "Infosys_Software Developer": [ {...}, {...} ], ... }
    if isinstance(data, dict):
        company = user.get("company", "")
        domain = user.get("domain", "")
        key = f"{company}_{domain}" if company and domain else None

        if key and key in data:
            all_questions = data[key]
        else:
            # fallback: sab company/domain ke questions mila do
            for qs_list in data.values():
                all_questions.extend(qs_list)
    elif isinstance(data, list):
        all_questions = data

    if not all_questions:
        st.error("No questions found in questions_bank.json.")
        st.stop()

    # jitne test me chahiye utne hi random questions lo
    if len(all_questions) >= num_questions:
        final_questions = random.sample(all_questions, num_questions)
    else:
        final_questions = all_questions
        num_questions = len(final_questions)
        st.session_state["active_test"]["num_questions"] = num_questions

    st.session_state["questions"] = final_questions
    st.session_state["user_answers"] = [""] * num_questions
    st.session_state["current_q"] = 0

# ab session se lo
questions = st.session_state["questions"]
user_answers = st.session_state["user_answers"]
index = st.session_state["current_q"]
question = questions[index]

# ---------------- RENDER QUESTION ----------------
st.markdown(
    f"<h4 style='color:#f1f5f9;'>Q{index + 1} of {len(questions)}</h4>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<h3 style='color:#e2e8f0; margin-top:6px;'>{question['question']}</h3>",
    unsafe_allow_html=True,
)

options = question["options"]

# ----- RADIO: koi label nahi, koi real option preselect nahi -----
current_sel = user_answers[index] if user_answers[index] in options else None

# dummy + real options
DUMMY_VALUE = "__none__"
radio_options = [DUMMY_VALUE] + options

if current_sel:
    default_index = 1 + options.index(current_sel)  # shift by 1 (dummy)
else:
    default_index = 0  # sirf dummy selected (jo CSS se hidden hai)

selected = st.radio(
    "",
    radio_options,
    index=default_index,
    key=f"q_{index}",
    label_visibility="collapsed",
)

# dummy ko ignore karo
if selected == DUMMY_VALUE:
    st.session_state["user_answers"][index] = ""
else:
    st.session_state["user_answers"][index] = selected

# ---------------- QUESTION NAVIGATION ----------------
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if index > 0:
        if st.button("⬅ Previous"):
            st.session_state["current_q"] -= 1
            st.rerun()

with col3:
    if index < num_questions - 1:
        if st.button("Next ➜"):
            st.session_state["current_q"] += 1
            st.rerun()

# ---------------- SUBMIT ----------------
submit_now = st.button("Submit Test ✔")

if submit_now or st.session_state.get("auto_submit"):
    score = 0
    for i, q in enumerate(questions):
        if st.session_state["user_answers"][i] == q.get("answer"):
            score += 1

    total = len(questions)
    percentage = (score / total) * 100 if total > 0 else 0

    st.session_state["test_result"] = {
        "score": score,
        "total": total,
        "percentage": percentage,
        "time_taken": time_limit - remaining,
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "title": test_info["title"],
    }

    st.switch_page("pages/9_Test_Results.py")

# ---------------- AUTO REFRESH FOR LIVE TIMER ----------------
# jab tak time bacha hai aur submit nahi hua, har 1 second me page rerun
if remaining > 0 and not st.session_state.get("auto_submit"):
    time.sleep(1)
    st.rerun()
