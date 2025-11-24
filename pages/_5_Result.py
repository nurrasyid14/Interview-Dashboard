# pages/_5_Result.py
import streamlit as st

def render():
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

    if not st.session_state.auth:
        st.warning("Please login first.")
        st.stop()

    if not st.session_state.completed or not st.session_state.final_report:
        st.info("Interview not completed yet.")
        st.stop()

    final_report = st.session_state.final_report

    st.title("Interview Result")
    st.subheader("Final Report")
    st.json(final_report)

    label = final_report.get("label", "Unknown")
    if label == "Layak":
        st.success("Candidate accepted (Layak).")
    elif label == "Dipertimbangkan":
        st.warning("Candidate to be considered")
    else:
        st.error("Candidate not accepted")

    col1, col2 = st.columns(2)
    if col1.button("Go to Menu"):
        st.query_params(page="menu")
        st.rerun()
    if col2.button("Logout"):
        st.session_state.clear()
        st.rerun()
