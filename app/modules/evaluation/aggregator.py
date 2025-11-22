# app/modules/evaluation/aggregator.py

"""
Aggregator module
-----------------
Merges:
- user metadata
- QnA sentiment scores
- text analysis metrics
- final decision engine output

Output:
    dashboard-ready CSV
"""

import pandas as pd
from pathlib import Path
import json

from ..QnA.text_mining import behavioral_analyze
from ..QnA.decisions import DecisionEngine
from .scorer import Scorer
from .analyser import clarity_score, relevance_score
from ..io_manager.storage_paths import USERS_DIR, REPORTS_DIR

DASHBOARD_DIR = Path(REPORTS_DIR)
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)


def build_dashboard(user_id: str, company_budget: int):
    """
    Aggregates all available data and produces:
    app/data/reports/{user_id}.csv
    """
    meta_path = USERS_DIR / f"{user_id}.json"
    report_path = Path(REPORTS_DIR) / f"{user_id}.csv"
    out_path = DASHBOARD_DIR / f"{user_id}.csv"

    # --- Load metadata ---
    metadata = json.loads(meta_path.read_text())

    # --- Load QnA Report ---
    df = pd.read_csv(report_path)

    # Extract question columns only (Q1..Q16 + Wage)
    question_cols = [c for c in df.columns if c.startswith("Q")]

    # --- Compute metrics ---
    clarity = []
    relevance = []
    scores = []

    scorer = Scorer()

    for q in question_cols:
        q_text = df[q].iloc[0]   # Question
        a_text = df[q].iloc[1]   # Answer

        axis_scores = behavioral_analyze(a_text)
        scores.append(scorer.overall_score(axis_scores))

        clarity.append(clarity_score(a_text))
        relevance.append(relevance_score(a_text, q_text))

    # --- Decision Engine ---
    engine = DecisionEngine(company_budget)
    summary = engine.judge(
        question_scores=scores[:16],  # first 16 are actual questions
        sentiment=sum(scores) / len(scores),
        months_experience=metadata.get("months_experience", 0),
        wage_expectation=metadata.get("wage_expectation", 0)
    )

    # --- Construct dashboard row ---
    result = {
        "UserID": user_id,
        **metadata,
        "avg_sentiment_score": round(sum(scores) / len(scores), 4),
        "avg_clarity": round(sum(clarity) / len(clarity), 4),
        "avg_relevance": round(sum(relevance) / len(relevance), 4),
        "final_decision": summary["decision"],
        "final_score": summary["final_score"],
        "difficulty": summary["difficulty"],
        "wage_penalty": summary["wage_penalty"]
    }

    pd.DataFrame([result]).to_csv(out_path, index=False)

    return result
