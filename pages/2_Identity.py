import streamlit as st
from app.modules.auth.auth_manager import load_user, update_user
from app.modules.utils.validators import validate_age

st.set_page_config(page_title="Identity - AI Interview", layout="centered")

# Hide sidebar
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

if not st.session_state.get("auth"):
    st.warning("Please login first.")
    st.query_params.update(page="login")
    st.rerun()

username = st.session_state.auth_user
user_meta = st.session_state.get("user_metadata", load_user(username))

st.title("Identity & Specialties")

with st.form("identity_form"):
    full_name = st.text_input("Full Name", value=user_meta.get("FullName", ""))
    birthdate = st.text_input("Birthdate (dd-mm-yyyy)", value=user_meta.get("Tanggal_Lahir", ""))
    months = st.number_input("Months of experience", min_value=0, value=int(user_meta.get("months_experience", 0)))
    address = st.text_input("Address", value=user_meta.get("Address", ""))

    position = st.selectbox("Position", [
        "Accountant", "Chef", "Manager", "Supervisor", "Business Advisor"
    ], index=0)

    specialties = st.multiselect(
        "Specialties", ["Option 1", "Option 2", "Option 3"],
        default=user_meta.get("Specialties", [])
    )

    submit = st.form_submit_button("Save & Continue")

if submit:
    if birthdate and not validate_age(birthdate):
        st.error("Invalid birthdate or under 18.")
    else:
        update_user(username, {
            "FullName": full_name,
            "Tanggal_Lahir": birthdate,
            "months_experience": int(months),
            "Address": address,
            "Position": position,
            "Specialties": specialties,
        })

        st.session_state.user_metadata = load_user(username)
        st.success("Saved.")

        st.query_params.update(page="interview")
        st.rerun()
