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
        df = pd.DataFrame([[]])
        df.to_csv(path, index=False)
        return

    # If headers provided, create CSV with 4 logical rows (labels, questions, answers, scores)
    if len(headers) > 0:
        row0 = headers  # Labels
        row1 = [""] * len(headers)  # Questions (empty initially)
        row2 = [""] * len(headers)  # Answers (empty initially)
        row3 = [0.0] * len(headers)  # Scores (default 0)
        df = pd.DataFrame([row0, row1, row2, row3], columns=headers)
    else:
        df = pd.DataFrame()
    
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def append_column(path: Path, col_name: str, rows: list):
    """
    Append a new column with 4 rows.
    rows: [label, question, answer, score] or shorter; will be padded.
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
        df = pd.DataFrame({col_name: rows})
        df.to_csv(path, index=False)
        return

    # If file exists, load and append the column
    df = pd.read_csv(path)

    # If file has fewer than 4 rows, expand it to have 4 rows
    if df.shape[0] < 4:
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

def load_csv_report(path: Path):
    """
    Load a CSV report and return it as a pandas DataFrame.
    Returns empty DataFrame if file doesn't exist.
    """
    path = Path(path)

    if not path.exists():
        return pd.DataFrame()  # Return empty table

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

def append_to_csv(path: Path, df: pd.DataFrame):
    """Compatibility alias for old function name."""
    return append_csv(path, df)


def create_csv_report(path: Path, df: pd.DataFrame = None):
    """
    Create a new CSV report.
    Compatible with old signature where only 'path' is passed.
    If df is None, create an empty CSV file.
    """
    ensure_directories()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # If no DataFrame provided → create empty CSV
    if df is None:
        empty_df = pd.DataFrame()
        empty_df.to_csv(path, index=False)
        return path

    # If df provided → write normally
    df.to_csv(path, index=False)
    return path

