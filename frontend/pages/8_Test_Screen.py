import streamlit as st
import time
import json
import os

from datetime import datetime

st.set_page_config(page_title="AIPS — Test", page_icon="📝", layout="wide")

# ---------------- AUTH CHECK ----------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
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
time_limit = test_info["time_limit"] * 60  # convert to seconds

# ---------------- TIMER SETUP ----------------
if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()

elapsed = int(time.time() - st.session_state["start_time"])
remaining = max(time_limit - elapsed, 0)

# auto submit when time over
if remaining <= 0:
    st.session_state["auto_submit"] = True

# ---------------- UI CSS ----------------
st.markdown("""
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

/* BIG OPTION CARDS */
.option-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 16px;
    border-radius: 14px;
    margin: 10px 0;
    cursor: pointer;
    transition: 0.25s;
}
.option-card:hover {
    transform: scale(1.02);
    border-color: #3b82f6;
}
.selected-opt {
    background: #0ea5e9 !important;
    color: black !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER (Back Disabled During Test) ----------------
st.write("")
st.markdown(
    f"<h3 style='color:white;'>📝 {test_info['title']}</h3>",
    unsafe_allow_html=True,
)

# ---------------- TIMER DISPLAY ----------------
mins = remaining // 60
secs = remaining % 60
st.markdown(f"<div class='timer-box'>⏳ {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)

# ---------------- LOAD QUESTIONS ----------------
if "questions" not in st.session_state or len(st.session_state["questions"]) == 0:
    # Load static questions JSON
    questions = []

    # 8_Test_Screen.py is in: frontend/pages/
# So parent folder = frontend (jaha JSON file rakhi hai)
    base_dir = os.path.dirname(os.path.dirname(__file__))   # .../frontend
    questions_path = os.path.join(base_dir, "questions_bank.json")

    with open(questions_path, "r", encoding="utf-8") as f:
        data = json.load(f)


    data = json.load(f)

    # filter
    user_company = user.get("company", "")
    filtered = [q for q in data if q["category"] == category and q["company"] == user_company]

    # if shortage, pick more from same category
    if len(filtered) < num_questions:
        extra = [q for q in data if q["category"] == category]
        filtered = filtered + extra

    # pick required number
    final_questions = filtered[:num_questions]
    st.session_state["questions"] = final_questions
    st.session_state["user_answers"] = [""] * num_questions
    st.session_state["current_q"] = 0

questions = st.session_state["questions"]
user_answers = st.session_state["user_answers"]
index = st.session_state["current_q"]
question = questions[index]

# ---------------- RENDER QUESTION ----------------
st.markdown(
    f"<h4 style='color:#f1f5f9;'>Q{index+1}. {question['question']}</h4>",
    unsafe_allow_html=True
)

options = question["options"]
selected = user_answers[index]

for opt in options:
    selected_class = "selected-opt" if opt == selected else ""
    if st.button(opt, key=f"opt_{index}_{opt}"):
        st.session_state["user_answers"][index] = opt
    st.markdown(f"<div class='option-card {selected_class}'>{opt}</div>", unsafe_allow_html=True)

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
        if user_answers[i] == q["answer"]:
            score += 1

    percentage = (score / num_questions) * 100

    st.session_state["test_result"] = {
        "score": score,
        "total": num_questions,
        "percentage": percentage,
        "time_taken": time_limit - remaining,
        "timestamp": datetime.now().isoformat(),
        "category": category
    }

    st.switch_page("pages/9_Test_Results.py")
