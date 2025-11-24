# pages/_4_Interview.py
import streamlit as st
from app.modules.QnA.questions import load_questions
from app.modules.QnA.judger import Judger

def render():
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

    if not st.session_state.auth:
        st.warning("Please login first.")
        st.stop()

    if st.session_state.judger is None:
        st.session_state.judger = Judger(user_id=st.session_state.auth_user, company_budget=5000)
        st.session_state.level = "leveling"
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.session_state._leveling_count = 0

    questions = load_questions()
    leveling = questions.get("leveling", [])
    beginner = questions.get("beginner", [])
    intermediate = questions.get("intermediate", [])
    advanced = questions.get("advanced", [])

    # LEVELING
    if st.session_state.level == "leveling":
        idx = st.session_state._leveling_count
        if idx < len(leveling):
            q = leveling[idx]
            with st.form(f"lev_{idx}"):
                answer = st.text_area(q)
                submitted = st.form_submit_button("Submit")
            if submitted:
                if not answer.strip():
                    st.error("Please answer the question.")
                else:
                    st.session_state.judger.process_answer(q, answer)
                    st.session_state.answers.append(answer)
                    st.session_state._leveling_count += 1
                    st.success("Saved")
                    st.rerun()
        else:
            months = int(st.session_state.user_metadata.get("months_experience", 0))
            if months < 12:
                st.session_state.level = "beginner"
            elif 12 <= months < 18:
                st.session_state.level = "intermediate"
            else:
                st.session_state.level = "advanced"
            st.rerun()
    else:
        bank = {"beginner": beginner, "intermediate": intermediate, "advanced": advanced}[st.session_state.level]
        idx = st.session_state.q_index
        if idx < len(bank):
            q_text = bank[idx]
            with st.form(f"q_{idx}"):
                answer = st.text_area(f"Q{idx+1}: {q_text}")
                submitted = st.form_submit_button("Submit")
            if submitted:
                if not answer.strip():
                    st.error("Please provide an answer")
                else:
                    st.session_state.judger.process_answer(q_text, answer)
                    st.session_state.answers.append(answer)
                    st.session_state.q_index += 1
                    st.success("Answer recorded")
                    st.rerun()
        else:
            wage = st.number_input("Ekspektasi gaji (angka)", min_value=0, step=100)
            if st.button("Submit Wage"):
                final_report = st.session_state.judger.finalize(
                    months_experience=int(st.session_state.user_metadata.get("months_experience", 0)),
                    wage_expectation=int(wage)
                )
                st.session_state.final_report = final_report
                st.session_state.completed = True
                st.session_state.interview_done = True
                st.success("Interview completed!")
                st.query_params(page="result")
                st.rerun()
