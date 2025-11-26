import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection("users")     # like SQL table
