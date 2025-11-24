# main.py
import streamlit as st
from pages import render_page

# -----------------------------------
# Session State Initialization
# -----------------------------------
DEFAULT_SESSION_KEYS = {
    "auth": False,
    "auth_user": None,
    "user_metadata": {},
    "identity_filled": False,
}

for key, default in DEFAULT_SESSION_KEYS.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -----------------------------------
# Optional styling loader
# -----------------------------------
try:
    from app.modules.frontend_loader import load_css, load_js
    load_css()
    load_js()
except Exception:
    pass  # Do not crash if frontend loader missing

# -----------------------------------
# Routing Logic
# -----------------------------------
current_page = None

if not st.session_state.auth:
    current_page = "login"

elif st.session_state.auth and not st.session_state.identity_filled:
    current_page = "identity"

else:
    current_page = "menu"

# Render selected page
render_page(current_page)
