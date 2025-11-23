# pages/3_Interview.py
import streamlit as st
from app.modules.QnA.questions import load_questions
from app.modules.QnA.judger import Judger

st.set_page_config(page_title="Interview - AI Interview", layout="centered")
st.title("Interview")

if not st.session_state.get("auth"):
    st.warning("Please log in first.")
    st.stop()

# Ensure session keys
if "judger" not in st.session_state or st.session_state.judger is None:
    # create judger using username
    judger = Judger(user_id=st.session_state.auth_user, company_budget=5000)
    st.session_state.judger = judger
    st.session_state.q_index = 0
    st.session_state.level = "leveling"  # start with leveling questions
    st.session_state.answers = []
    st.session_state._leveling_count = 0

questions = load_questions()
leveling = questions["leveling"]
beginner = questions["beginner"]
intermediate = questions["intermediate"]
advanced = questions["advanced"]
wage_q = questions["wage"][0]

# Handle leveling questions first (2 questions)
if st.session_state.level == "leveling":
    idx = st.session_state._leveling_count
    if idx < len(leveling):
        q = leveling[idx]
        with st.form(f"lev_{idx}"):
            answer = st.text_area(q)
            submitted = st.form_submit_button("Submit")
        if submitted:
            # store answer and process
            st.session_state.judger.process_answer(q, answer)
            st.session_state.answers.append(answer)
            st.session_state._leveling_count += 1
            st.success("Saved")
            st.experimental_rerun()
    else:
        # decide next level using months_experience from metadata
        months = int(st.session_state.user_metadata.get("months_experience", 0))
        if months < 12:
            st.session_state.level = "beginner"
        elif 12 <= months < 18:
            st.session_state.level = "intermediate"
        else:
            st.session_state.level = "advanced"
        st.experimental_rerun()
else:
    # handle main question banks
    if st.session_state.level == "beginner":
        bank = beginner
    elif st.session_state.level == "intermediate":
        bank = intermediate
    else:
        bank = advanced

    q_index = st.session_state.q_index
    if q_index < len(bank):
        q_text = bank[q_index]
        with st.form(f"q_{q_index}"):
            answer = st.text_area(f"Q{q_index+1}: {q_text}")
            submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.judger.process_answer(q_text, answer)
            st.session_state.answers.append(answer)
            st.session_state.q_index += 1
            st.success("Answer recorded.")
            st.experimental_rerun()
    else:
        st.info("All questions done. Wage expectation:")
        wage = st.number_input("Berapa ekspektasi gaji Anda? (angka)", min_value=0, step=100, format="%d")
        if st.button("Submit Wage"):
            final_report = st.session_state.judger.finalize(
                months_experience=int(st.session_state.user_metadata.get("months_experience", 0)),
                wage_expectation=int(wage),
            )
            st.session_state.final_report = final_report
            st.session_state.completed = True
            st.success("Interview finished. See result page.")
            st.experimental_set_query_params(page="result")
            st.experimental_rerun()
