import streamlit as st

st.set_page_config(page_title="Menu", layout="centered")
st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

if not st.session_state.auth:
    st.warning("Please login first.")
    st.stop()

st.title("Main Menu")
if st.button("Dashboard"):
    st.query_params["page"] = "dashboard"
    st.rerun()
if st.button("Interview"):
    st.query_params["page"] = "interview"
    st.rerun()
if st.button("Logout"):
    st.session_state.clear()
    st.rerun()
