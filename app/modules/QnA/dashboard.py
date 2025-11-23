# app/modules/QnA/dashboard.py

from pathlib import Path
import pandas as pd
from collections import Counter

from .text_mining import Tokenizer, Stemmer, Lemmatizer, BehavioralSentiment
from ..io_manager.storage_paths import REPORTS_DIR


class DashboardBuilder:
    """
    Builds analytical summary from a user's CSV interview file.

    Extracts:
    - identity
    - relevance scores (0-1)
    - sentiment (-1 to 1)
    - overall score
    - most weighted words (top 3)
    - most frequent words (top 3)
    - bar-chart ready scores
    """

    def __init__(self, user_id: str, use_stem=False, use_lemma=True):
        self.user_id = user_id
        self.file_path = Path(REPORTS_DIR) / f"{user_id}.csv"

        # Preprocessors
        self.tokenizer = Tokenizer()
        self.stemmer = Stemmer() if use_stem else None
        self.lemmatizer = Lemmatizer() if use_lemma else None
        self.behavior = BehavioralSentiment()

    # -------------------------------
    # CSV READER
    # -------------------------------
    def load(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path)
        return df

    # -------------------------------
    # TOKEN PIPELINE
    # -------------------------------
    def preprocess(self, text: str):
        tokens = self.tokenizer.process(text)
        if self.stemmer:
            tokens = self.stemmer.process(" ".join(tokens))
        if self.lemmatizer:
            tokens = self.lemmatizer.process(" ".join(tokens))
        return tokens

    # -------------------------------
    # BUILD DASHBOARD
    # -------------------------------
    def build(self) -> dict:
        df = self.load()

        # Extract identity (stored in first column "ID" row 2 = answer)
        identity = df["ID"][2] if "ID" in df.columns else self.user_id

        # Collect question scores (row index 3)
        score_row = df.iloc[3, :]  # row 3 is scores

        # Remove FINAL and Wage_Expectation scores
        clean_scores = score_row[
            ~score_row.index.isin(["FINAL", "Wage_Expectation"])
        ].astype(float).tolist()

        # Relevance score (average of Q1..Q16)
        relevance_score = sum(clean_scores[:16]) / 16 if clean_scores else 0.0

        # Sentiment = average of row-3 scores (since each is already [-1..1])
        sentiment_score = relevance_score * 2 - 1  # reverse mapping if needed

        # Overall (same formula as decision engine)
        overall_score = (relevance_score + (sentiment_score+1)/2) / 2

        # -------------------------------
        # MOST FREQUENT WORDS
        # -------------------------------
        answers = df.iloc[2, :].astype(str).tolist()  # row 2 = answers
        all_tokens = []
        for ans in answers:
            all_tokens.extend(self.preprocess(ans))

        freq = Counter(all_tokens)
        most_frequent = freq.most_common(3)

        # -------------------------------
        # MOST WEIGHTED WORDS using BehavioralSentiment axes
        # -------------------------------
        axis_scores = {}
        for word in all_tokens:
            axes = self.behavior.score_axes([word])
            axis_scores[word] = sum(axes.values())

        weighted_sorted = sorted(axis_scores.items(), key=lambda x: x[1], reverse=True)
        most_weighted = weighted_sorted[:3]

        # -------------------------------
        # BAR CHART DATA
        # -------------------------------
        bar_data = {
            "labels": list(df.columns),
            "scores": score_row.astype(float).tolist(),
            "threshold": 0.8
        }

        # -------------------------------
        # FINAL OUTPUT DICT
        # -------------------------------
        return {
            "identity": identity,
            "relevance_score": round(relevance_score, 4),
            "sentiment_score": round(sentiment_score, 4),
            "overall_score": round(overall_score, 4),
            "most_frequent_words": most_frequent,
            "most_weighted_words": most_weighted,
            "bar_chart": bar_data
        }
