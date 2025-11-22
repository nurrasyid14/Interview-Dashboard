# app/modules/io_manager/csvio.py
"""
CSV I/O utilities for incremental QnA storage.
Includes:
- ensure_csv: create CSV with 4 rows (labels, questions, answers, scores)
- append_column: add a new column to existing CSV
- update_score_row: update 4th row (score) for a column
- write_csv / append_csv: general CSV operations
"""

from pathlib import Path
import pandas as pd
from .storage_paths import ensure_directories


def ensure_csv(path: Path, headers: list):
    """
    Ensures a CSV exists with the given headers.
    Initializes 4 rows: labels, questions, answers, scores (default 0)
    """
    path = Path(path)
    if not path.exists():
        df = pd.DataFrame(columns=headers)
        # Initialize 4 rows
        df.loc[0] = headers                   # Row 1: Labels
        df.loc[1] = [""] * len(headers)       # Row 2: Questions
        df.loc[2] = [""] * len(headers)       # Row 3: Answers
        df.loc[3] = [0.0] * len(headers)      # Row 4: Scores
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)


def append_column(path: Path, col_name: str, rows: list):
    """
    Append a new column with 4 rows.
    rows: [label, question, answer, score]
    If CSV doesn't exist -> create default empty CSV
    """
    path = Path(path)
    ensure_csv(path, headers=[])
    df = pd.read_csv(path)

    # Fill missing rows to ensure 4 rows
    if len(rows) < 4:
        rows += [""] * (4 - len(rows))
    elif len(rows) > 4:
        rows = rows[:4]

    df[col_name] = rows
    df.to_csv(path, index=False)


def update_score_row(path: Path, col_name: str, score: float):
    """
    Update the 4th row (Scores) for a specific column.
    Raises KeyError if column doesn't exist.
    """
    path = Path(path)
    df = pd.read_csv(path)
    if col_name not in df.columns:
        raise KeyError(f"Column {col_name} not found in {path}")
    df.at[3, col_name] = score
    df.to_csv(path, index=False)


def write_csv(path: Path, df: pd.DataFrame):
    """
    Overwrite a CSV file safely, ensuring directories exist.
    """
    ensure_directories()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def append_csv(path: Path, df: pd.DataFrame):
    """
    Append DataFrame rows to an existing CSV.
    Creates the file if it doesn't exist.
    """
    ensure_directories()
    path = Path(path)

    if path.exists():
        old_df = pd.read_csv(path)
        merged = pd.concat([old_df, df], ignore_index=True)
        merged.to_csv(path, index=False)
    else:
        df.to_csv(path, index=False)
