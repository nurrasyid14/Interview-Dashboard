# app/modules/auth/login.py

from pathlib import Path
from app.modules.utils import validate_username
from app.modules.io_manager import load_json, USERS_DIR

def user_exists(username: str) -> bool:
    """
    Check if any metadata file belongs to this username.
    """
    for file in USERS_DIR.glob("*.json"):
        data = load_json(file)
        if data.get("Username") == username:
            return True
    return False

def get_user_metadata(username: str) -> dict | None:
    """
    Load and return metadata JSON by username.
    """
    for file in USERS_DIR.glob("*.json"):
        data = load_json(file)
        if data.get("Username") == username:
            return data
    return None

def login(username: str) -> dict:
    """
    Simple login:
    - username must be valid format
    - username must exist in saved metadata
    """
    if not validate_username(username):
        raise ValueError("Invalid username format.")

    metadata = get_user_metadata(username)

    if metadata is None:
        raise FileNotFoundError("User not found.")

    return metadata
