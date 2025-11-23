# pages/5_Dashboard.py
import streamlit as st
from app.modules.QnA.dashboard import DashboardBuilder
import pandas as pd

st.set_page_config(page_title="Dashboard - AI Interview", layout="centered")
st.title("Dashboard")

if not st.session_state.get("auth"):
    st.warning("Please log in first.")
    st.stop()

user_id = st.session_state.auth_user
builder = DashboardBuilder(user_id)
dashboard = builder.build()

st.subheader("Identity")
st.write(dashboard.get("identity"))

col1, col2, col3 = st.columns(3)
col1.metric("Relevance", dashboard["relevance_score"])
col2.metric("Sentiment", dashboard["sentiment_score"])
col3.metric("Overall", dashboard["overall_score"])

st.write("### Most Frequent Words")
st.write(dashboard["most_frequent_words"])

st.write("### Most Weighted Words")
st.write(dashboard["most_weighted_words"])

st.write("### Scores Bar Chart")
bar = dashboard["bar_chart"]
# Build dataframe for bar chart labels vs scores
df = pd.DataFrame({"label": bar["labels"], "score": bar["scores"]})
st.bar_chart(df.rename(columns={"label": "index"}).set_index("index"))
