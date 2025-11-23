# main.py
import streamlit as st

st.set_page_config(
    page_title="AI Job Interview System",
    layout="centered",
)

# ----------------------------------------------------------------------
# Initialize session state
# ----------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = {}

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "interview_done" not in st.session_state:
    st.session_state.interview_done = False

if "judger" not in st.session_state:
    st.session_state.judger = None


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
