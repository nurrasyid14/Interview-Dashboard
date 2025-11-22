"""
QnA module initializer.

Exposes:
- QuestionBank       : Source of all interview questions.
- Judger             : Main evaluator for scoring answers.

- Text-mining engine components:
    Preprocessors (Tokenize, Stem, Lemma, BoW, TFIDF)
    Sentiment engines (RuleBased, Behavioral, LDA)
    behavioral_analyze() convenience function
"""

from .questions import load_questions
from .judger import Judger
from .decisions import DecisionEngine

# Preprocessing polymorphism
from .text_mining import (
    BasePreprocessor,
    Tokenizer,
    Stemmer,
    Lemmatizer,
    BagOfWords,
    TFIDF,
)

# Sentiment polymorphism
from .text_mining import (
    BaseSentiment,
    RuleBasedSentiment,
    BehavioralSentiment,
    LDASentiment,
)

# High-level API
from .text_mining import behavioral_analyze

__all__ = [
    "load_questions",
    "Judger",
    "DecisionEngine",
    "BasePreprocessor",
    "Tokenizer",
    "Stemmer",
    "Lemmatizer",
    "BagOfWords",
    "TFIDF",
    "BaseSentiment",
    "RuleBasedSentiment",
    "BehavioralSentiment",
    "LDASentiment",
    "behavioral_analyze",
]