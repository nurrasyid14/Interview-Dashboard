# app/modules/io_manager/__init__.py

"""
I/O management layer for JSON and CSV operations.

Exports:
- save_json, load_json
- write_csv, append_csv
- USERS_DIR, REPORTS_DIR, TEMP_DIR
"""

from .jsonio import save_json, load_json
from .csvio import write_csv, append_csv, ensure_csv, append_column, update_score_row
from .storage_paths import USERS_DIR, REPORTS_DIR, TEMP_DIR, ensure_directories

__all__ = [
    "save_json",
    "load_json",
    "write_csv",
    "append_csv",
    "USERS_DIR",
    "REPORTS_DIR",
    "TEMP_DIR",
    "ensure_directories",
    "ensure_csv",
    "append_column",
    "update_score_row",
]
