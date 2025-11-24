import streamlit as st
from app.modules.frontend_loader import load_css, load_js

# Load CSS/JS globally
load_css()
load_js()

# Hide sidebar
st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

# -------------------------
# Initialize session state
# -------------------------
session_keys = [
    "auth", "auth_user", "user_metadata", "identity_filled",
    "interview_started", "interview_done", "completed", "final_report",
    "judger", "level", "q_index", "answers", "_leveling_count"
]

for key in session_keys:
    if key not in st.session_state:
        if key in ["auth", "identity_filled", "interview_started", "interview_done", "completed"]:
            st.session_state[key] = False
        elif key == "answers":
            st.session_state[key] = []
        else:
            st.session_state[key] = None

# -------------------------
# Logout handler
# -------------------------
if st.session_state.get("auth") and st.query_params.get("logout") == ["1"]:
    st.session_state.clear()
    st.rerun()

# -------------------------
# Determine current page
# -------------------------
current_page = st.query_params.get("page", ["login"])[0]

# -------------------------
# Routing logic
# -------------------------
if not st.session_state.auth:
    from pages import _1_Login as login_page
    login_page.render()
elif st.session_state.auth and not st.session_state.identity_filled:
    from pages import _2_Identity as identity_page
    identity_page.render()
else:
    if current_page == "menu":
        from pages import _3_Menu as menu_page
        menu_page.render()
    elif current_page == "interview":
        from pages import _4_Interview as interview_page
        interview_page.render()
    elif current_page == "result":
        from pages import _5_Result as result_page
        result_page.render()
    elif current_page == "dashboard":
        from pages import _6_Dashboard as dashboard_page
        dashboard_page.render()
    else:
        # Default redirect to menu
        st.experimental_set_query_params(page="menu")  # this is still supported as of now
        st.rerun()
