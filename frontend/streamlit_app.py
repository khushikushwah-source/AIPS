# frontend/streamlit_app.py
import streamlit as st
from pathlib import Path
import importlib.util
import sys
import os

# -----------------------
# Basic config & hide Streamlit chrome (optional)
# -----------------------
st.set_page_config(page_title="AIPS", page_icon="🤖", layout="wide")
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      header {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Load welcome module from pages/0_Welcome.py dynamically
# -----------------------
ROOT = Path(_file_).resolve().parent  # frontend/
welcome_path = ROOT / "pages" / "0_Welcome.py"

if not welcome_path.exists():
    st.error(f"Welcome page not found at {welcome_path}. Make sure frontend/pages/0_Welcome.py exists.")
    st.stop()

spec = importlib.util.spec_from_file_location("welcome_page", str(welcome_path))
welcome_mod = importlib.util.module_from_spec(spec)
sys.modules["welcome_page"] = welcome_mod
spec.loader.exec_module(welcome_mod)

# The welcome module is expected to export:
#   - render_welcome()
#   - render_auth_forms()
#   - (optional) main_after_enter()
# If names differ, adjust below.

# -----------------------
# Ensure session flags (streamlit session_state is shared across modules)
# -----------------------
if "entered" not in st.session_state:
    st.session_state["entered"] = False
if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = None

# -----------------------
# Show welcome or main app
# -----------------------
if not st.session_state["entered"]:
    # Call functions from the welcome module to render the hero and the auth forms.
    # These functions write to the same Streamlit context.
    if hasattr(welcome_mod, "render_welcome"):
        welcome_mod.render_welcome()
    else:
        st.error("render_welcome() not found in welcome module.")

    # Render inline auth forms if present
    if hasattr(welcome_mod, "render_auth_forms"):
        welcome_mod.render_auth_forms()
else:
    # After "entered" show the main app. If welcome module provides a main_after_enter() function, call it.
    if hasattr(welcome_mod, "main_after_enter"):
        welcome_mod.main_after_enter()
    else:
        # fallback: simple main UI
        st.sidebar.title("AIPS")
        page = st.sidebar.radio("Navigation", ["Dashboard", "Take Test", "Hiring Flow", "Results", "Sign out"])
        st.header("AI Interview Preparation System")
        if page == "Dashboard":
            st.write("Dashboard (placeholder)")
        elif page == "Take Test":
            st.write("Take Test (placeholder)")
        elif page == "Hiring Flow":
            st.write("Hiring Flow (placeholder)")
        elif page == "Results":
            st.write("Results (placeholder)")
        elif page == "Sign out":
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.session_state["entered"] = False
            st.experimental_rerun()