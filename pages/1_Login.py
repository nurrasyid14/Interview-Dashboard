import streamlit as st
from app.modules.auth.auth_manager import create_user, verify_user, load_user
from app.modules.utils.validators import validate_username, validate_password

st.set_page_config(page_title="Login - AI Interview", layout="centered")

# Hide sidebar
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("Login / Signup")

# Init session states
st.session_state.setdefault("auth", False)
st.session_state.setdefault("auth_user", None)

# If logged in already → go to identity
if st.session_state.auth:
    st.success(f"Logged in as {st.session_state.auth_user}")
    st.query_params.update(page="identity")
    st.rerun()


# ---------------- TAB LAYOUT ---------------- #
tab_login, tab_signup = st.tabs(["Login", "Signup"])

# ---------------- LOGIN ---------------- #
with tab_login:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if verify_user(username, password):
            st.session_state.auth = True
            st.session_state.auth_user = username
            st.session_state.user_metadata = load_user(username)

            st.success("Login successful")
            st.query_params.update(page="identity")
            st.rerun()
        else:
            st.error("Invalid username or password")


# ---------------- SIGNUP ---------------- #
with tab_signup:
    with st.form("signup_form"):
        new_username = st.text_input("Choose username")
        new_password = st.text_input("Choose password", type="password")
        full_name = st.text_input("Full name (optional)")
        register = st.form_submit_button("Create Account")

    if register:
        if not validate_username(new_username):
            st.error("Invalid username")
        elif not validate_password(new_password, new_username):
            st.error("Weak password")
        else:
            try:
                create_user(new_username, new_password, full_name=full_name)
                st.success("Account created. Please login.")
            except FileExistsError:
                st.error("Username already exists")
