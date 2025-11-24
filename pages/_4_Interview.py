import streamlit as st
from app.modules.QnA.questions import load_questions
from app.modules.QnA.judger import Judger

def render():
    st.markdown('<style> section[data-testid="stSidebar"]{display:none;} </style>', unsafe_allow_html=True)
    
    if not st.session_state.get("auth"):
        st.warning("Please login first.")
        st.session_state["next_page"] = "login"
        st.rerun()
    
    if not st.session_state.get("identity_filled"):
        st.warning("Please complete your identity first.")
        st.session_state["next_page"] = "identity"
        st.rerun()
    
    if st.session_state.get("interview_done"):
        st.info("You have already completed the interview. Redirecting to menu...")
        st.session_state["next_page"] = "menu"
        st.rerun()
    
    st.title("📝 Interview Session")
    
    if "judger" not in st.session_state or st.session_state.judger is None:
        st.session_state.judger = Judger(
            user_id=st.session_state.get("auth_user"),
            company_budget=5000
        )
        st.session_state.interview_stage = "leveling"
        st.session_state.current_question_index = 0
        st.session_state.all_answers = []
        st.session_state.determined_level = None
    
    # Load all questions
    questions = load_questions()
    leveling = questions.get("leveling", [])
    beginner = questions.get("beginner", [])
    intermediate = questions.get("intermediate", [])
    advanced = questions.get("advanced", [])
    
    if st.session_state.interview_stage == "leveling":
        idx = st.session_state.current_question_index
        total_leveling = len(leveling)
        
        if idx < total_leveling:
            st.info(f"**Level Determination** - Question {idx + 1} of {total_leveling}")
            st.progress((idx + 1) / total_leveling)
            
            question_text = leveling[idx]
            st.markdown(f"### {question_text}")
            
            with st.form(key=f"leveling_form_{idx}"):
                answer = st.text_area(
                    "Your answer:",
                    height=150,
                    key=f"leveling_answer_{idx}",
                    placeholder="Type your answer here..."
                )
                submitted = st.form_submit_button("Submit Answer", use_container_width=True)
                
                if submitted:
                    if not answer.strip():
                        st.error("❌ Please provide an answer before submitting.")
                    else:
                        try:
                            st.session_state.judger.process_answer(question_text, answer)
                            st.session_state.all_answers.append(answer)
                            st.session_state.current_question_index += 1
                            st.success("✅ Answer recorded!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error processing answer: {e}")
        else:
            months = int(st.session_state.get("user_metadata", {}).get("months_experience", 0))
            if months < 12:
                st.session_state.determined_level = "beginner"
            elif 12 <= months < 18:
                st.session_state.determined_level = "intermediate"
            else:
                st.session_state.determined_level = "advanced"
            
            st.session_state.interview_stage = "main_questions"
            st.session_state.current_question_index = 0
            st.rerun()
    
    elif st.session_state.interview_stage == "main_questions":
        question_bank = {
            "beginner": beginner,
            "intermediate": intermediate,
            "advanced": advanced
        }.get(st.session_state.determined_level, beginner)
        
        idx = st.session_state.current_question_index
        total_questions = len(question_bank)
        
        if idx < total_questions:
            st.info(f"**{st.session_state.determined_level.title()} Level** - Question {idx + 1} of {total_questions}")
            st.progress((idx + 1) / total_questions)
            
            question_text = question_bank[idx]
            st.markdown(f"### Q{idx + 1}: {question_text}")
            
            with st.form(key=f"main_form_{idx}"):
                answer = st.text_area(
                    "Your answer:",
                    height=150,
                    key=f"main_answer_{idx}",
                    placeholder="Type your answer here..."
                )
                submitted = st.form_submit_button("Submit Answer", use_container_width=True)
                
                if submitted:
                    if not answer.strip():
                        st.error("❌ Please provide an answer before submitting.")
                    else:
                        try:
                            st.session_state.judger.process_answer(question_text, answer)
                            st.session_state.all_answers.append(answer)
                            st.session_state.current_question_index += 1
                            st.success("✅ Answer recorded!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error processing answer: {e}")
        else:
            st.session_state.interview_stage = "wage"
            st.rerun()
    
    elif st.session_state.interview_stage == "wage":
        st.success("🎉 You've completed all interview questions!")
        st.markdown("### Final Step: Salary Expectation")
        
        with st.form(key="wage_form"):
            wage = st.number_input(
                "Berapa ekspektasi gaji Anda per bulan? (dalam Rupiah)",
                min_value=0,
                step=100000,
                format="%d",
                help="Masukkan angka ekspektasi gaji bulanan Anda"
            )
            submitted = st.form_submit_button("Submit & Complete Interview", use_container_width=True)
            
            if submitted:
                if wage <= 0:
                    st.error("❌ Please enter a valid salary expectation.")
                else:
                    try:
                        final_report = st.session_state.judger.finalize(
                            months_experience=int(st.session_state.user_metadata.get("months_experience", 0)),
                            wage_expectation=int(wage)
                        )
                        
                        st.session_state.final_report = final_report
                        st.session_state.interview_done = True
                        st.session_state.completed = True
                        st.session_state.interview_stage = "completed"
                        
                        st.success("✅ Interview completed successfully!")
                        st.balloons()
                        
                        st.session_state["next_page"] = "results"
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error finalizing interview: {e}")
                        import traceback
                        st.code(traceback.format_exc())

render()
