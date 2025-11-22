# app/modules/evaluation/analyser.py

"""
Analyser module
---------------
Provides lightweight text analytics for dashboard:

- clarity scoring (length, stopwords, special chars)
- relevance scoring (keyword overlap)
- frequent words
- semantic similarity placeholder (Jaccard)
"""

from typing import List, Dict
from collections import Counter
import re

from ..QnA.text_mining import Tokenizer

# --------------------------
# Minimal stopword list
# --------------------------
STOPWORDS = {
    "dan", "yang", "di", "ke", "dari", "untuk", "pada", "dengan",
    "ini", "itu", "saya", "anda", "kami", "kita", "sebagai", "adalah",
    "oleh", "atau", "tetapi", "juga", "dalam", "tidak", "sebagai",
}


# ---------------------------------------------------------------------
# 1. Clarity Scoring
# ---------------------------------------------------------------------
def clarity_score(text: str) -> float:
    """
    Measures clarity based on:
    - token length (8–40 ideal)
    - stopword fraction
    - proportion of special characters

    Returns score ∈ [0, 1].
    """
    tokens = Tokenizer().process(text)
    n = len(tokens)
    if n == 0:
        return 0.0

    # Length score: linear between 8–40 tokens
    length_score = min(max((min(n, 40) - 8) / (40 - 8), 0), 1)

    # Stopword fraction penalty
    stop_frac = sum(1 for t in tokens if t in STOPWORDS) / n
    stop_penalty = 1 - stop_frac  # higher fraction reduces score

    # Special character penalty
    special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
    special_frac = special_chars / max(len(text), 1)
    special_penalty = 1 - special_frac  # more special chars reduces score

    # Combined score: weighted average
    score = 0.5 * length_score + 0.25 * stop_penalty + 0.25 * special_penalty
    return round(score, 4)

# ---------------------------------------------------------------------
# 2. Relevance Scoring
# ---------------------------------------------------------------------
def relevance_score(text: str, question: str) -> float:
    """
    Uses token overlap ratio between question and answer.
    Returns relevance ∈ [0, 1].
    """
    tok = set(Tokenizer().process(text))
    qtok = set(Tokenizer().process(question))
    if not tok or not qtok:
        return 0.0
    overlap = len(tok & qtok)
    base = len(qtok)
    return round(overlap / base, 4)

# ---------------------------------------------------------------------
# 3. Frequent Word Extraction
# ---------------------------------------------------------------------
def frequent_words(text: str, top_k=5, exclude_stopwords=True) -> Dict[str, int]:
    tokens = Tokenizer().process(text)
    if exclude_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]
    return dict(Counter(tokens).most_common(top_k))

# ---------------------------------------------------------------------
# 4. Semantic Similarity (Jaccard placeholder)
# ---------------------------------------------------------------------
def semantic_similarity(a: str, b: str) -> float:
    """
    Placeholder for semantic similarity.
    Jaccard(set(tokens)).
    Returns [0,1].
    """
    t1 = set(Tokenizer().process(a))
    t2 = set(Tokenizer().process(b))
    if not t1 or not t2:
        return 0.0
    score = len(t1 & t2) / len(t1 | t2)
    return round(score, 4)
