# app/modules/QnA/text_mining.py
"""
Full Text Mining Engine for the QnA module (enhanced with NLTK + sklearn).

Includes:
1. Preprocessing Polymorphism
   - BasePreprocessor
   - Tokenizer
   - Stemmer
   - Lemmatizer
   - BagOfWords
   - TFIDF

2. Sentiment Polymorphism
   - BaseSentiment
   - BehavioralSentiment (axis-based scoring)
   - LDASentiment (placeholder)
   - RuleBasedSentiment (simple +/- word list)

3. High-level API:
   - behavioral_analyze(text)
"""

from typing import List, Dict
from collections import Counter
import re

# NLP imports
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)


# ================================================================
# 1. PREPROCESSING POLYMORPHISM
# ================================================================

class BasePreprocessor:
    """Superclass defining the interface."""
    def process(self, text: str):
        raise NotImplementedError


class Tokenizer(BasePreprocessor):
    """NLTK tokenizer."""
    def process(self, text: str) -> List[str]:
        text = text.lower()
        tokens = word_tokenize(text)
        # remove punctuation tokens
        tokens = [t for t in tokens if t.isalnum()]
        return tokens


class Stemmer(BasePreprocessor):
    """NLTK Porter stemmer."""
    def __init__(self):
        self.stemmer = PorterStemmer()

    def process(self, text: str) -> List[str]:
        tokens = Tokenizer().process(text)
        return [self.stemmer.stem(t) for t in tokens]


class Lemmatizer(BasePreprocessor):
    """NLTK WordNet lemmatizer."""
    def __init__(self):
        self.lemma = WordNetLemmatizer()

    def process(self, text: str) -> List[str]:
        tokens = Tokenizer().process(text)
        return [self.lemma.lemmatize(t) for t in tokens]


class BagOfWords(BasePreprocessor):
    """Return token counts (dictionary)."""
    def process(self, text: str) -> Dict[str, int]:
        tokens = Tokenizer().process(text)
        return dict(Counter(tokens))


class TFIDF(BasePreprocessor):
    """Lightweight TF-IDF using sklearn (single doc)."""
    def process(self, text: str) -> Dict[str, float]:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        return dict(zip(feature_names, scores))


# ================================================================
# 2. SENTIMENT POLYMORPHISM
# ================================================================

class BaseSentiment:
    """Interface for a sentiment module."""
    def score(self, text: str) -> float:
        raise NotImplementedError


class RuleBasedSentiment(BaseSentiment):
    """Generic +/- lexicon sentiment."""
    POS = {"good", "great", "excellent", "positive", "improve", "support"}
    NEG = {"bad", "poor", "worse", "negative", "fail", "issue"}

    def score(self, text: str) -> float:
        tokens = Tokenizer().process(text)
        pos = sum(1 for t in tokens if t in self.POS)
        neg = sum(1 for t in tokens if t in self.NEG)
        if pos == neg == 0:
            return 0.0
        return (pos - neg) / (pos + neg + 1)


class LDASentiment(BaseSentiment):
    """Placeholder for future LDA-based scoring."""
    def score(self, text: str) -> float:
        return 0.0


# ================================================================
# 3. BEHAVIORAL SENTIMENT (AXIS MODEL)
# ================================================================

_DETERMINATION_POS = {
    "dedicated", "persistent", "determined", "motivated",
    "driven", "resilient", "committed", "persevere", "ambitious"
}
_DETERMINATION_NEG = {"unmotivated", "give up", "quit", "apathetic", "indifferent", "disengaged"}

_WILLINGNESS_POS = {
    "willing", "eager", "enthusiastic", "open", "cooperative",
    "adaptable", "flexible", "proactive"
}
_WILLINGNESS_NEG = {"unwilling", "reluctant", "resistant", "hesitant", "avoid", "averse"}

_RELIABILITY_POS = {
    "punctual", "consistent", "dependable", "responsible",
    "organized", "reliable", "steady", "trustworthy"
}
_RELIABILITY_NEG = {"late", "inconsistent", "unreliable", "irresponsible", "careless", "erratic"}

_HONESTY_POS = {"honest", "transparent", "truthful", "sincere", "straightforward", "upfront", "trustworthy"}
_HONESTY_NEG = {"dishonest", "untruthful", "deceptive", "evasive", "misleading", "conceal"}


def _axis_score(tokens: List[str], pos: set, neg: set) -> float:
    pos_c = sum(1 for t in tokens if t in pos)
    neg_c = sum(1 for t in tokens if t in neg)
    if pos_c == neg_c == 0:
        return 0.0
    return max(-1, min(1, (pos_c - neg_c) / (pos_c + neg_c + 1)))


class BehavioralSentiment(BaseSentiment):
    """Axis-based behavioral sentiment."""

    def score_axes(self, tokens: List[str]) -> Dict[str, float]:
        det = _axis_score(tokens, _DETERMINATION_POS, _DETERMINATION_NEG)
        will = _axis_score(tokens, _WILLINGNESS_POS, _WILLINGNESS_NEG)
        rel = _axis_score(tokens, _RELIABILITY_POS, _RELIABILITY_NEG)
        hon = _axis_score(tokens, _HONESTY_POS, _HONESTY_NEG)
        return {
            "determination": round(det, 4),
            "willingness": round(will, 4),
            "reliability": round(rel, 4),
            "honesty": round(hon, 4),
        }

    def score(self, text: str) -> float:
        tokens = Tokenizer().process(text)
        axes = self.score_axes(tokens)
        return round(sum(axes.values()) / 4, 4)


# ================================================================
# 4. HIGH LEVEL API
# ================================================================

def behavioral_analyze(text: str) -> Dict[str, float]:
    """Returns per-axis + overall sentiment."""
    engine = BehavioralSentiment()
    tokens = Tokenizer().process(text)
    scores = engine.score_axes(tokens)
    scores["overall"] = round(sum(scores.values()) / 4, 4)
    return scores
