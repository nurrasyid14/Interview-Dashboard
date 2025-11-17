# tokenizer.py

import spacy
from nltk.tokenize import word_tokenize
from typing import List, Literal

class Tokenizer:
    """
    Tokenizes raw text into words, using spaCy (preferred) or NLTK.
    """

    def __init__(self, lang_model: str = "en_core_web_sm", backend: Literal["spacy", "nltk"] = "spacy"):
        self.backend = backend
        if backend == "spacy":
            print(f"[INFO] Loading spaCy model: {lang_model} ...")
            self.nlp = spacy.load(lang_model, disable=["ner", "parser", "textcat"])
            print("[INFO] Model loaded successfully.")
        else:
            self.nlp = None

    def tokenize(self, text: str) -> List[str]:
        if self.backend == "spacy" and self.nlp:
            doc = self.nlp(text)
            return [token.text for token in doc if not token.is_space]
        else:
            return word_tokenize(text)

    def batch_tokenize(self, texts: List[str]) -> List[List[str]]:
        return [self.tokenize(t) for t in texts]
