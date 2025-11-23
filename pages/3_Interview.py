# pages/3_Interview.py
import streamlit as st
from app.modules.QnA.questions import load_questions
from app.modules.QnA.judger import Judger

st.set_page_config(page_title="Interview - AI Interview", layout="centered")
st.title("Interview")

if not st.session_state.get("auth"):
    st.warning("Please log in first.")
    st.stop()

if st.session_state.judger is None:
    judger = Judger(user_id=st.session_state.auth_user, company_budget=5000)
    st.session_state.judger = judger
    st.session_state.level = "leveling"
    st.session_state.q_index = 0
    st.session_state.answers = []
    st.session_state._leveling_count = 0

# Load all question banks
try:
    questions = load_questions()
except Exception as e:
    st.error(f"Error loading questions: {e}")
    st.stop()

leveling = questions.get("leveling", [])
beginner = questions.get("beginner", [])
intermediate = questions.get("intermediate", [])
advanced = questions.get("advanced", [])
wage_q = questions.get("wage", [{}])[0]

# Handle leveling questions first (2 questions)
if st.session_state.level == "leveling":
    idx = st.session_state.get("_leveling_count", 0)
    if idx < len(leveling):
        q = leveling[idx]
        with st.form(f"lev_{idx}"):
            answer = st.text_area(q)
            submitted = st.form_submit_button("Submit")
        if submitted:
            if not answer.strip():
                st.error("Please provide an answer")
            else:
                try:
                    st.session_state.judger.process_answer(q, answer)
                    st.session_state.answers.append(answer)
                    st.session_state._leveling_count = idx + 1
                    st.success("Saved")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing answer: {e}")
    else:
        # Decide next level using months_experience from metadata
        months = int(st.session_state.user_metadata.get("months_experience", 0))
        if months < 12:
            st.session_state.level = "beginner"
        elif 12 <= months < 18:
            st.session_state.level = "intermediate"
        else:
            st.session_state.level = "advanced"
        st.rerun()
else:
    # Handle main question banks
    if st.session_state.level == "beginner":
        bank = beginner
    elif st.session_state.level == "intermediate":
        bank = intermediate
    else:
        bank = advanced

    q_index = st.session_state.get("q_index", 0)
    if q_index < len(bank):
        q_text = bank[q_index]
        with st.form(f"q_{q_index}"):
            answer = st.text_area(f"Q{q_index+1}: {q_text}")
            submitted = st.form_submit_button("Submit")
        if submitted:
            if not answer.strip():
                st.error("Please provide an answer")
            else:
                try:
                    st.session_state.judger.process_answer(q_text, answer)
                    st.session_state.answers.append(answer)
                    st.session_state.q_index = q_index + 1
                    st.success("Answer recorded.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing answer: {e}")
    else:
        st.info("All questions done. Wage expectation:")
        wage = st.number_input("Berapa ekspektasi gaji Anda? (angka)", min_value=0, step=100, format="%d")
        if st.button("Submit Wage"):
            try:
                final_report = st.session_state.judger.finalize(
                    months_experience=int(st.session_state.user_metadata.get("months_experience", 0)),
                    wage_expectation=int(wage),
                )
                st.session_state.final_report = final_report
                st.session_state.completed = True
                st.success("Interview finished. See result page.")
                st.query_params["page"] = "result"
                st.rerun()
            except Exception as e:
                st.error(f"Error finalizing interview: {e}")
