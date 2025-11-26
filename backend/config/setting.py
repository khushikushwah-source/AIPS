import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

class Settings:
    # Flask app settings
    DEBUG = os.getenv("DEBUG", "True") == "True"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))

    # Firebase service account file
    FIREBASE_CREDENTIALS = os.getenv(
        "FIREBASE_CREDENTIALS",
        "backend/config/firebase_config.json"
    )

    # Firestore collection names
    COLLECTION_DOMAINS = "domains"
    COLLECTION_COMPANIES = "companies"
    COLLECTION_TESTS = "tests"
    COLLECTION_QUESTIONS = "questions"
    COLLECTION_ATTEMPTS = "attempts"
    COLLECTION_USERS = "users"

settings = Settings()
