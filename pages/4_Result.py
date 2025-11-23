# pages/4_Result.py
import streamlit as st

st.set_page_config(page_title="Result - AI Interview", layout="centered")
st.title("Interview Result")

if not st.session_state.get("auth"):
    st.warning("Please log in first.")
    st.stop()

if not st.session_state.get("completed", False):
    st.info("Interview not completed yet.")
    st.stop()

final_report = st.session_state.get("final_report", {})
st.subheader("Final Report")
st.json(final_report)

label = final_report.get("label", "Unknown")
if label == "Layak":
    st.success("Candidate accepted (Layak).")
elif label == "Dipertimbangkan":
    st.warning("Candidate to be considered.")
else:
    st.error("Candidate not accepted.")

if st.button("Go to Dashboard"):
    st.experimental_set_query_params(page="dashboard")
    st.experimental_rerun()

if st.button("Logout"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.experimental_rerun()
