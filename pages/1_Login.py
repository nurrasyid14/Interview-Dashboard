# pages/1_Login.py
import streamlit as st
from app.modules.auth.auth_manager import create_user, verify_user, load_user
from app.modules.utils.validators import validate_username, validate_password

st.set_page_config(page_title="Auth - AI Interview", layout="centered")
st.title("Login / Signup")

if "auth" not in st.session_state:
    st.session_state.auth = False
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None
if "judger" not in st.session_state:
    st.session_state.judger = None

def logout_clear():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.experimental_rerun()

# show logout if logged in
if st.session_state.get("auth"):
    st.info(f"Already logged in as {st.session_state.auth_user}")
    if st.button("Logout"):
        logout_clear()

tab = st.tabs(["Login", "Signup"])[0]

with st.form("login_form"):
    username = st.text_input("Username (lowercase)")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    if not username or not password:
        st.error("Fill both fields")
    else:
        if verify_user(username, password):
            st.success("Login successful")
            st.session_state.auth = True
            st.session_state.auth_user = username
            # load metadata into session
            st.session_state.user_metadata = load_user(username)
            # move to identity page
            st.experimental_set_query_params(page="identity")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

with st.form("signup_form"):
    new_username = st.text_input("Choose username (lowercase)", key="su_username")
    new_password = st.text_input("Choose password", type="password", key="su_password")
    full_name = st.text_input("Full name (optional)", key="su_name")
    signup = st.form_submit_button("Create account")

if signup:
    if not (new_username and new_password):
        st.error("Please fill username and password")
    elif not validate_username(new_username):
        st.error("Username invalid. Lowercase letters, digits, dot or underscore, must contain a letter.")
    elif not validate_password(new_password, new_username):
        st.error("Password does not meet complexity requirements.")
    else:
        try:
            create_user(new_username, new_password, full_name=full_name)
            st.success("Account created. Please log in.")
        except FileExistsError:
            st.error("Username already exists.")
