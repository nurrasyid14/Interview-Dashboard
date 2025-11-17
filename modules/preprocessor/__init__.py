"""
Preprocessor Package
--------------------
This package handles all data preprocessing steps required by the AI Interviewer pipeline.
It includes:
- Ingestion (input handling, transcription, translation)
- Text Cleaning (normalization, tokenization, stopword removal)
- Linguistics (lemmatization, stemming, tagging)
- Feature Extraction (BoW, TF-IDF, embeddings)
"""

# --- Ingestion ---
from .ingestion import (
    input_handler,
    audio_transcriber,
    translator
)

# --- Text Cleaning ---
from .text_cleaning import (
    normalizer,
    tokenizer,
    stopwords_remover
)

# --- Linguistics ---
from .linguistics import (
    LemmatizerStemmer, 
    POSTagger
)

# --- Feature Extracting ---
from .feature_extraction import (
    bag_of_words,
    tf_idf,
    word_embedding
)

__all__ = [
    # ingestion
    "input_handler",
    "audio_transcriber",
    "translator",
    # text cleaning
    "normalizer",
    "tokenizer",
    "stopwords_remover",
    # linguistics
    "lemmatizer",
    "stemmer",
    "tagger",
    # feature extracting
    "bag_of_words",
    "tf_idf",
    "word_embedding"
]

# --- Convenience printout for development/debugging ---
if __name__ == "__main__":
    print("[INFO] Preprocessor package initialized successfully.")
    print("Submodules available:")
    for name in __all__:
        print(f"  - {name}")
