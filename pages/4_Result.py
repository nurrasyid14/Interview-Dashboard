import streamlit as st

st.set_page_config(page_title="Result")

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

if not st.session_state.get("completed"):
    st.info("Interview not finished.")
    st.query_params.update(page="interview")
    st.rerun()

final = st.session_state.final_report

st.title("Final Interview Result")
st.json(final)

if final.get("label") == "Layak":
    st.success("Accepted")
elif final.get("label") == "Dipertimbangkan":
    st.warning("To be considered")
else:
    st.error("Rejected")

if st.button("Go to Dashboard"):
    st.query_params.update(page="dashboard")
    st.rerun()

if st.button("Logout"):
    st.session_state.clear()
    st.rerun()
