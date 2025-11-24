# pages/_4_Interview.py
import streamlit as st
from app.modules.QnA.questions import load_questions
from app.modules.QnA.judger import Judger

def render():
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

    if not st.session_state.get("auth"):
        st.warning("Please login first.")
        st.stop()

    # Initialize judger lazily in session
    if st.session_state.get("judger") is None:
        # company budget example: 5000
        st.session_state.judger = Judger(user_id=st.session_state.get("auth_user"), company_budget=5000)
        st.session_state.level = "leveling"
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.session_state._leveling_count = 0

    # load question banks
    questions = load_questions()
    leveling = questions.get("leveling", [])
    beginner = questions.get("beginner", [])
    intermediate = questions.get("intermediate", [])
    advanced = questions.get("advanced", [])

    # Leveling stage
    if st.session_state.get("level") == "leveling":
        idx = st.session_state.get("_leveling_count", 0)
        if idx < len(leveling):
            q = leveling[idx]
            with st.form(f"lev_{idx}"):
                answer = st.text_area(q)
                submitted = st.form_submit_button("Submit")
            if submitted:
                if not answer.strip():
                    st.error("Please answer the question.")
                else:
                    # process answer
                    try:
                        st.session_state.judger.process_answer(q, answer)
                    except Exception as e:
                        st.error(f"Error processing answer: {e}")
                    st.session_state.answers.append(answer)
                    st.session_state._leveling_count = idx + 1
                    st.success("Saved")
                    st.rerun()
        else:
            # determine level based on months_experience
            months = int(st.session_state.get("user_metadata", {}).get("months_experience", 0))
            if months < 12:
                st.session_state.level = "beginner"
            elif 12 <= months < 18:
                st.session_state.level = "intermediate"
            else:
                st.session_state.level = "advanced"
            st.rerun()
        return

    # Main question bank stage
    bank = {
        "beginner": beginner,
        "intermediate": intermediate,
        "advanced": advanced
    }.get(st.session_state.get("level", "beginner"), beginner)

    idx = st.session_state.get("q_index", 0)
    if idx < len(bank):
        q_text = bank[idx]
        with st.form(f"q_{idx}"):
            answer = st.text_area(f"Q{idx+1}: {q_text}")
            submitted = st.form_submit_button("Submit")
        if submitted:
            if not answer.strip():
                st.error("Please provide an answer")
            else:
                try:
                    st.session_state.judger.process_answer(q_text, answer)
                except Exception as e:
                    st.error(f"Error processing answer: {e}")
                st.session_state.answers.append(answer)
                st.session_state.q_index = idx + 1
                st.success("Answer recorded")
                st.rerun()
        return

    # After questions done, ask for wage
    wage = st.number_input("Ekspektasi gaji (angka)", min_value=0, step=100)
    if st.button("Submit Wage"):
        try:
            final_report = st.session_state.judger.finalize(
                months_experience=int(st.session_state.user_metadata.get("months_experience", 0)),
                wage_expectation=int(wage)
            )
            st.session_state.final_report = final_report
            st.session_state.completed = True
            st.session_state.interview_done = True
            st.success("Interview completed!")
            # navigate to results
            st.session_state["next_page"] = "results"
            st.rerun()
        except Exception as e:
            st.error(f"Error finalizing interview: {e}")
