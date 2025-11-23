import streamlit as st
import pandas as pd
from app.modules.QnA.dashboard import DashboardBuilder

st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

st.set_page_config(page_title="Dashboard")

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

st.write("### Final Score Chart")
df = pd.DataFrame({
    "Label": dash["bar_chart"]["labels"],
    "Score": dash["bar_chart"]["scores"]
}).set_index("Label")

st.bar_chart(df)

if st.button("Logout"):
    st.session_state.clear()
    st.rerun()
