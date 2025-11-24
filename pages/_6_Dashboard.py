# pages/_6_Dashboard.py
import streamlit as st
import pandas as pd
from app.modules.QnA.dashboard import DashboardBuilder

def render():
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

    if not st.session_state.get("auth"):
        st.warning("Please login first.")
        st.stop()

    user = st.session_state.get("auth_user")
    try:
        builder = DashboardBuilder(user)
        dash = builder.build()
    except Exception as e:
        st.error(f"Cannot build dashboard: {e}")
        dash = {
            "identity": user,
            "relevance_score": 0.0,
            "sentiment_score": 0.0,
            "overall_score": 0.0,
            "most_frequent_words": [],
            "most_weighted_words": [],
            "bar_chart": {"labels": [], "scores": [], "threshold": 0.8}
        }

    st.title("Dashboard")

    st.write("### Identity")
    st.write(dash.get("identity"))

    col1, col2, col3 = st.columns(3)
    col1.metric("Relevance", dash.get("relevance_score", 0.0))
    col2.metric("Sentiment", dash.get("sentiment_score", 0.0))
    col3.metric("Overall", dash.get("overall_score", 0.0))

    st.write("### Most Frequent Words")
    st.write(dash.get("most_frequent_words", []))

    st.write("### Most Weighted Words")
    st.write(dash.get("most_weighted_words", []))

    st.write("### Scores Chart")
    labels = dash.get("bar_chart", {}).get("labels", [])
    scores = dash.get("bar_chart", {}).get("scores", [])
    if labels and scores and len(labels) == len(scores):
        df = pd.DataFrame({"Label": labels, "Score": scores}).set_index("Label")
        st.bar_chart(df)
    else:
        st.info("No chart data available.")

    col1, col2 = st.columns(2)
    if col1.button("Go to Menu"):
        st.session_state["next_page"] = "menu"
        st.rerun()
    if col2.button("Logout"):
        # clear session and go to login
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.session_state["next_page"] = "login"
        st.rerun()
