# app/modules/auth/auth_manager.py
import hashlib
from pathlib import Path
from typing import Optional, Dict
from app.modules.io_manager import save_json, load_json, USERS_DIR
from app.modules.utils.idgen import generate_user_id

USERS_DIR.mkdir(parents=True, exist_ok=True)

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def user_file(username: str) -> Path:
    # store one JSON per username for simplicity
    return USERS_DIR / f"{username}.json"

def create_user(username: str, password: str, full_name: str = "") -> Dict:
    """
    Create a user if username not exists.
    Returns saved metadata dict.
    """
    path = user_file(username)
    if path.exists():
        raise FileExistsError("User already exists")

    # generate a stable id based on username + timestamp
    file_id = generate_user_id((full_name or username)[:3].upper())
    metadata = {
        "File_ID": file_id,
        "Username": username,
        "PasswordHash": _hash_password(password),
        "FullName": full_name,
        "months_experience": 0,
        "wage_expectation": 0,
        "Specialties": [],
    }
    save_json(metadata, path)
    return metadata

def load_user(username: str) -> Optional[Dict]:
    path = user_file(username)
    if not path.exists():
        return None
    return load_json(path)

def verify_user(username: str, password: str) -> bool:
    data = load_user(username)
    if not data:
        return False
    return data.get("PasswordHash") == _hash_password(password)

def update_user(username: str, updates: Dict) -> Dict:
    data = load_user(username) or {}
    data.update(updates)
    save_json(data, user_file(username))
    return data
