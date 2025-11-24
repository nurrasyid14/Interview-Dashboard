# pages/_6_Dashboard.py
import streamlit as st
import pandas as pd
from app.modules.QnA.dashboard import DashboardBuilder

def render():
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

    if not st.session_state.auth:
        st.warning("Please login first.")
        st.stop()

    user = st.session_state.auth_user
    builder = DashboardBuilder(user)
    dash = builder.build()

    st.title("Dashboard")

    st.write("### Identity")
    st.write(dash["identity"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Relevance", dash["relevance_score"])
    col2.metric("Sentiment", dash["sentiment_score"])
    col3.metric("Overall", dash["overall_score"])

    st.write("### Most Frequent Words")
    st.write(dash["most_frequent_words"])

    st.write("### Most Weighted Words")
    st.write(dash["most_weighted_words"])

    st.write("### Scores Chart")
    df = pd.DataFrame({
        "Label": dash["bar_chart"]["labels"],
        "Score": dash["bar_chart"]["scores"]
    }).set_index("Label")
    st.bar_chart(df)

    col1, col2 = st.columns(2)
    if col1.button("Go to Menu"):
        st.query_params(page="menu")
        st.rerun()
    if col2.button("Logout"):
        st.session_state.clear()
        st.rerun()
