#main.py
import streamlit as st
from app.modules.frontend_loader import load_css, load_js

st.set_page_config(page_title="AI Job Interview System",
                    layout="centered",
                    initial_sidebar_state="collapsed",
)

load_css()
load_js()


# ----------------------------------------------------------------------
# Initialize session state
# ----------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "auth" not in st.session_state:
    st.session_state.auth = False

if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

if "user_metadata" not in st.session_state:
    st.session_state.user_metadata = {}

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "interview_done" not in st.session_state:
    st.session_state.interview_done = False

if "judger" not in st.session_state:
    st.session_state.judger = None

if "level" not in st.session_state:
    st.session_state.level = None

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "_leveling_count" not in st.session_state:
    st.session_state._leveling_count = 0

if "final_report" not in st.session_state:
    st.session_state.final_report = None

if "completed" not in st.session_state:
    st.session_state.completed = False

if "identity_filled" not in st.session_state:
    st.session_state.identity_filled = False


# ----------------------------------------------------------------------
# Navbar (top)
# ----------------------------------------------------------------------
def navbar():
    st.markdown(
        """
        <style>
            .navbar {
                background-color: #222;
                padding: 12px;
                border-radius: 6px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .navbar a {
                color: #fff;
                margin-right: 16px;
                text-decoration: none;
                font-weight: 500;
            }
            .navbar a:hover {
                color: #1f77ff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    left_links = """
        <div>
            <a href="/">Home</a>
            <a href="/Login">Login</a>
            <a href="/Identity">Identity</a>
            <a href="/Interview">Interview</a>
            <a href="/Result">Result</a>
            <a href="/Dashboard">Dashboard</a>
        </div>
    """

    right_links = """
        <div>
            <a href="/?logout=1">Logout</a>
        </div>
    """

    st.markdown(f'<div class="navbar">{left_links}{right_links}</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Logout Handler
# ----------------------------------------------------------------------
def handle_logout():
    if "logout" in st.query_params:
        if st.query_params["logout"] == "1":
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ----------------------------------------------------------------------
# Main App Entry
# ----------------------------------------------------------------------
def main():
    handle_logout()
    navbar()

    st.title("Welcome to the AI Job Interview Evaluation System")

    if not st.session_state.authenticated:
        st.info("Please go to **Login** to continue.")
        return

    if st.session_state.authenticated and not st.session_state.get("identity_filled", False):
        st.warning("Identity not completed. Proceed to **Identity** page.")
        return

    if (
        st.session_state.authenticated
        and st.session_state.get("identity_filled", False)
        and not st.session_state.interview_done
    ):
        st.info("Proceed to **Interview** page.")
        return

    if st.session_state.interview_done:
        st.success("Interview completed! See **Result** or **Dashboard**.")


# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
