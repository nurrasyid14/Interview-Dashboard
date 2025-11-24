# pages/_3_Menu.py
import streamlit as st

def render():
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

    if not st.session_state.auth:
        st.warning("Please login first.")
        st.stop()

    st.title(f"Welcome, {st.session_state.auth_user}!")
    st.info("Select an option below:")

    col1, col2, col3 = st.columns(3)
    if col1.button("Dashboard"):
        st.query_params['page']="dashboard"
        st.rerun()
    if col2.button("Interview"):
        st.query_params['page']="interview"
        st.rerun()
    if col3.button("Logout"):
        st.session_state.clear()
        st.rerun()
