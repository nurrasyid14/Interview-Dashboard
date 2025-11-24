import streamlit as st

def render():
    st.markdown('<style> section[data-testid="stSidebar"]{display:none;} </style>', unsafe_allow_html=True)

    if not st.session_state.get("auth"):
        st.warning("Please login first.")
        st.session_state["next_page"] = "login"
        st.rerun()

    if not st.session_state.get("identity_filled"):
        st.warning("Please complete your profile first.")
        st.session_state["next_page"] = "identity"
        st.rerun()

    st.title(f"Welcome, {st.session_state.get('auth_user')}!")
    st.info("Select an option below:")

    col1, col2, col3 = st.columns(3)

    if col1.button("Start Interview", use_container_width=True):
        st.session_state["next_page"] = "interview"
        st.rerun()

    dashboard_disabled = not st.session_state.get("interview_done", False)
    if col2.button(
        "View Dashboard", 
        use_container_width=True, 
        disabled=dashboard_disabled,
        help="Complete the interview first to view dashboard"
    ):
        st.session_state["next_page"] = "dashboard"
        st.rerun()

    if col3.button("🚪 Logout", use_container_width=True):
        # Clear all session state
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.session_state["next_page"] = "login"
        st.rerun()

    st.markdown("---")
    st.subheader("Your Status")
    
    interview_status = "✅ Completed" if st.session_state.get("interview_done") else "❌ Not Started"
    st.write(f"**Interview Status:** {interview_status}")
    
    if st.session_state.get("interview_done"):
        st.success("You can now view your dashboard!")
