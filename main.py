import streamlit as st
import pandas as pd
import os
import json
import time
import plotly.express as px
import plotly.graph_objects as go

# Import custom modules
# Ensure you have empty __init__.py files in app/ and app/modules/
from app.modules import nlp_engine, question_bank

# --- CONFIG & SETUP ---
st.set_page_config(page_title="Hire-ON!", layout="wide")

USER_DB_PATH = "app/data/users"
JOB_DB_PATH = "app/data/jobs.csv"
REPORT_PATH = "app/reports"

# Ensure directories exist
os.makedirs(USER_DB_PATH, exist_ok=True)
os.makedirs(REPORT_PATH, exist_ok=True)

# --- SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'identity_filled' not in st.session_state:
    st.session_state.identity_filled = False
if 'interview_status' not in st.session_state:
    st.session_state.interview_status = False
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'interview_answers' not in st.session_state:
    st.session_state.interview_answers = [] # Stores dicts: {question, answer, grade, sentiment, relevance}
if 'determined_level' not in st.session_state:
    st.session_state.determined_level = None
if 'wage_question_shown' not in st.session_state:
    st.session_state.wage_question_shown = False

# --- HELPER FUNCTIONS ---

def load_jobs():
    # Create dummy if not exists
    if not os.path.exists(JOB_DB_PATH):
        df = pd.DataFrame({
            "position": ["Chef", "OB", "Business Advisor", "Accountant", "General Manager"],
            "affordable_wage": [5000000, 3000000, 8000000, 7000000, 15000000]
        })
        df.to_csv(JOB_DB_PATH, index=False)
    return pd.read_csv(JOB_DB_PATH)

def save_user_data(username, data):
    with open(f"{USER_DB_PATH}/{username}.json", "w") as f:
        json.dump(data, f)

def load_user_data(username):
    path = f"{USER_DB_PATH}/{username}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def determine_level(years_exp):
    # Based on README Logic (simplified interpretation)
    try:
        y = float(years_exp)
        if y < 2: return "Beginner"
        elif y < 5: return "Intermediate"
        else: return "Advanced"
    except:
        return "Beginner"

def save_interview_results(username, position, answers_data, wage_req, status, avg_score):
    # Format: L1-L2-Q1...Q16-Wage (Columns)
    # Rows: Label, Question, Answer, Grade
    
    # Prepare columns list
    cols = ["L1", "L2"] + [f"Q{i}" for i in range(1, 17)] + ["Wage_Expectation"]
    
    # Prepare data rows
    labels_row = ["Label"] * 19
    qs_row = [a['question'] for a in answers_data] + ["Wage Request"]
    ans_row = [a['answer'] for a in answers_data] + [str(wage_req)]
    grade_row = [a['grade'] for a in answers_data] + [status] # Using wage column for status in grade row

    df = pd.DataFrame([labels_row, qs_row, ans_row, grade_row], columns=cols)
    df.to_csv(f"{REPORT_PATH}/{username}_interview.csv", index=False)
    
    # Update User Profile
    user_dat = load_user_data(username)
    user_dat['interview_done'] = True
    user_dat['final_score'] = avg_score
    user_dat['final_status'] = status
    user_dat['wage_request'] = wage_req
    save_user_data(username, user_dat)

# --- PAGE FUNCTIONS ---

def login_page():
    st.title("Hire-ON! Login")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        u_user = st.text_input("Username")
        u_pass = st.text_input("Password", type="password")
        if st.button("Log In"):
            data = load_user_data(u_user)
            if data and data['password'] == u_pass:
                st.session_state.logged_in = True
                st.session_state.username = u_user
                st.session_state.identity_filled = data.get('identity_filled', False)
                st.session_state.interview_status = data.get('interview_done', False)
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        s_user = st.text_input("New Username")
        s_name = st.text_input("Full Name")
        s_pass = st.text_input("New Password", type="password")
        s_conf = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if s_pass != s_conf:
                st.error("Passwords do not match")
            elif load_user_data(s_user):
                st.error("User already exists")
            else:
                user_data = {
                    "username": s_user, "name": s_name, "password": s_pass, 
                    "identity_filled": False, "interview_done": False
                }
                save_user_data(s_user, user_data)
                st.success("Account created! Please Log In.")

def identity_page():
    st.title("Candidate Identity")
    st.info("Please complete your profile to proceed.")
    
    jobs = load_jobs()
    
    with st.form("identity_form"):
        dob = st.date_input("Birthday")
        address = st.text_area("Address")
        contact = st.text_input("Contact Number")
        position = st.selectbox("Application Position", jobs['position'].unique())
        mastery = st.text_area("Fields of Mastery / Skills")
        
        submitted = st.form_submit_button("Save & Continue")
        if submitted:
            user_dat = load_user_data(st.session_state.username)
            user_dat.update({
                "birthday": str(dob), "address": address, "contact": contact,
                "position": position, "mastery": mastery, "identity_filled": True
            })
            save_user_data(st.session_state.username, user_dat)
            st.session_state.identity_filled = True
            st.rerun()

def interview_engine():
    st.header("Interview Session")
    user_dat = load_user_data(st.session_state.username)
    position = user_dat.get('position')
    
    # 1. Determine Questions List
    # Initial 2 determination questions + 16 Main Questions
    if 'q_list' not in st.session_state:
        # Start with just determination questions
        st.session_state.q_list = question_bank.get_determination_questions()
    
    current_idx = st.session_state.current_q_index
    
    # Logic to transition from Determination (2 Qs) to Main (16 Qs)
    if current_idx == 2 and st.session_state.determined_level is None:
        # Analyze first 2 answers to determine level (Simplified logic: length of answer implies depth)
        # In real world, use NLP on the first 2 answers
        ans_len = len(st.session_state.interview_answers[0]['answer']) + len(st.session_state.interview_answers[1]['answer'])
        level = "Beginner"
        if ans_len > 100: level = "Intermediate"
        if ans_len > 200: level = "Advanced"
        
        st.session_state.determined_level = level
        # Generate next 16 questions
        main_qs = question_bank.get_interview_questions(position, level)
        st.session_state.q_list.extend(main_qs)
        st.rerun()

    # Logic for Wage Question (Final)
    if current_idx == 18 and not st.session_state.wage_question_shown:
        st.session_state.wage_question_shown = True
    
    # RENDER QUESTION
    if current_idx < 18:
        q_text = st.session_state.q_list[current_idx]
        st.subheader(f"Question {current_idx + 1}/18")
        st.write(q_text)
        
        answer = st.text_area("Your Answer:", key=f"ans_{current_idx}")
        
        if st.button("Submit Answer"):
            if not answer:
                st.warning("Please provide an answer.")
            else:
                # --- GRADING ---
                with st.spinner("Analyzing..."):
                    sent_score = nlp_engine.analyze_sentiment(answer)
                    # Calculate relevance against the Question text itself (simplified context)
                    rel_score = nlp_engine.calculate_relevance(answer, q_text)
                    grade = nlp_engine.grading_formula(sent_score, rel_score)
                    
                    st.session_state.interview_answers.append({
                        "question": q_text,
                        "answer": answer,
                        "grade": grade,
                        "sentiment": sent_score,
                        "relevance": rel_score
                    })
                    
                    st.session_state.current_q_index += 1
                    st.rerun()
    
    # RENDER WAGE QUESTION
    elif st.session_state.wage_question_shown:
        st.subheader("Final Question")
        wage_input = st.number_input("What is your expected monthly wage (IDR)?", min_value=0.0)
        
        if st.button("Finish Interview"):
            # --- FINAL CALCULATION ---
            total_score = sum([x['grade'] for x in st.session_state.interview_answers])
            avg_score = total_score / 18 if len(st.session_state.interview_answers) > 0 else 0
            
            # Wage Logic
            jobs = load_jobs()
            affordable = jobs.loc[jobs['position'] == position, 'affordable_wage'].values[0]
            golden_ratio = 1.618 # Phi
            max_wage = affordable * golden_ratio
            
            status = "REJECTED"
            final_wage_offer = 0
            
            # Threshold check
            if avg_score >= 0.8:
                if wage_input > max_wage:
                    status = "REJECTED (Wage too high)"
                elif wage_input >= (0.8 * affordable):
                    status = "ACCEPTED"
                    final_wage_offer = wage_input
                else:
                    status = "ACCEPTED (Standard)"
                    final_wage_offer = affordable
            else:
                status = "REJECTED (Score too low)"
            
            save_interview_results(
                st.session_state.username, position, 
                st.session_state.interview_answers, 
                wage_input, status, avg_score
            )
            
            st.session_state.interview_status = True
            st.rerun()

def dashboard_page():
    st.title("Candidate Dashboard")
    
    user_dat = load_user_data(st.session_state.username)
    df_res = pd.read_csv(f"{REPORT_PATH}/{st.session_state.username}_interview.csv")
    
    # Extract data from CSV structure (Row based)
    # Row 1: Questions, Row 2: Answers, Row 3: Grades
    questions = df_res.iloc[0, :18].tolist() # First 18 cols
    grades = pd.to_numeric(df_res.iloc[2, :18]).tolist()
    answers = df_res.iloc[1, :18].tolist()
    
    final_status = user_dat.get('final_status', 'Unknown')
    final_score = user_dat.get('final_score', 0)
    
    # 1. Identity & Status
    col1, col2, col3 = st.columns(3)
    col1.metric("Position", user_dat.get('position'))
    col2.metric("Overall Score", f"{final_score:.2f}")
    col3.metric("Status", final_status, delta_color="normal" if "ACCEPTED" in final_status else "inverse")
    
    st.divider()
    
    # 2. Score Bar Plot vs Threshold
    st.subheader("Performance Analysis")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=[f"Q{i}" for i in range(1, 19)], y=grades, name='Score'))
    fig_bar.add_hline(y=0.8, line_dash="dash", line_color="red", annotation_text="Threshold (0.8)")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # 3. Tabular Score
    st.subheader("Detailed Question Log")
    details_df = pd.DataFrame({
        "Question": questions,
        "Answer": answers,
        "Score": grades
    })
    st.dataframe(details_df)
    
    # 4. Word Analysis
    st.subheader("Language Analysis")
    
    # Top Frequent
    top_words = nlp_engine.extract_keywords(answers, top_n=3)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Most Frequent Words**")
        for word, count in top_words:
            st.write(f"- {word}: {count} times")
            
    # Simple weighting visualization (simulated by length/complexity)
    with c2:
        st.markdown("**Weighted/Significant Terms**")
        # In a real app, use TF-IDF scores here
        st.write("- (Analysis reserved for full TF-IDF implementation)")
        st.write(f"- Top Context: {user_dat.get('position')}")

    # 5. Closing
    st.divider()
    if "ACCEPTED" in final_status:
        st.balloons()
        st.success(f"Congratulations! We are thrilled to welcome you as our new {user_dat.get('position')}.")
    else:
        st.error("Motivation: Success is stumbling from failure to failure with no loss of enthusiasm. Keep improving!")

# --- MAIN APP CONTROLLER ---

def main():
    # Sidebar Menu
    if st.session_state.logged_in:
        with st.sidebar:
            st.image("https://img.icons8.com/clouds/100/000000/resume.png") # Placeholder
            st.write(f"Welcome, **{st.session_state.username}**")
            
            menu = ["Interview"]
            if st.session_state.interview_status:
                menu.insert(0, "Dashboard")
                
            choice = st.radio("Menu", menu + ["Logout"])
            
            if choice == "Logout":
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        if not st.session_state.identity_filled:
            identity_page()
        else:
            if choice == "Interview":
                if st.session_state.interview_status:
                    st.warning("You have already completed the interview. Go to Dashboard.")
                else:
                    interview_engine()
            elif choice == "Dashboard":
                dashboard_page()
    else:
        login_page()

if __name__ == "__main__":
    main()