# stopwords_remover.py

import nltk
from typing import List, Literal

nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

class StopwordsRemover:
    """
    Removes stopwords from text.
    """

    def __init__(self, lang: Literal["english", "indonesian"] = "english", extra_stopwords=None):
        self.stop_words = set(stopwords.words(lang))
        if extra_stopwords:
            self.stop_words.update(extra_stopwords)

    def remove(self, tokens: List[str]) -> List[str]:
        return [t for t in tokens if t.lower() not in self.stop_words]

    def batch_remove(self, tokenized_docs: List[List[str]]) -> List[List[str]]:
        return [self.remove(doc) for doc in tokenized_docs]
