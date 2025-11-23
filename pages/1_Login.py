import streamlit as st
from app.modules.auth.auth_manager import create_user, verify_user, load_user
from app.modules.utils.validators import validate_username, validate_password
from app.modules.frontend_loader import render_template

st.set_page_config(page_title="Login", layout="centered")

# Hide sidebar
st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

render_template("login.html", height=250)

if "auth" not in st.session_state:
    st.session_state.auth = False
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

def logout_clear():
    st.session_state.clear()
    st.rerun()

tabs = st.tabs(["Login", "Signup"])

with tabs[0]:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if verify_user(username, password):
            st.session_state.auth = True
            st.session_state.auth_user = username
            st.session_state.user_metadata = load_user(username)
            st.query_params["page"] = "identity"
            st.rerun()
        else:
            st.error("Invalid credentials")

with tabs[1]:
    with st.form("signup_form"):
        new_username = st.text_input("Choose username", key="su_username")
        new_password = st.text_input("Choose password", type="password", key="su_password")
        full_name = st.text_input("Full Name", key="su_name")
        signup = st.form_submit_button("Signup")

    if signup:
        if not (new_username and new_password):
            st.error("Fill both fields")
        elif not validate_username(new_username):
            st.error("Invalid username")
        elif not validate_password(new_password, new_username):
            st.error("Password too weak")
        else:
            try:
                create_user(new_username, new_password, full_name=full_name)
                st.success("Account created. Please login.")
            except FileExistsError:
                st.error("Username exists")
