# app/main.py

import streamlit as st
from app.modules.QnA.judger import Judger
from app.modules.QnA.questions import (
    beginner_questions,
    intermediate_questions,
    advanced_questions,
    wage_question,
)

st.set_page_config(page_title="AI Job Interview", layout="centered")
st.title("AI Job Interview Evaluation System")

# ----------------------------
# 1. Authentication / User Info
# ----------------------------
with st.form("auth_form"):
    name = st.text_input("Full Name")
    usn = st.text_input("USN")
    address = st.text_input("Address")
    position = st.radio(
        "Select Position",
        ["Accountant", "Chef", "Manager", "Supervisor", "Business Advisor"],
    )
    specialty = st.multiselect(
        "Select Specialty", ["Option 1", "Option 2", "Option 3"]
    )
    auth_submitted = st.form_submit_button("Start Interview")

if auth_submitted:
    if not (name and usn and address):
        st.error("Please fill all required fields!")
    else:
        pos_key = position.lower().replace(" ", "_")
        # Initialize Judger
        judger = Judger(user_id=usn, company_budget=5000)  # example budget
        st.session_state['judger'] = judger
        st.session_state['position'] = pos_key
        st.session_state['q_index'] = 0
        st.session_state['answers'] = []
        st.session_state['level'] = "beginner"
        st.success(f"Welcome {name}! Proceed to the interview questions.")

# ----------------------------
# 2. QnA Iteration
# ----------------------------
if 'judger' in st.session_state:
    judger = st.session_state['judger']
    pos_key = st.session_state['position']
    q_index = st.session_state['q_index']
    level = st.session_state['level']

    # Select question bank
    if level == "beginner":
        q_bank = beginner_questions[pos_key]
    elif level == "intermediate":
        q_bank = intermediate_questions[pos_key]
    else:
        q_bank = advanced_questions[pos_key]

    if q_index < len(q_bank):
        q_text = q_bank[q_index]
        with st.form(f"q_form_{q_index}"):
            answer = st.text_area(f"Q{q_index+1}: {q_text}")
            submitted_answer = st.form_submit_button("Submit Answer")

        if submitted_answer:
            score = judger.process_answer(q_text, answer)
            st.write(f"Score for this answer: {score}")
            st.session_state['answers'].append(answer)
            st.session_state['q_index'] += 1

    else:
        # Wage expectation question
        st.info("All questions completed! Please provide wage expectation.")
        wage = st.number_input(
            wage_question, min_value=0, step=100, format="%d"
        )
        submit_wage = st.button("Submit Wage")
        if submit_wage:
            # Assuming months_experience = 12 (can be modified to ask user)
            final_report = judger.finalize(months_experience=12, wage_expectation=wage)
            st.success("Interview Completed! Here is your final report:")
            st.json(final_report)
