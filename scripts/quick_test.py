#!/usr/bin/env python3
"""
AI Interview System - Module Verification
Quick verification that all critical modules can be imported and initialized.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test all critical module imports."""
    print("\n" + "="*60)
    print("AI Interview System - Module Verification")
    print("="*60)
    
    print("\n1. Testing imports...")
    
    try:
        from app.modules.auth import create_user, verify_user, load_user
        print("   ✓ Auth module")
    except Exception as e:
        print(f"   ✗ Auth module: {e}")
        return False
    
    try:
        from app.modules.utils import (
            validate_username,
            validate_password,
            validate_age,
            generate_user_id
        )
        print("   ✓ Utils module")
    except Exception as e:
        print(f"   ✗ Utils module: {e}")
        return False
    
    try:
        from app.modules.io_manager import load_csv_report, append_to_csv
        print("   ✓ IO Manager module")
    except Exception as e:
        print(f"   ✗ IO Manager module: {e}")
        return False
    
    try:
        from app.modules.QnA import (
            QuestionBank,
            InterviewJudger,
            TextMiningPipeline,
            FinalDecisions
        )
        print("   ✓ QnA module")
    except Exception as e:
        print(f"   ✗ QnA module: {e}")
        return False
    
    print("\n2. Testing validation functions...")
    
    # Test password validation
    try:
        valid_pwd = validate_password("TestPass@123", "testuser")
        invalid_pwd = validate_password("weak", "testuser")
        assert valid_pwd == True, "Valid password should pass"
        assert invalid_pwd == False, "Weak password should fail"
        print("   ✓ Password validation")
    except Exception as e:
        print(f"   ✗ Password validation: {e}")
        return False
    
    # Test username validation
    try:
        valid_user = validate_username("test.user")
        invalid_user = validate_username("TestUser")  # uppercase not allowed
        assert valid_user == True, "Valid username should pass"
        assert invalid_user == False, "Uppercase username should fail"
        print("   ✓ Username validation")
    except Exception as e:
        print(f"   ✗ Username validation: {e}")
        return False
    
    # Test age validation
    try:
        valid_age = validate_age("01-01-2000")  # Should be 24+ years old
        invalid_age = validate_age("01-01-2010")  # Should be ~14 years old
        assert valid_age == True, "Valid age should pass"
        assert invalid_age == False, "Invalid age should fail"
        print("   ✓ Age validation")
    except Exception as e:
        print(f"   ✗ Age validation: {e}")
        return False
    
    # Test ID generation
    try:
        user_id = generate_user_id("ABC")
        assert user_id is not None, "User ID should be generated"
        assert "-" in user_id, "User ID should contain dashes"
        print(f"   ✓ ID generation (Sample: {user_id})")
    except Exception as e:
        print(f"   ✗ ID generation: {e}")
        return False
    
    print("\n3. Testing core modules...")
    
    try:
        qb = QuestionBank()
        assert qb.get_leveling_questions() is not None
        print("   ✓ Question Bank initialization")
    except Exception as e:
        print(f"   ✗ Question Bank: {e}")
        return False
    
    try:
        tm = TextMiningPipeline()
        test_text = "This is a great opportunity!"
        score = tm.analyze_sentiment(test_text)
        assert -1 <= score <= 1, "Sentiment score should be between -1 and 1"
        print(f"   ✓ Text Mining (Sample sentiment: {score:.2f})")
    except Exception as e:
        print(f"   ✗ Text Mining: {e}")
        return False
    
    print("\n4. Testing data persistence...")
    
    try:
        from app.modules.io_manager import create_csv_report, load_csv_report
        test_user = "test_verify_user"
        csv_path = create_csv_report(test_user)
        assert csv_path.exists(), "CSV report should be created"
        print("   ✓ CSV report creation")
    except Exception as e:
        print(f"   ✗ CSV operations: {e}")
        return False
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED - System is ready!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Run: streamlit run main.py")
    print("  2. Login with: dev.premium1 / DevTest@2024")
    print("  3. Or signup with new credentials")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
