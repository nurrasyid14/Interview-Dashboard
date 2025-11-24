# pages/_2_Identity.py
import streamlit as st
from app.modules.auth.auth_manager import load_user, update_user
from app.modules.utils.validators import validate_age

def render():
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

    if not st.session_state.auth:
        st.warning("Please login first.")
        st.stop()

    username = st.session_state.auth_user
    user_meta = st.session_state.user_metadata

    with st.form("identity_form"):
        full_name = st.text_input("Full Name", value=user_meta.get("FullName", ""))
        birthdate = st.text_input("Birthdate (dd-mm-yyyy)", value=user_meta.get("Tanggal_Lahir", ""))
        months_experience = st.number_input("Months of experience", min_value=0, value=int(user_meta.get("months_experience", 0)))
        address = st.text_input("Address", value=user_meta.get("Address", ""))
        position = st.selectbox("Position", ["Accountant", "Chef", "Manager", "Supervisor", "Business Advisor"])
        specialties = st.multiselect("Specialties", ["Option 1", "Option 2", "Option 3"], default=user_meta.get("Specialties", []))
        submitted = st.form_submit_button("Save & Continue")

    if submitted:
        if birthdate and not validate_age(birthdate):
            st.error("Invalid or underage")
        else:
            updates = {
                "FullName": full_name,
                "Tanggal_Lahir": birthdate,
                "months_experience": int(months_experience),
                "Address": address,
                "Position": position,
                "Specialties": specialties,
                "identity_filled": True
            }
            update_user(username, updates)
            st.session_state.user_metadata = load_user(username)
            st.session_state.identity_filled = True
            st.success("Profile saved.")
            st.query_params(page="menu")
            st.rerun()
