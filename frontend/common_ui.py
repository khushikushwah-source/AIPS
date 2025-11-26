import streamlit as st

# Call this at the TOP of every page
def setup_page(title: str, page_id: str):
    """
    title: page title text
    page_id: string used for navigation, e.g. 'pages/1_Register.py'
    """

    # Set basic config once
    st.set_page_config(page_title=f"{title} | AIPS", page_icon="🤖", layout="wide")

    # Hide sidebar, header, footer
    st.markdown(
        """
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            section[data-testid="stSidebar"] {display: none !important;}  /* hide sidebar */
            .block-container {padding-top: 1.5rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---- Navigation history in session_state ----
    history = st.session_state.get("nav_history", [])

    # If first time, initialise
    if not history:
        history = [page_id]
    else:
        # Avoid pushing same page repeatedly
        if history[-1] != page_id:
            history.append(page_id)
    st.session_state["nav_history"] = history

    # ---- Top row: Back button + Title ----
    back_col, title_col = st.columns([1, 9])

    with back_col:
        if len(history) > 1:  # only show back if something to go back to
            if st.button("← Back"):
                history.pop()              # remove current page
                prev_page = history[-1]    # previous page
                st.session_state["nav_history"] = history
                st.switch_page(prev_page)
        else:
            st.write("")  # spacing

    with title_col:
        st.title(title)
