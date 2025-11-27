import streamlit as st
import requests

API_BASE = "http://localhost:5000/api"

st.set_page_config(page_title="Hiring Process", page_icon="🔁", layout="wide")

st.title("🔁 Hiring Process Flow")

companies = requests.get(f"{API_BASE}/companies/").json()

company_names = [c["name"] for c in companies]
selected = st.selectbox("Choose Company", company_names)

company = next((c for c in companies if c["name"] == selected), None)

if company:
    st.header(f"{company['name']} — Hiring Steps")

    for step in company["hiring_flow"]:
        st.subheader(f"🟦 {step['stage_name']}")
        st.write(f"📄 {step['description']}")
        st.info(f"💡 Tip: {step['tips']}")
        st.markdown("---")
else:
    st.warning("No company selected.")
