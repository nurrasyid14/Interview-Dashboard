# app/modules/utils/idgen.py

from datetime import datetime
from pathlib import Path

COUNTER_DIR = Path("app/data/temp/counters")

def _ensure_counter_dir():
    COUNTER_DIR.mkdir(parents=True, exist_ok=True)

def _load_counter(timestamp: str) -> int:
    """Load counter for this timestamp, return 0 if none."""
    try:
        counter_file = COUNTER_DIR / f"{timestamp}.txt"
        if counter_file.exists():
            return int(counter_file.read_text().strip())
    except Exception:
        pass
    return 0

def _save_counter(timestamp: str, value: int):
    """Added error handling for counter file writes"""
    try:
        counter_file = COUNTER_DIR / f"{timestamp}.txt"
        _ensure_counter_dir()
        counter_file.write_text(str(value))
    except Exception:
        pass

def generate_user_id(initials: str) -> str:
    """
    Generate ID of the form:
    <ord_initials>-YYYYMMDD-HHMMSS-XXX
    Example: MNR -> 77-78-82-20251123-020000-001
    """
    initials = (initials or "USR").upper().strip()[:3]  # Add default initials
    
    try:
        ord_part = "-".join(str(ord(c)) for c in initials)
    except Exception:
        ord_part = "000"

    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")

    timestamp = f"{date_str}-{time_str}"

    _ensure_counter_dir()
    counter = _load_counter(timestamp)
    counter += 1
    _save_counter(timestamp, counter)

    return f"{ord_part}-{timestamp}-{counter:03d}"
