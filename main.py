# main.py
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="AI Job Interview System",
    layout="centered",
)

# ----------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------
def init():
    defaults = {
        "authenticated": False,
        "identity_filled": False,
        "interview_started": False,
        "interview_done": False,
        "judger": None,
        "user": {}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ----------------------------------------------------------------------
# Hide default Streamlit multipage sidebar
# ----------------------------------------------------------------------
hide_style = """
<style>
    section[data-testid="stSidebar"] {display: none;}
    div[data-testid="stToolbar"] {display: none;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Logout Handler
# ----------------------------------------------------------------------
def handle_logout():
    if "logout" in st.query_params:
        if st.query_params["logout"] == "1":
            st.session_state.clear()
            st.rerun()

handle_logout()

# ----------------------------------------------------------------------
# Navbar (minimal)
# ----------------------------------------------------------------------
def navbar():
    st.markdown(
        """
        <style>
        .nav {
            background:#222;padding:12px;border-radius:6px;
            display:flex;justify-content:space-between;
        }
        .nav a {color:white;text-decoration:none;margin-right:15px;}
        .nav a:hover {color:#1f77ff;}
        </style>
        <div class="nav">
            <div>
                <a href="/">Home</a>
            </div>
            <div>
                <a href="/?logout=1">Logout</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

navbar()

# ----------------------------------------------------------------------
# ROUTER — Force user to correct page
# ----------------------------------------------------------------------
def route():
    if not st.session_state.authenticated:
        switch_page("Login")

    elif st.session_state.authenticated and not st.session_state.identity_filled:
        switch_page("Identity")

    elif st.session_state.identity_filled and not st.session_state.interview_done:
        switch_page("Interview")

    elif st.session_state.interview_done:
        switch_page("Result")

route()

# ----------------------------------------------------------------------
# Main Page Body (Only shown if someone directly arrives here)
# ----------------------------------------------------------------------
st.title("AI Job Interview System")

if st.session_state.interview_done:
    st.success("Interview finished. You can now view your Result or Dashboard.")
else:
    st.info("Redirecting...")

