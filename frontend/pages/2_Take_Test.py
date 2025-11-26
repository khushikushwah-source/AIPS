import streamlit as st
import requests

API_BASE = "http://localhost:5000/api"

st.set_page_config(page_title="Take Test", page_icon="📝", layout="wide")

st.title("📝 Take a Test")

# Fetch companies
companies = requests.get(f"{API_BASE}/companies/").json()
company_names = [c['name'] for c in companies]

company = st.selectbox("Choose Company", company_names)
selected_company = next((c for c in companies if c['name'] == company), None)

# Fetch tests for company
if selected_company:
    tests = requests.get(f"{API_BASE}/tests/?company_id={selected_company['company_id']}").json()
    if tests:
        test_names = [t["test_type"] + " - " + t["test_id"] for t in tests]
        selected_test_name = st.selectbox("Select Test", test_names)

        selected_test = next((t for t in tests if (t['test_type'] + " - " + t['test_id']) == selected_test_name), None)
    else:
        st.warning("No tests found for this company.")
        selected_test = None
else:
    selected_test = None

if selected_test:
    st.info(f"Selected Test: {selected_test['test_id']}")

    if st.button("Start Test"):
        response = requests.post(
            f"{API_BASE}/attempts/start",
            json={"test_id": selected_test["test_id"], "id_token": "TEST_USER_TOKEN"}
        )

        if response.status_code == 201:
            data = response.json()
            st.session_state["attempt_id"] = data["attempt_id"]
            st.session_state["test"] = data["test"]

            st.success("Test Started!")
        else:
            st.error("Unable to start test.")

    # If test already started
    if "test" in st.session_state:
        st.subheader("Questions")

        answers = []

        for q in st.session_state["test"]["question_ids"]:
            q_data = requests.get(f"{API_BASE}/questions/{q}").json()

            st.write(f"### {q_data['text']}")

            if q_data["type"] == "mcq":
                resp = st.radio("Select Answer", q_data["options"], key=q)
            else:
                resp = st.text_area("Your Answer:", key=q)

            answers.append({
                "question_id": q,
                "response": resp,
                "type": q_data["type"],
                "expected_answer": q_data.get("expected_answer"),
                "expected_keywords": q_data.get("expected_keywords")
            })

        if st.button("Submit Test"):
            response = requests.post(
                f"{API_BASE}/attempts/submit",
                json={
                    "attempt_id": st.session_state["attempt_id"],
                    "answers": answers,
                    "id_token": "TEST_USER_TOKEN"
                }
            )

            if response.status_code == 200:
                st.success(f"Test Submitted! Your Score: {response.json()['score']}")
            else:
                st.error("Submission failed.")
