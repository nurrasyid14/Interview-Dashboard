# app/modules/QnA/text_mining.py
"""
Full Text Mining Engine for the QnA module.

Features:
1. Preprocessing Polymorphism:
   - BasePreprocessor
   - Tokenizer
   - Stemmer
   - Lemmatizer
   - BagOfWords
   - TFIDF

2. Sentiment Polymorphism:
   - BaseSentiment
   - RuleBasedSentiment
   - BehavioralSentiment (axis-based)
   - LDASentiment (placeholder)

3. Unified High-level API:
   - TextMiningPipeline.analyze_sentiment() → FLOAT
   - behavioral_analyze(text)
"""

from typing import List, Dict
from collections import Counter

# NLP imports
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


# ================================================================
# NLTK SAFE INITIALIZATION
# ================================================================
_use_nltk_tokenize = False

try:
    nltk.download("punkt_tab", quiet=True)
    from nltk.tokenize import word_tokenize
    _use_nltk_tokenize = True
except Exception:
    try:
        nltk.download("punkt", quiet=True)
        from nltk.tokenize import word_tokenize
        _use_nltk_tokenize = True
    except Exception:
        pass

try: nltk.download("wordnet", quiet=True)
except: pass

try: nltk.download("omw-1.4", quiet=True)
except: pass


# ================================================================
# 1. PREPROCESSING POLYMORPHISM
# ================================================================
class BasePreprocessor:
    def process(self, text: str):
        raise NotImplementedError


class Tokenizer(BasePreprocessor):
    """Tokenize using NLTK, fallback to simple split."""
    def process(self, text: str) -> List[str]:
        text = text.lower()

        if _use_nltk_tokenize:
            try:
                tokens = word_tokenize(text)
            except Exception:
                tokens = text.split()
        else:
            tokens = text.split()

        # Keep only alphanumeric tokens
        return [t for t in tokens if t.isalnum()]


class Stemmer(BasePreprocessor):
    def __init__(self):
        self.stem = PorterStemmer()

    def process(self, text: str) -> List[str]:
        return [self.stem.stem(t) for t in Tokenizer().process(text)]


class Lemmatizer(BasePreprocessor):
    def __init__(self):
        self.lemma = WordNetLemmatizer()

    def process(self, text: str) -> List[str]:
        return [self.lemma.lemmatize(t) for t in Tokenizer().process(text)]


class BagOfWords(BasePreprocessor):
    def process(self, text: str) -> Dict[str, int]:
        return dict(Counter(Tokenizer().process(text)))


class TFIDF(BasePreprocessor):
    """TF-IDF extractor for single document."""
    def process(self, text: str) -> Dict[str, float]:
        try:
            v = TfidfVectorizer()
            matrix = v.fit_transform([text])
            features = v.get_feature_names_out()
            values = matrix.toarray()[0]
            return dict(zip(features, values))
        except Exception:
            return BagOfWords().process(text)


# ================================================================
# 2. SENTIMENT POLYMORPHISM
# ================================================================
class BaseSentiment:
    def score(self, text: str) -> float:
        raise NotImplementedError


class RuleBasedSentiment(BaseSentiment):
    """Simple + / - lexicon model."""
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
    """Placeholder for future LDA model."""
    def score(self, text: str) -> float:
        return 0.0


# ================================================================
# 3. BEHAVIORAL SENTIMENT AXIS MODEL
# ================================================================
_DETERMINATION_POS = {
    "dedicated", "persistent", "determined", "motivated",
    "driven", "resilient", "committed", "persevere", "ambitious"
}
_DETERMINATION_NEG = {"unmotivated", "give", "quit", "apathetic", "indifferent", "disengaged"}

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

_HONESTY_POS = {"honest", "transparent", "truthful", "sincere", "straightforward", "upfront"}
_HONESTY_NEG = {"dishonest", "untruthful", "deceptive", "evasive", "misleading", "conceal"}


def _axis_score(tokens: List[str], pos: set, neg: set) -> float:
    pos_c = sum(t in pos for t in tokens)
    neg_c = sum(t in neg for t in tokens)

    if pos_c == neg_c == 0:
        return 0.0

    return max(-1, min(1, (pos_c - neg_c) / (pos_c + neg_c + 1)))


class BehavioralSentiment(BaseSentiment):
    """Personality axis-based scoring."""

    def score_axes(self, tokens: List[str]) -> Dict[str, float]:
        return {
            "determination": round(_axis_score(tokens, _DETERMINATION_POS, _DETERMINATION_NEG), 4),
            "willingness":   round(_axis_score(tokens, _WILLINGNESS_POS, _WILLINGNESS_NEG), 4),
            "reliability":   round(_axis_score(tokens, _RELIABILITY_POS, _RELIABILITY_NEG), 4),
            "honesty":       round(_axis_score(tokens, _HONESTY_POS, _HONESTY_NEG), 4),
        }

    def score(self, text: str) -> float:
        tokens = Tokenizer().process(text)
        axes = self.score_axes(tokens)
        return round(sum(axes.values()) / 4, 4)


# ================================================================
# 4. TEXT MINING PIPELINE (FIXED FOR TEST SUITE)
# ================================================================
class TextMiningPipeline:
    """
    Preprocess → extract features → sentiment score
    Expected by test suite:
        analyze_sentiment(text) → returns FLOAT
    """

    def __init__(self, preprocessor=None, feature_extractor=None, sentiment_engine=None):
        self.preprocessor = preprocessor or Tokenizer()
        self.feature_extractor = feature_extractor or TFIDF()
        self.sentiment_engine = sentiment_engine or RuleBasedSentiment()

    def preprocess(self, text: str) -> List[str]:
        return self.preprocessor.process(text)

    def extract_features(self, text: str):
        try:
            return self.feature_extractor.process(text)
        except Exception:
            return BagOfWords().process(text)

    def analyze_sentiment(self, text: str) -> float:
        """
        Must return FLOAT (test suite requirement).
        """
        # Preprocess & feature extraction (for pipeline completeness)
        _ = self.preprocess(text)
        _ = self.extract_features(text)

        # Sentiment always returned as float
        score = self.sentiment_engine.score(text)
        return float(score)


# ================================================================
# 5. HIGH LEVEL BEHAVIORAL API
# ================================================================
def behavioral_analyze(text: str) -> Dict[str, float]:
    tokens = Tokenizer().process(text)
    engine = BehavioralSentiment()
    axes = engine.score_axes(tokens)
    axes["overall"] = round(sum(axes.values()) / 4, 4)
    return axes
