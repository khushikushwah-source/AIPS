import streamlit as st

def domain_card(title, description, tags):
    st.markdown(f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
        ">
            <h3>{title}</h3>
            <p>{description}</p>
            <b>Tags:</b> {", ".join(tags)}
        </div>
    """, unsafe_allow_html=True)


def hiring_step_card(stage, description, tips):
    st.markdown(f"""
        <div style="
            border-left: 5px solid #4CAF50;
            padding: 15px;
            margin: 15px 0;
            background-color: #eef6ee;
            border-radius: 5px;
        ">
            <h4>🟦 {stage}</h4>
            <p>📄 {description}</p>
            <p><b>💡 Tip:</b> {tips}</p>
        </div>
    """, unsafe_allow_html=True)


def test_info_card(test_id, test_type, difficulty, duration):
    st.markdown(f"""
        <div style="
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 12px;
            background-color: #ffffff;
            margin: 10px 0;
        ">
            <h4>{test_type} ({test_id})</h4>
            <p><b>Difficulty:</b> {difficulty}</p>
            <p><b>Duration:</b> {duration} mins</p>
        </div>
    """, unsafe_allow_html=True)
