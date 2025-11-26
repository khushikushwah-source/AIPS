import streamlit as st
import requests

API_BASE = "http://localhost:5000/api"

st.set_page_config(page_title="Results", page_icon="📚", layout="wide")

st.title("📚 Your Test Results")

USER_ID = "TEST_USER_ID"  # Replace when integrating Firebase Auth

results = requests.get(f"{API_BASE}/attempts/user/{USER_ID}", json={"id_token": "TEST_USER_TOKEN"}).json()

if results:
    for r in results:
        st.subheader(f"Test ID: {r['test_id']}")
        st.write(f"Score: {r.get('score', 'Not graded')}")
        st.write(f"Started: {r.get('started_at')}")
        st.write(f"Finished: {r.get('finished_at')}")
        st.markdown("---")
else:
    st.info("No results found.")
