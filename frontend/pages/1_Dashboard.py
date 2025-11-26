import streamlit as st
import requests

API_BASE = "http://localhost:5000/api"

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard")

st.write("Welcome to the AI Interview Preparation System!")

# Fetch domains
st.subheader("Available Domains")
domains = requests.get(f"{API_BASE}/domains/").json()

for domain in domains:
    st.markdown(f"### 🔹 {domain['name']}")
    st.write(domain["description"])
    st.write(f"**Tags:** {', '.join(domain['tags'])}")
    st.divider()

st.success("Use the sidebar to navigate between Test, Hiring Flow, and Results pages.")
