# lemmatizer_stemmer.py

import spacy
from nltk.stem import PorterStemmer, SnowballStemmer
from typing import List, Literal

class LemmatizerStemmer:
    """
    Perform lemmatization and stemming for linguistic normalization.
    """

    def __init__(
        self,
        lang_model: str = "en_core_web_sm",
        stemmer: Literal["porter", "snowball", None] = "porter",
    ):
        print(f"[INFO] Loading spaCy model: {lang_model} ...")
        self.nlp = spacy.load(lang_model, disable=["ner", "parser", "textcat"])
        print("[INFO] Model loaded successfully.")

        if stemmer == "porter":
            self.stemmer = PorterStemmer()
        elif stemmer == "snowball":
            self.stemmer = SnowballStemmer("english")
        else:
            self.stemmer = None

    def lemmatize(self, text: str) -> List[str]:
        doc = self.nlp(text)
        return [token.lemma_ for token in doc]

    def stem(self, text: str) -> List[str]:
        tokens = [token.text for token in self.nlp(text)]
        if self.stemmer:
            return [self.stemmer.stem(token) for token in tokens]
        return tokens

    def process(self, text: str, do_lemmatize=True, do_stem=False) -> List[str]:
        """
        Unified method to perform lemmatization and/or stemming.
        """
        tokens = self.lemmatize(text) if do_lemmatize else [t.text for t in self.nlp(text)]
        if do_stem and self.stemmer:
            tokens = [self.stemmer.stem(t) for t in tokens]
        return tokens
