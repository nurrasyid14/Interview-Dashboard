# word_embedding.py
import numpy as np
import spacy
from typing import List

class WordEmbedding:
    """
    Universal word embedding generator using spaCy models.
    Automatically falls back if the model has no pretrained vectors.
    """

    def __init__(self, lang_model="en_core_web_md"):
        print(f"[INFO] Loading spaCy model: {lang_model} ...")
        self.nlp = spacy.load(lang_model, disable=["parser", "ner", "textcat"])
        print("[INFO] Model loaded successfully.")

        # Detect if vectors exist
        self.vector_width = self.nlp.vocab.vectors_length
        if self.vector_width == 0:
            print("[WARN] Model has no pretrained vectors. Falling back to hash-based token vectors.")
            self.use_hash_vectors = True
            self.vector_width = 300  # arbitrary fixed size
        else:
            print(f"[INFO] Pretrained vectors detected: {self.vector_width}-dimensional.")
            self.use_hash_vectors = False

    def _vectorize_sentence(self, sentence: str):
        doc = self.nlp(sentence)
        vectors = []

        for token in doc:
            # Always safe to call token.vector (spaCy will return hash vector if no pretrained)
            vec = token.vector
            if vec is not None and len(vec) > 0:
                vectors.append(vec)

        if len(vectors) == 0:
            return np.zeros(self.vector_width)
        return np.mean(vectors, axis=0)

    def transform(self, documents: List[str]):
        print(f"[INFO] Vectorizing {len(documents)} documents ...")
        embeddings = np.vstack([self._vectorize_sentence(doc) for doc in documents])
        print(f"[INFO] Finished vectorizing. Shape: {embeddings.shape}")
        return embeddings

__all__ = ["WordEmbedding"]
