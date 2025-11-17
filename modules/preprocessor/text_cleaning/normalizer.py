# normalizer.py

import re
import unicodedata
from typing import List

class TextNormalizer:
    """
    Cleans and normalizes raw text for NLP tasks.
    """

    def __init__(self, lowercase: bool = True, remove_punct: bool = True, remove_numbers: bool = True):
        self.lowercase = lowercase
        self.remove_punct = remove_punct
        self.remove_numbers = remove_numbers

    def _remove_punctuation(self, text: str) -> str:
        return re.sub(r"[^\w\s]", "", text)

    def _remove_numbers(self, text: str) -> str:
        return re.sub(r"\d+", "", text)

    def _normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")

    def normalize(self, text: str) -> str:
        """
        Apply all configured normalization steps.
        """
        if self.lowercase:
            text = text.lower()
        text = re.sub(r"http\S+|www\S+|@\S+|#\S+", "", text)  # URLs, mentions, hashtags
        if self.remove_punct:
            text = self._remove_punctuation(text)
        if self.remove_numbers:
            text = self._remove_numbers(text)
        text = self._normalize_unicode(text)
        return re.sub(r"\s+", " ", text).strip()

    def batch_normalize(self, texts: List[str]) -> List[str]:
        return [self.normalize(t) for t in texts]
