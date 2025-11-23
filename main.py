import streamlit as st

# --------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------
from app.modules.auth.auth_manager import (
    create_user, verify_user, load_user, update_user
)
from app.modules.utils.validators import validate_username, validate_password, validate_age
from app.modules.QnA.questions import load_questions
from app.modules.QnA.judger import Judger
from app.modules.QnA.dashboard import DashboardBuilder


# --------------------------------------------------------------------
# GLOBAL CONFIG
# --------------------------------------------------------------------
st.set_page_config(page_title="AI Interview System", layout="centered")

# Hide sidebar
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display:none;}
        div[data-testid="stToolbar"] {display:none;}
    </style>
""", unsafe_allow_html=True)

# Init session states
st.session_state.setdefault("auth", False)
st.session_state.setdefault("auth_user", None)
st.session_state.setdefault("user_metadata", None)
st.session_state.setdefault("page", "login")  # global router
st.session_state.setdefault("judger", None)
st.session_state.setdefault("completed", False)
st.session_state.setdefault("final_report", None)


# --------------------------------------------------------------------
# ROUTER
# --------------------------------------------------------------------
def go(page_name: str):
    st.session_state.page = page_name
    st.rerun()


# --------------------------------------------------------------------
# PAGE 1 — LOGIN / SIGNUP
# --------------------------------------------------------------------
def page_login():

    st.title("Login / Signup")

    # If logged in → force identity fill
    if st.session_state.auth:
        go("identity")

    tab_login, tab_signup = st.tabs(["Login", "Signup"])

    # --- LOGIN TAB ---
    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

        if submit:
            if verify_user(username, password):
                st.session_state.auth = True
                st.session_state.auth_user = username
                st.session_state.user_metadata = load_user(username)
                go("identity")
            else:
                st.error("Invalid username or password")

    # --- SIGNUP TAB ---
    with tab_signup:
        with st.form("signup_form"):
            new_username = st.text_input("Choose username")
            new_password = st.text_input("Choose password", type="password")
            full_name = st.text_input("Full name (optional)")
            register = st.form_submit_button("Create Account")

        if register:
            if not validate_username(new_username):
                st.error("Invalid username")
            elif not validate_password(new_password, new_username):
                st.error("Weak password")
            else:
                try:
                    create_user(new_username, new_password, full_name=full_name)
                    st.success("Account created. Now login.")
                except FileExistsError:
                    st.error("Username already exists")


# --------------------------------------------------------------------
# TOP NAV (AFTER IDENTITY PAGE)
# --------------------------------------------------------------------
def top_nav():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    if col1.button("Interview"):
        go("interview")

    if col2.button("Dashboard"):
        go("dashboard")

    if col3.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")


# --------------------------------------------------------------------
# PAGE 2 — IDENTITY
# --------------------------------------------------------------------
def page_identity():
    if not st.session_state.auth:
        go("login")

    meta = st.session_state.user_metadata

    st.title("Identity Information (Required)")

    with st.form("identity_form"):
        full_name = st.text_input("Full Name", value=meta.get("FullName", ""))
        birthdate = st.text_input("Birthdate (dd-mm-yyyy)", value=meta.get("Tanggal_Lahir", ""))
        months = st.number_input("Months of experience", min_value=0,
                                 value=int(meta.get("months_experience", 0)))
        address = st.text_input("Address", value=meta.get("Address", ""))
        position = st.selectbox("Position", [
            "Accountant", "Chef", "Manager", "Supervisor", "Business Advisor"
        ])
        specialties = st.multiselect(
            "Specialties", ["Option 1", "Option 2", "Option 3"],
            default=meta.get("Specialties", [])
        )

        save = st.form_submit_button("Save Profile")

    if save:
        if birthdate and not validate_age(birthdate):
            st.error("Invalid birthdate or under 18.")
        else:
            update_user(st.session_state.auth_user, {
                "FullName": full_name,
                "Tanggal_Lahir": birthdate,
                "months_experience": int(months),
                "Address": address,
                "Position": position,
                "Specialties": specialties,
            })
            st.session_state.user_metadata = load_user(st.session_state.auth_user)
            st.success("Saved.")

            go("menu")

    # Identity must be filled before accessing menu
    return


# --------------------------------------------------------------------
# PAGE — MENU SCREEN
# --------------------------------------------------------------------
def page_menu():
    st.title("Welcome!")

    st.write("Your identity is saved. Choose what to do next.")
    top_nav()


# --------------------------------------------------------------------
# PAGE 3 — INTERVIEW
# --------------------------------------------------------------------
def page_interview():
    if not st.session_state.auth:
        go("login")

    top_nav()

    st.title("Interview")

    # Prepare Judger
    if st.session_state.judger is None:
        st.session_state.judger = Judger(
            user_id=st.session_state.auth_user,
            company_budget=5000
        )
        st.session_state.q_index = 0
        st.session_state.level = "leveling"
        st.session_state.answers = []
        st.session_state._leveling_count = 0

    questions = load_questions()

    # Leveling questions (2 Q)
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
            # Decide level
            months = int(st.session_state.user_metadata.get("months_experience", 0))
            if months < 12:
                st.session_state.level = "beginner"
            elif months < 18:
                st.session_state.level = "intermediate"
            else:
                st.session_state.level = "advanced"
            st.rerun()
        return

    # Main question banks
    bank = questions[st.session_state.level]
    q_idx = st.session_state.q_index

    if q_idx < len(bank):
        q_text = bank[q_idx]
        with st.form(f"q_{q_idx}"):
            a = st.text_area(f"Q{q_idx+1}: {q_text}")
            sub = st.form_submit_button("Submit")
        if sub:
            st.session_state.judger.process_answer(q_text, a)
            st.session_state.answers.append(a)
            st.session_state.q_index += 1
            st.rerun()
        return

    # Wage expectation
    st.info("All questions finished.")
    wage = st.number_input("Wage expectation", min_value=0, step=100)

    if st.button("Submit Wage"):
        report = st.session_state.judger.finalize(
            months_experience=int(st.session_state.user_metadata.get("months_experience", 0)),
            wage_expectation=int(wage),
        )
        st.session_state.final_report = report
        st.session_state.completed = True
        go("result")


# --------------------------------------------------------------------
# PAGE 4 — RESULT
# --------------------------------------------------------------------
def page_result():
    if not st.session_state.auth:
        go("login")

    top_nav()

    if not st.session_state.completed:
        st.info("You have not finished interview.")
        return

    st.title("Interview Result")

    st.json(st.session_state.final_report)

    lbl = st.session_state.final_report.get("label")

    if lbl == "Layak":
        st.success("ACCEPTED")
    elif lbl == "Dipertimbangkan":
        st.warning("CONSIDERED")
    else:
        st.error("REJECTED")


# --------------------------------------------------------------------
# PAGE 5 — DASHBOARD
# --------------------------------------------------------------------
def page_dashboard():
    if not st.session_state.auth:
        go("login")

    top_nav()

    st.title("Dashboard")

    if not st.session_state.completed:
        st.info("No interviews done yet.")
        return

    builder = DashboardBuilder(st.session_state.auth_user)
    dash = builder.build()

    st.subheader("Identity")
    st.write(dash["identity"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Relevance", dash["relevance_score"])
    col2.metric("Sentiment", dash["sentiment_score"])
    col3.metric("Overall", dash["overall_score"])

    st.write("### Most Frequent Words")
    st.write(dash["most_frequent_words"])

    st.write("### Most Weighted Words")
    st.write(dash["most_weighted_words"])

    st.write("### Score Bar Chart")
    import pandas as pd
    df = pd.DataFrame({
        "Label": dash["bar_chart"]["labels"],
        "Score": dash["bar_chart"]["scores"]
    }).set_index("Label")

    st.bar_chart(df)


# --------------------------------------------------------------------
# MASTER ROUTING LOGIC
# --------------------------------------------------------------------
if st.session_state.page == "login":
    page_login()
elif st.session_state.page == "identity":
    page_identity()
elif st.session_state.page == "menu":
    page_menu()
elif st.session_state.page == "interview":
    page_interview()
elif st.session_state.page == "result":
    page_result()
elif st.session_state.page == "dashboard":
    page_dashboard()
