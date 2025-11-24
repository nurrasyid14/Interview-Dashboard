# main.py
import streamlit as st

# Optional: load CSS/JS (guard errors)
try:
    from app.modules.frontend_loader import load_css, load_js
    load_css()
    load_js()
except Exception:
    pass

# -------------------------
# Initialize session state defaults
# -------------------------
DEFAULT_KEYS = {
    "auth": False,
    "auth_user": None,
    "user_metadata": {},
    "identity_filled": False,
    "interview_started": False,
    "interview_done": False,
    "completed": False,
    "final_report": None,
    "judger": None,
    "level": None,
    "q_index": 0,
    "answers": [],
    "_leveling_count": 0,
    # next_page: optional transient navigation signal
}

for k, default in DEFAULT_KEYS.items():
    if k not in st.session_state:
        st.session_state[k] = default

# optional: hide Streamlit default sidebar
st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

# -------------------------
# Navigation: session-driven
# -------------------------
# If a page explicitly requested navigation, consume it first
next_page = st.session_state.pop("next_page", None)

if next_page:
    current_page = next_page
else:
    # Allow external read-only query param to suggest a page, but do not rely on it for flow
    query_page = st.query_params.get("page", None)
    if query_page:
        query_page = query_page[0]  # first value only

    if not st.session_state.auth:
        current_page = "login"
    elif st.session_state.auth and not st.session_state.identity_filled:
        current_page = "identity"
    else:
        # Authenticated and identity filled: choose
        if query_page in {"menu", "interview", "results", "dashboard"}:
            current_page = query_page
        else:
            current_page = "menu"

# -------------------------
# Lazy import & render
# -------------------------
if current_page == "login":
    import pages._1_Login as login_page
    login_page.render()
elif current_page == "identity":
    import pages._2_Identity as identity_page
    identity_page.render()
elif current_page == "menu":
    import pages._3_Menu as menu_page
    menu_page.render()
elif current_page == "interview":
    import pages._4_Interview as interview_page
    interview_page.render()
elif current_page == "results":
    import pages._5_Result as result_page
    result_page.render()
elif current_page == "dashboard":
    import pages._6_Dashboard as dashboard_page
    dashboard_page.render()
else:
    # Fallback to menu
    import pages._3_Menu as menu_page 
    menu_page.render()
