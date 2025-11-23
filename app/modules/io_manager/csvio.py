# app/modules/io_manager/csvio.py

from pathlib import Path
import pandas as pd
from .storage_paths import ensure_directories


def ensure_csv(path: Path, headers: list | None = None):
    """
    Ensures a CSV exists with the given headers.
    Initializes 4 rows: labels, questions, answers, scores (default 0).
    If headers is None or empty and file exists -> do nothing.
    If headers is None or empty and file doesn't exist -> create an empty CSV with
    no Q columns but still create the file to reserve the path.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        return

    if not headers:
        # create an empty DataFrame (no Q columns) but keep the 4-row convention
        df = pd.DataFrame()  # no columns yet
        # create placeholder rows (0..3) to keep consistent indexing if desired
        df = pd.DataFrame([[]])  # initially one empty row
        df.to_csv(path, index=False)
        return

    # If headers provided, create CSV with 4 logical rows (labels, questions, answers, scores)
    df = pd.DataFrame(columns=headers)
    # Initialize 4 rows (we'll use row index 0..3)
    # Row 0: Labels (use headers as labels)
    # Row 1: Questions (empty strings)
    # Row 2: Answers (empty strings)
    # Row 3: Scores (zeros)
    if len(headers) > 0:
        # build rows as a dict-of-lists consistent with columns
        row0 = headers
        row1 = [""] * len(headers)
        row2 = [""] * len(headers)
        row3 = [0.0] * len(headers)
        df = pd.DataFrame([row0, row1, row2, row3], columns=headers)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def append_column(path: Path, col_name: str, rows: list):
    """
    Append a new column with 4 rows.
    rows: either [label, question, answer, score] or shorter; will be padded.
    If CSV doesn't exist -> create it with this column as the first column.
    """
    path = Path(path)
    ensure_directories()
    path.parent.mkdir(parents=True, exist_ok=True)

    # Ensure rows length is exactly 4
    if len(rows) < 4:
        rows = rows + [""] * (4 - len(rows))
    elif len(rows) > 4:
        rows = rows[:4]

    if not path.exists():
        # create DataFrame with this single column
        df = pd.DataFrame([rows], columns=[col_name]).T  # create vertical then transpose
        # After transpose we'll have 4 rows with index 0..3 and a single column, but we want rows as row-index
        df = pd.DataFrame([rows], columns=[col_name])  # simpler: one row per entire list -> we need 4 rows
        # Build DataFrame properly: rows are 4 rows
        df = pd.DataFrame([rows], columns=[col_name]).T
        # Reformat to 4 named rows (0..3)
        df = pd.DataFrame({col_name: rows})
        df.to_csv(path, index=False)
        return

    # If file exists, load and append the column
    df = pd.read_csv(path)

    # If file has fewer than 4 rows, try to expand it to have 4 rows
    if df.shape[0] < 4:
        # create missing rows with empty values for existing columns
        missing = 4 - df.shape[0]
        for _ in range(missing):
            df.loc[df.shape[0]] = [""] * df.shape[1]

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
    # Ensure 4 rows
    if df.shape[0] < 4:
        missing = 4 - df.shape[0]
        for _ in range(missing):
            df.loc[df.shape[0]] = [""] * df.shape[1]
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
