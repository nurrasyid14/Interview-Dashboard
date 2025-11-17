# pos_tagger.py

import spacy
from typing import List, Tuple

class POSTagger:
    """
    Perform POS tagging and dependency extraction.
    """

    def __init__(self, lang_model: str = "en_core_web_sm"):
        print(f"[INFO] Loading spaCy model: {lang_model} ...")
        self.nlp = spacy.load(lang_model, disable=["ner", "textcat"])
        print("[INFO] Model loaded successfully.")

    def tag(self, text: str) -> List[Tuple[str, str]]:
        """
        Returns a list of (token, POS tag).
        """
        doc = self.nlp(text)
        return [(token.text, token.pos_) for token in doc]

    def dependencies(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Returns a list of (token, head, dependency relation).
        """
        doc = self.nlp(text)
        return [(token.text, token.head.text, token.dep_) for token in doc]
