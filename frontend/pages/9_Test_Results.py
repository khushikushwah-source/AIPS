import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AIPS — Test Result", page_icon="🏆", layout="wide")

# -------------- AUTH CHECK --------------
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.switch_page("2_Login.py")

user = st.session_state.get("user", {})
email = user.get("email", "")

# -------------- RESULT DATA CHECK --------------
if "test_result" not in st.session_state:
    st.error("No test result found. Please attempt a test first.")
    st.stop()

result = st.session_state["test_result"]
score = result.get("score", 0)
total = result.get("total", 0)
percentage = result.get("percentage", 0.0)
time_taken = int(result.get("time_taken", 0))
category = result.get("category", "")
title = result.get("title", "Test Result")

# time format
mins = time_taken // 60
secs = time_taken % 60

# correct / wrong
correct = score
wrong = total - score

# -------------- BADGE LOGIC --------------
if percentage >= 90:
    status = "Excellent"
    badge_icon = "🟢"
    badge_color = "#22c55e"
    status_text = "PASS"
elif percentage >= 75:
    status = "Very Good"
    badge_icon = "🔵"
    badge_color = "#3b82f6"
    status_text = "PASS"
elif percentage >= 50:
    status = "Good"
    badge_icon = "🟡"
    badge_color = "#eab308"
    status_text = "PASS"
else:
    status = "Needs Improvement"
    badge_icon = "🔴"
    badge_color = "#ef4444"
    status_text = "FAIL"

# -------------- GLOBAL CSS --------------
st.markdown(
    f"""
<style>
#MainMenu, header, footer {{visibility: hidden;}}
section[data-testid="stSidebar"] {{display: none !important;}}
html, body, [data-testid="stAppViewContainer"], .main {{ background: #020617; }}

.result-card {{
    margin-top: 30px;
    padding: 24px 28px;
    border-radius: 20px;
    background: radial-gradient(circle at top left, #1d4ed8, #020617);
    box-shadow: 0 18px 45px rgba(15,23,42,0.8);
    color: #e5e7eb;
}}

.result-title {{
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 4px;
}}

.result-subtitle {{
    font-size: 16px;
    color: #cbd5f5;
    margin-bottom: 18px;
}}

.badge-pill {{
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    background: {badge_color}33;
    border: 1px solid {badge_color};
    color: {badge_color};
    font-weight: 600;
    margin-left: 10px;
    font-size: 14px;
}}

.metric-box {{
    padding: 14px 16px;
    border-radius: 14px;
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(148,163,184,0.4);
    text-align: center;
}}

.metric-label {{
    font-size: 14px;
    color: #9ca3af;
}}

.metric-value {{
    font-size: 22px;
    font-weight: 700;
    color: #e5e7eb;
}}

.action-btn {{
    border-radius: 999px !important;
    padding: 8px 22px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

# -------------- TOP HEADING --------------
st.markdown(
    f"""
<div style="text-align:center; margin-top:10px;">
    <h2 style="color:#e5e7eb; font-size:30px;">🏆 Test Completed</h2>
    <p style="color:#9ca3af; font-size:16px; margin-top:4px;">
        {title} &nbsp;·&nbsp; <span style="color:#60a5fa;">{category}</span>
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# -------------- MAIN SCORE CARD --------------
st.markdown("<div class='result-card'>", unsafe_allow_html=True)

c1, c2 = st.columns([2, 1])

with c1:
    st.markdown(
        f"""
        <div class="result-title">
            Overall Performance: {score}/{total}
            <span class="badge-pill">{badge_icon} {status} · {status_text}</span>
        </div>
        <div class="result-subtitle">
            Nice work, {user.get("name","Candidate")}! Here's how you performed in this attempt.
        </div>
        """,
        unsafe_allow_html=True,
    )

    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Score</div>
                <div class="metric-value">{score} / {total}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mcol2:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Accuracy</div>
                <div class="metric-value">{percentage:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mcol3:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Time Taken</div>
                <div class="metric-value">{mins}m {secs}s</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with c2:
    # focus on correct vs wrong
    circle_text = f"{correct} Correct\n{wrong} Wrong"
    st.markdown(
        f"""
        <div style="
            border-radius: 999px;
            width: 160px;
            height: 160px;
            border: 4px solid {badge_color};
            display: flex;
            align-items: center;
            justify-content: center;
            text-align:center;
            white-space: pre-line;
            font-size: 16px;
            font-weight:600;
            color:#e5e7eb;
            margin:auto;
            background: rgba(15,23,42,0.8);
        ">
            {circle_text}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# -------------- GRAPH: CORRECT VS WRONG --------------
st.markdown(
    "<h4 style='color:#e5e7eb; margin-top:24px;'>📊 Correct vs Wrong</h4>",
    unsafe_allow_html=True,
)

graph_col1, graph_col2 = st.columns([1.5, 2])

with graph_col1:
    df = pd.DataFrame(
        {
            "Result": ["Correct", "Wrong"],
            "Count": [correct, max(wrong, 0)],
        }
    ).set_index("Result")
    st.bar_chart(df, height=220)

with graph_col2:
    st.write("")
    st.write(
        f"""
    - ✅ **Correct:** {correct}  
    - ❌ **Wrong:** {wrong}  
    - 🎯 **Accuracy:** {percentage:.1f}%  
    """
    )
    if percentage >= 75:
        st.success("Great job! You're on track for most company aptitude / technical rounds. Keep practicing to reach 90%+.")
    elif percentage >= 50:
        st.info("Decent performance! Thoda aur practice karo — specially incorrect questions par dobara focus karo.")
    else:
        st.warning("Don't worry! Ye sirf practice test hai. Incorrect questions dekho, concepts revise karo and try again. 🙂")

# -------------- QUESTION-WISE SUMMARY --------------
questions = st.session_state.get("questions", [])
user_answers = st.session_state.get("user_answers", [])

st.markdown(
    "<h4 style='color:#e5e7eb; margin-top:28px;'>📌 Question-wise Summary</h4>",
    unsafe_allow_html=True,
)

if questions and user_answers:
    rows = []
    for i, q in enumerate(questions):
        ua = user_answers[i] if i < len(user_answers) else ""
        ca = q.get("answer", "")
        result_icon = "✔" if ua == ca else "❌"
        rows.append(
            {
                "Q#": i + 1,
                "Question": q.get("question", "")[:80] + ("..." if len(q.get("question", "")) > 80 else ""),
                "Your Answer": ua or "-",
                "Correct Answer": ca,
                "Result": result_icon,
            }
        )

    df_q = pd.DataFrame(rows)
    st.dataframe(df_q, use_container_width=True, height=320)
else:
    st.write("No detailed question data found for this test.")

# -------------- ACTION BUTTONS --------------
st.write("")
bcol1, bcol2, bcol3 = st.columns([1, 1, 3])

with bcol1:
    if st.button("🔁 Retry Test", use_container_width=True):
        # sirf test-related states clear karo
        for key in ["questions", "user_answers", "current_q", "start_time",
                    "auto_submit", "test_result"]:
            st.session_state.pop(key, None)

        # agar active_test missing hai to pehle test select karvao
        if "active_test" not in st.session_state:
            st.switch_page("pages/7_Test_Page.py")
        else:
            # same test dobara chalu hoga
            st.switch_page("pages/8_test_Screen.py")

with bcol2:
    if st.button("🏠 Back to Dashboard", use_container_width=True):
        st.switch_page("pages/7_Test_Page.py")

