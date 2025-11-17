#tf_idf.py

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List
nltk.download('punkt_tab', quiet=True)

class TFIDF:
    """
    Object-Oriented TF-IDF Vectorizer.
    Converts documents into TF-IDF weighted feature representations.
    """

    def __init__(self, tokenizer=None, max_features=5000):
        self.vectorizer = TfidfVectorizer(
            tokenizer=tokenizer or nltk.word_tokenize,
            max_features=max_features
        )

    def fit(self, documents: List[str]):
        self.vectorizer.fit(documents)
        return self

    def transform(self, documents: List[str]):
        return self.vectorizer.transform(documents)

    def fit_transform(self, documents: List[str]):
        return self.vectorizer.fit_transform(documents)

    def get_feature_names(self):
        return self.vectorizer.get_feature_names_out()

__all__ = ['TFIDF']