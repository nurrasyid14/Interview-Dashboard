#!/usr/bin/env python3
"""
Comprehensive test suite for AI Interview System.
Tests all critical functionality.
"""

import sys
from pathlib import Path
import json
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

# Test counter
passed = 0
failed = 0
errors = []

def test(name, func):
    global passed, failed, errors
    try:
        func()
        passed += 1
        print(f"✓ {name}")
    except AssertionError as e:
        failed += 1
        errors.append(f"✗ {name}: {e}")
        print(f"✗ {name}")
    except Exception as e:
        failed += 1
        errors.append(f"✗ {name}: {type(e).__name__}: {e}")
        print(f"✗ {name}")

# =================================================================
# VALIDATORS TESTS
# =================================================================
def test_username_validation():
    from app.modules.utils import validate_username
    assert validate_username("test.user") == True
    assert validate_username("user123") == True
    assert validate_username("TestUser") == False  # uppercase
    assert validate_username("test-user") == False  # hyphen
    assert validate_username("123") == False  # no letters

def test_password_validation():
    from app.modules.utils import validate_password
    assert validate_password("TestPass123!", "testuser") == True
    assert validate_password("weak", "testuser") == False  # too short
    assert validate_password("testuser1!", "testuser") == False  # contains username
    assert validate_password("ALLUPPERCASE1!", "testuser") == False  # no lowercase

def test_age_validation():
    from app.modules.utils import validate_age
    assert validate_age("15-03-1995") == True  # 29+ years old
    assert validate_age("01-01-2010") == False  # too young
    assert validate_age("31-12-2020") == False  # too young
    assert validate_age("invalid") == False

# =================================================================
# I/O TESTS
# =================================================================
def test_json_io():
    from app.modules.io_manager import save_json, load_json
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test.json"
        data = {"name": "test", "value": 123}
        save_json(data, path)
        loaded = load_json(path)
        assert loaded == data
        assert load_json(Path(tmpdir) / "nonexistent.json") == {}  # fallback

def test_csv_operations():
    from app.modules.io_manager.csvio import ensure_csv, append_column
    import pandas as pd
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test.csv"
        
        # Create with headers
        ensure_csv(path, headers=["Q1", "Q2"])
        df = pd.read_csv(path)
        assert df.shape[0] == 4  # 4 rows
        assert df.shape[1] == 2  # 2 columns
        
        # Append column
        append_column(path, "Q3", ["Q3", "Question 3", "Answer 3", "0.5"])
        df = pd.read_csv(path)
        assert "Q3" in df.columns

# =================================================================
# TEXT MINING TESTS
# =================================================================
def test_tokenizer():
    from app.modules.QnA.text_mining import Tokenizer
    tok = Tokenizer()
    tokens = tok.process("This is a test!")
    assert len(tokens) > 0
    assert "this" in tokens
    assert "is" in tokens

def test_behavioral_sentiment():
    from app.modules.QnA.text_mining import behavioral_analyze
    
    # Positive answer
    result = behavioral_analyze("I am very motivated and determined to succeed")
    assert result["overall"] > 0
    
    # Negative answer
    result = behavioral_analyze("I give up easily and don't try hard")
    assert result["overall"] < 0
    
    # Neutral answer
    result = behavioral_analyze("The weather is nice today")
    assert -0.1 < result["overall"] < 0.1

# =================================================================
# AUTH TESTS
# =================================================================
def test_auth_create_user():
    from app.modules.auth import create_user, verify_user, load_user
    import tempfile
    import shutil
    
    # Use temp directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        import app.modules.io_manager.storage_paths as sp
        original_users_dir = sp.USERS_DIR
        sp.USERS_DIR = Path(tmpdir)
        
        try:
            metadata = create_user("testuser", "TestPass123!", "Test User")
            assert metadata["Username"] == "testuser"
            
            # Verify login
            assert verify_user("testuser", "TestPass123!") == True
            assert verify_user("testuser", "wrongpass") == False
            
            # Load user
            user = load_user("testuser")
            assert user is not None
            
        finally:
            sp.USERS_DIR = original_users_dir

# =================================================================
# QUESTION BANK TESTS
# =================================================================
def test_question_bank():
    from app.modules.QnA import load_questions
    q = load_questions()
    assert len(q["leveling"]) == 2
    assert len(q["beginner"]) == 16
    assert len(q["intermediate"]) == 16
    assert len(q["advanced"]) == 16

# =================================================================
# DECISION ENGINE TESTS
# =================================================================
def test_decision_engine():
    from app.modules.QnA.decisions import DecisionEngine
    
    engine = DecisionEngine(company_budget=5000)
    
    # High scores → Layak
    result = engine.judge(
        question_scores=[0.9] * 16,
        sentiment=0.8,
        months_experience=12,
        wage_expectation=3000
    )
    assert result["label"] == "Layak"
    assert result["final_score"] >= 0.8
    
    # Low scores → Tidak Layak
    result = engine.judge(
        question_scores=[0.3] * 16,
        sentiment=-0.5,
        months_experience=6,
        wage_expectation=2000
    )
    assert result["label"] == "Tidak Layak"
    assert result["final_score"] < 0.6
    
    # Medium scores → Dipertimbangkan
    result = engine.judge(
        question_scores=[0.65] * 16,
        sentiment=0.3,
        months_experience=10,
        wage_expectation=3500
    )
    assert result["label"] == "Dipertimbangkan"
    assert 0.6 <= result["final_score"] < 0.8

# =================================================================
# JUDGER TESTS
# =================================================================
def test_judger():
    from app.modules.QnA import Judger
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        import app.modules.io_manager.storage_paths as sp
        original_reports = sp.REPORTS_DIR
        sp.REPORTS_DIR = Path(tmpdir)
        
        try:
            judger = Judger(user_id="testuser", company_budget=5000)
            
            # Process answer
            score = judger.process_answer(
                "What motivates you?",
                "I am very motivated and determined to achieve my goals."
            )
            assert isinstance(score, float)
            assert -1 <= score <= 1
            
            # Process 15 more answers to reach 16
            for i in range(15):
                judger.process_answer(
                    f"Question {i}?",
                    "I am reliable and honest in my work."
                )
            
            # Finalize
            report = judger.finalize(months_experience=12, wage_expectation=4000)
            assert "label" in report
            assert "final_score" in report
            
        finally:
            sp.REPORTS_DIR = original_reports

# =================================================================
# RUN ALL TESTS
# =================================================================
def main():
    print("=" * 60)
    print("AI Interview System - Test Suite")
    print("=" * 60)
    print()
    
    print("VALIDATORS:")
    test("Username validation", test_username_validation)
    test("Password validation", test_password_validation)
    test("Age validation", test_age_validation)
    print()
    
    print("I/O OPERATIONS:")
    test("JSON I/O", test_json_io)
    test("CSV operations", test_csv_operations)
    print()
    
    print("TEXT MINING:")
    test("Tokenizer", test_tokenizer)
    test("Behavioral sentiment", test_behavioral_sentiment)
    print()
    
    print("AUTHENTICATION:")
    test("Create and verify user", test_auth_create_user)
    print()
    
    print("QUESTION BANK:")
    test("Question bank loading", test_question_bank)
    print()
    
    print("DECISION ENGINE:")
    test("Decision engine scoring", test_decision_engine)
    print()
    
    print("JUDGER:")
    test("Judger pipeline", test_judger)
    print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if errors:
        print("\nFailed Tests:")
        for error in errors:
            print(f"  {error}")
        print()
        return 1
    else:
        print("\nALL TESTS PASSED ✓")
        print()
        return 0

if __name__ == "__main__":
    sys.exit(main())
