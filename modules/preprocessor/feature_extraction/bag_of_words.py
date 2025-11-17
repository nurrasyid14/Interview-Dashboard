#bag_of_words.py

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from typing import List
nltk.download('punkt_tab', quiet=True)

class BagOfWords:
    """
    Object-Oriented Bag of Words extractor.
    Converts text documents into a Document-Term Matrix using token counts.
    """

    def __init__(self, tokenizer=None):
        self.vectorizer = CountVectorizer(tokenizer=tokenizer or nltk.word_tokenize)

    def fit(self, documents: List[str]):
        self.vectorizer.fit(documents)
        return self

    def transform(self, documents: List[str]):
        return self.vectorizer.transform(documents)

    def fit_transform(self, documents: List[str]):
        return self.vectorizer.fit_transform(documents)

    def get_feature_names(self):
        return self.vectorizer.get_feature_names_out()

__all__ = ['BagOfWords']