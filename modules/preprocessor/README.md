# 🧹 Preprocessor Module

Part of the AI Interviewer backend pipeline.
Handles data ingestion, cleaning, and linguistic feature preparation from raw speech or text.

## 📦 Overview

The Preprocessor is responsible for converting raw, multilingual audio and textual input from interview sessions into clean, structured, and analyzable data.
It forms the foundation for downstream processes like feature extraction, sentiment analysis, and decision modeling.

This module is composed of three key blocks:
```
preprocessor/
│
├── ingestion/          # Handles data input, transcription, and translation
├── text_cleaning/      # Normalization, tokenization, stopword removal, etc.
└── linguistics/        # Lemmatization, stemming, and POS tagging
```
## 🧩 Submodules
### 1. Ingestion

Handles all raw input sources — including audio, text, and multilingual data streams.

Components:

input_handler.py → Manages incoming data from APIs, forms, or chat pipelines.

audio_transcriber.py → Converts .wav, .mp3, or live audio into text using speech_recognition.

translator.py → Auto-translates non-English input into the project’s target analysis language via supported translation APIs.

### 2. Text Cleaning

Cleans and normalizes text before linguistic and ML processing.

Components:

normalizer.py → Lowercasing, punctuation removal, symbol cleanup.

tokenizer.py → Sentence/word-level tokenization using nltk or spaCy.

stopwords_remover.py → Removes irrelevant tokens.

🧠 Tip: This stage ensures that the AI model focuses only on meaningful linguistic signals rather than noise.

### 3. Linguistics

Adds higher-level NLP structure for feature extraction.

Components:

lemma_stem.py → Performs stemming and lemmatization.

tagger.py → Part-of-speech tagging for syntactic context and feature engineering.

## 🧠 Processing Flow
Audio/Text Input
     ↓
Ingestion → Translation
     ↓
Text Cleaning → Tokenization → Stopword Removal
     ↓
Linguistics → Lemmatization → Tagging
     ↓
Feature Extraction (next block)


Each stage outputs standardized, language-agnostic text vectors ready for feature engineering and learning models.

## 🧰 Requirements
```
nltk
spacy
scikit-learn
speechrecognition
pydub
numpy
```

## 🗣️ For multilingual support, install the spaCy model(s) you need:
```
python -m spacy download en_core_web_md
python -m spacy download id_core_news_md
python -m spacy download xx_ent_wiki_sm
```
## ⚙️ Usage Example
``` py
from preprocessor.ingestion.audio_transcriber import AudioTranscriber
from preprocessor.text_cleaning.normalizer import TextNormalizer
from preprocessor.linguistics.lemma_stem import LemmaStemmer


# 1️⃣ Transcribe audio
# transcriber = AudioTranscriber()
# text = transcriber.transcribe("input/interview_sample.wav")

# 2️⃣ Normalize
normalizer = TextNormalizer()
clean_text = normalizer.clean(text)

# 3️⃣ Lemmatize
lemmatizer = LemmaStemmer(lang="en")
processed = lemmatizer.process(clean_text)

print(processed)
```

## 🧩 Integration Notes

This module feeds into:

feature_extracting/ → to build text vectors (TF-IDF, embeddings, etc.)

subset_selection/ → for cross-validation

ensemble_learning/ → for decision modeling

visualizer/ → for output dashboards
