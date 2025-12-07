import streamlit as st
import google.generativeai as genai
import json
from firebase_config import db

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("models/text-bison-001")

def get_hiring_process(company, domain):
    doc_ref = db.collection("hiring_process").document(f"{company}_{domain}")
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()["stages"]

    prompt = f"""
    Create a structured hiring process for {company} for {domain} role.
    Format response strictly in JSON list (no extra text):
    [
      {{
        "title": "",
        "time": "",
        "sections": [
          {{"name": "", "topics": ["", "", ""]}}
        ]
      }}
    ]
    """
    
    response = model.generate_content(prompt)
    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    stages = json.loads(text)

    doc_ref.set({"stages": stages})
    return stages
