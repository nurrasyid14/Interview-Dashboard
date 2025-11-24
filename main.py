# main.py
import streamlit as st
from app.modules.frontend_loader import load_css, load_js
# main.py
if not st.session_state.auth:
    import pages._1_Login as login_page
    login_page.render()

elif st.session_state.auth and not st.session_state.identity_filled:
    import pages._2_Identity as identity_page
    identity_page.render()

else:
    import pages._3_Menu as menu_page
    menu_page.render()


# -------------------------
# Load frontend assets
# -------------------------
load_css()
load_js()

# Hide default Streamlit sidebar
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
query_params = st.query_params  # stable API
if st.session_state.get("auth") and query_params.get("logout") == ["1"]:
    st.session_state.clear()
    st.rerun()

# -------------------------
# Determine current page
# -------------------------
current_page = query_params.get("page", ["login"])[0]

# -------------------------
# Routing logic
# -------------------------
if not st.session_state.auth:
    render_page("login")
elif st.session_state.auth and not st.session_state.identity_filled:
    render_page("identity")
else:
    if current_page in ["menu", "interview", "result", "dashboard"]:
        render_page(current_page)
    else:
        # Default to menu
        st.query_params = {"page": "menu"}  # stable API
        st.rerun()
