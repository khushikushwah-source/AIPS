import os

# --------------------------------------------
# Frontend Configuration for Streamlit App
# --------------------------------------------

# Base URL of your Flask backend API
API_BASE = os.getenv("API_BASE", "http://localhost:5000/api")

# Dummy user values (replace later when Firebase Auth is added)
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "TEST_USER_ID")
DEFAULT_ID_TOKEN = os.getenv("DEFAULT_ID_TOKEN", "TEST_USER_TOKEN")

# UI branding
APP_NAME = "AI Interview Preparation System"
APP_LOGO = "assets/images/logo.png"   # optional

# Pagination settings for results page
DEFAULT_PAGE_SIZE = 10
