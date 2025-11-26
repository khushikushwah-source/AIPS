import streamlit as st

def load_navbar():
    st.markdown("""
        <style>
            .navbar {
                background-color: #2b2b2b;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .navbar h2 {
                color: white;
                margin: 0;
                display: inline-block;
            }
        </style>

        <div class="navbar">
            <h2>🤖 AI Interview Preparation System</h2>
        </div>
    """, unsafe_allow_html=True)
