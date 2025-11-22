# app/modules/auth/metadata_filler.py

from pathlib import Path
from app.modules.utils import (
    validate_metadata,
    generate_user_id
)
from app.modules.io_manager import save_json, USERS_DIR

def extract_initials(name: str) -> str:
    """
    Extract initials from a name.
    Example:
    - 'Muhamad Nur Rasyid' -> MNR
    - 'Ari Lasso' -> AL
    """
    parts = name.strip().split()
    return "".join(p[0].upper() for p in parts if p)

def build_metadata(name: str, birthdate: str, contact: str, address: str, jobs: list, username: str) -> dict:
    """
    Construct the metadata JSON object.
    """
    if not validate_metadata(name, username, birthdate, jobs):
        raise ValueError("Invalid user metadata submitted.")

    initials = extract_initials(name)
    user_id = generate_user_id(initials)

    metadata = {
        "File_ID": user_id,
        "Nama": name,
        "Tanggal_Lahir": birthdate,
        "Kontak": contact,
        "Alamat": address,
        "Keahlian": jobs,
        "Username": username
    }

    return metadata

def save_metadata(metadata: dict) -> Path:
    """
    Save metadata JSON to app/data/users/<File_ID>.json
    """
    file_id = metadata["File_ID"]
    output_path = USERS_DIR / f"{file_id}.json"
    save_json(metadata, output_path)
    return output_path
