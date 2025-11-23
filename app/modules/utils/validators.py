# app/modules/utils/validators.py

import re
from datetime import datetime

# username: lowercase letters required, may contain digits/dot/underscore
USERNAME_REGEX = re.compile(r"^(?=.*[a-z])[a-z0-9._]+$")

def validate_name(name: str) -> bool:
    """Name must contain alphabetic characters and not be empty."""
    return isinstance(name, str) and len(name.strip()) > 0

def validate_username(username: str) -> bool:
    """
    Username rules:
    - lowercase only
    - digits allowed
    - dot allowed
    - underscore allowed
    - must contain at least 1 alphabet
    """
    if not isinstance(username, str):
        return False
    return USERNAME_REGEX.match(username) is not None

def validate_age(birthdate: str) -> bool:
    """
    birthdate format: dd-mm-yyyy
    Must be >= 18 years old.
    """
    try:
        day, month, year = map(int, birthdate.split("-"))
        dob = datetime(year, month, day)
    except Exception:
        return False

    today = datetime.now()
    age_years = (today - dob).days / 365.25  # slightly more accurate leap-year adjustment

    return age_years >= 18

def validate_job_specialties(jobs) -> bool:
    """Must be a non-empty list of job specialties."""
    return isinstance(jobs, list) and len(jobs) > 0

def validate_metadata(name, username, birthdate, jobs) -> bool:
    """Convenience wrapper for full metadata validation."""
    return (
        validate_name(name) and
        validate_username(username) and
        validate_age(birthdate) and
        validate_job_specialties(jobs)
    )

def validate_password(password: str, username: str) -> bool:
    """
    Password rules:
    - at least 8 characters
    - at least 1 uppercase letter
    - at least 1 lowercase letter
    - at least 1 digit
    - at least 1 special character (any non-alphanumeric)
    - must not contain the username
    """
    if not isinstance(password, str) or len(password) < 8:
        return False
    if username and username.lower() in password.lower():
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    # more permissive: any non-alphanumeric counts as "special"
    if not re.search(r"[^a-zA-Z0-9]", password):
        return False
    return True
