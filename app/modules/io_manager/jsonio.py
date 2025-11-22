# app/modules/io_manager/jsonio.py

import json
from pathlib import Path
from .storage_paths import ensure_directories

def save_json(data: dict, path: Path):
    """
    Save dictionary to a JSON file with pretty formatting.
    """
    ensure_directories()
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path: Path) -> dict:
    """
    Load JSON file and return dictionary.
    """
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
