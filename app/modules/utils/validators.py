# utils/validators.py

import re
from datetime import datetime

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
    age_years = (today - dob).days / 365

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
