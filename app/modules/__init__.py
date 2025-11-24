# app/modules/__init__.py
"""
Grand __init__.py for app/modules

Exposes all key submodules:
- QnA (questions, judger, text mining, decisions)
- IO Manager (csvio, storage_paths)
- Evaluation (scorer, analyser, aggregator)
- Operator (if any)
- Logger (if any)
"""

# -----------------------
# QnA Module
# -----------------------
from .QnA.questions import (
    get_questions_for_position,
    get_leveling_questions,
    get_wage_question,
    get_all_questions,
    get_job_positions,
    determine_level,
)
from .QnA.judger import Judger, InterviewJudger
from .QnA.decisions import DecisionEngine, FinalDecisions


from .QnA.text_mining import(
    analyze_sentiment,
    calculate_relevance,
    grading_formula,
    extract_keywords,)

from .QnA.decisions import DecisionEngine

# -----------------------
# IO Manager Module
# -----------------------
from .io_manager.csvio import write_csv, append_csv, ensure_csv, append_column
from .io_manager.storage_paths import USERS_DIR, REPORTS_DIR, ensure_directories

# -----------------------
# Evaluation Module
# -----------------------
from .evaluation.scorer import Scorer
from .evaluation.analyser import clarity_score, relevance_score, frequent_words, semantic_similarity
from .evaluation.aggregator import build_dashboard
from .frontend_loader import load_css, load_js

# -----------------------
# Operator / Logger (if any)
# -----------------------
# from .operator import ...
from .logging.logger import get_logger, log_user_event  
__all__ = [
    # QnA
    "get_questions_for_position",
    "get_leveling_questions",
    "get_wage_question",
    "get_all_questions",
    "get_job_positions",
    "determine_level",
    "Judger",
    "InterviewJudger",
    "DecisionEngine",
    "FinalDecisions",
    "analyze_sentiment",
    "calculate_relevance",
    "grading_formula",
    "extract_keywords",
    
    # IO Manager
    "write_csv",
    "append_csv",
    "ensure_csv",
    "append_column",
    "USERS_DIR",
    "REPORTS_DIR",
    "ensure_directories",

    # Evaluation
    "Scorer",
    "sentiment_to_score",
    "clarity_score",
    "relevance_score",
    "frequent_words",
    "semantic_similarity",
    "build_dashboard",

    # Operator / Logger (if any)
    "get_logger",
    "log_user_event",

    # Frontend Loader
    "load_css",
    "load_js",
]
