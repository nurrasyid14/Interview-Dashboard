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
from .QnA.questions import load_questions
from .QnA.judger import Judger
from .QnA.text_mining import (
    BasePreprocessor,
    Tokenizer,
    Stemmer,
    Lemmatizer,
    BagOfWords,
    TFIDF,
    BaseSentiment,
    RuleBasedSentiment,
    LDASentiment,
    BehavioralSentiment,
    behavioral_analyze
)
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

# -----------------------
# Operator / Logger (if any)
# -----------------------
# from .operator import ...
from .logging.logger import get_logger, log_user_event  
__all__ = [
    # QnA
    "load_questions",
    "Judger",
    "BasePreprocessor",
    "Tokenizer",
    "Stemmer",
    "Lemmatizer",
    "BagOfWords",
    "TFIDF",
    "BaseSentiment",
    "RuleBasedSentiment",
    "LDASentiment",
    "BehavioralSentiment",
    "behavioral_analyze",
    "DecisionEngine",

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
] 