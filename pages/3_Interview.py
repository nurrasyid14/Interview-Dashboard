import streamlit as st
from app.modules.QnA.questions import load_questions
from app.modules.QnA.judger import Judger

st.set_page_config(page_title="Interview", layout="centered")

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

if "judger" not in st.session_state:
    st.session_state.judger = Judger(
        user_id=st.session_state.auth_user,
        company_budget=5000
    )
    st.session_state.q_index = 0
    st.session_state.level = "leveling"
    st.session_state.answers = []
    st.session_state._leveling_count = 0

questions = load_questions()

# LEVELING QUESTIONS (2 Q)
if st.session_state.level == "leveling":
    idx = st.session_state._leveling_count

    if idx < len(questions["leveling"]):
        q = questions["leveling"][idx]

        with st.form(f"lev_{idx}"):
            ans = st.text_area(q)
            sub = st.form_submit_button("Submit")

        if sub:
            st.session_state.judger.process_answer(q, ans)
            st.session_state.answers.append(ans)
            st.session_state._leveling_count += 1
            st.rerun()

    else:
        months = int(st.session_state.user_metadata.get("months_experience", 0))

        if months < 12: st.session_state.level = "beginner"
        elif months < 18: st.session_state.level = "intermediate"
        else: st.session_state.level = "advanced"

        st.rerun()

# MAIN QUESTIONS
else:
    level = st.session_state.level
    bank = questions[level]

    q_idx = st.session_state.q_index

    if q_idx < len(bank):
        q = bank[q_idx]
        with st.form(f"q_{q_idx}"):
            a = st.text_area(f"Q{q_idx+1}: {q}")
            sub = st.form_submit_button("Submit")

        if sub:
            st.session_state.judger.process_answer(q, a)
            st.session_state.answers.append(a)
            st.session_state.q_index += 1
            st.rerun()

    else:
        st.info("All questions done.")
        wage = st.number_input("Wage expectation", min_value=0, step=100)

        if st.button("Submit Wage"):
            report = st.session_state.judger.finalize(
                months_experience=int(st.session_state.user_metadata.get("months_experience", 0)),
                wage_expectation=int(wage),
            )
            st.session_state.final_report = report
            st.session_state.completed = True

            st.query_params.update(page="result")
            st.rerun()
