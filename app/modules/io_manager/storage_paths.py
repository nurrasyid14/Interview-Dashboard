# app/modules/io_manager/storage_paths.py

from pathlib import Path

# Root data directory
DATA_ROOT = Path("app/data")

# Specific directories for structured storage
USERS_DIR = DATA_ROOT / "users"
REPORTS_DIR = DATA_ROOT / "reports"
TEMP_DIR = DATA_ROOT / "temp"

def ensure_directories():
    """
    Create required directories if they don't exist.
    This must be called by modules that perform file I/O.
    """
    USERS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
