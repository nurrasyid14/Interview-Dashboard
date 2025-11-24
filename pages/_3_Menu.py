# pages/_3_Menu.py
import streamlit as st

def render():
    st.set_page_config(page_title="Menu", layout="centered")
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

    if not st.session_state.get("auth"):
        st.warning("Please login first.")
        st.stop()

    st.title(f"Welcome, {st.session_state.get('auth_user')}!")
    st.info("Select an option below:")

    col1, col2, col3 = st.columns(3)
    if col1.button("Interview"):
        st.session_state["next_page"] = "interview"
        st.rerun()
    if col2.button("Dashboard"):
        st.session_state["next_page"] = "dashboard"
        st.rerun()
    if col3.button("Logout"):
        # clear session and go to login
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.session_state["next_page"] = "login"
        st.rerun()
