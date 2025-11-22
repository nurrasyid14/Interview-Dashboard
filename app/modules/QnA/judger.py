# app/modules/QnA/judger.py
"""
Judger module orchestrates:
- question sequencing
- text-mining scoring
- decision engine evaluation
- CSV report writing (incremental)
"""

from typing import List, Dict
import csv
import os

from .questions import load_questions
from .text_mining import (
    BehavioralSentiment, Tokenizer, Stemmer, Lemmatizer, behavioral_analyze
)
from .decisions import DecisionEngine
from ..io_manager.csvio import ensure_csv, append_column
from ..io_manager.storage_paths import REPORTS_DIR


class Judger:
    """
    Manages the entire QnA pipeline for a single user.
    """

    def __init__(self, user_id: str, company_budget: int, use_stem: bool = False, use_lemma: bool = True):
        self.user_id = user_id
        self.file_path = os.path.join(REPORTS_DIR, f"{user_id}.csv")
        self.company_budget = company_budget
        self.questions = load_questions()
        self.collected_answers: List[str] = []
        self.scores: List[float] = []
        self.use_stem = use_stem
        self.use_lemma = use_lemma

        # Initialize preprocessors
        self.tokenizer = Tokenizer()
        self.stemmer = Stemmer() if self.use_stem else None
        self.lemmatizer = Lemmatizer() if self.use_lemma else None
        self.behavior_engine = BehavioralSentiment()

        ensure_csv(self.file_path, headers=["ID"])

    # -------------------------------------------------------------------

    def _preprocess_tokens(self, text: str) -> List[str]:
        tokens = self.tokenizer.process(text)
        if self.stemmer:
            tokens = self.stemmer.process(" ".join(tokens))
        if self.lemmatizer:
            tokens = self.lemmatizer.process(" ".join(tokens))
        return tokens

    # -------------------------------------------------------------------

    def process_answer(self, question: str, answer: str) -> float:
        """
        Process one QnA pair:
        - preprocess tokens (optional stem/lemma)
        - run behavioral sentiment
        - append to CSV
        """
        tokens = self._preprocess_tokens(answer)
        axes_scores = self.behavior_engine.score_axes(tokens)
        sentiment_score = round(sum(axes_scores.values()) / 4, 4)

        # store sequential scores
        self.scores.append(sentiment_score)
        self.collected_answers.append(answer)

        # append 3 rows for the column
        append_column(
            self.file_path,
            col_name=f"Q{len(self.scores)}",
            rows=[question, answer, sentiment_score]
        )

        return sentiment_score

    # -------------------------------------------------------------------

    def finalize(self, months_experience: int, wage_expectation: int) -> Dict:
        """
        Triggered after all questions (16 + wage) are answered.
        Computes:
        - final decision score
        - difficulty
        - penalty
        - suitability label
        """
        engine = DecisionEngine(self.company_budget)

        avg_sentiment = sum(self.scores) / len(self.scores) if self.scores else 0.0

        final_report = engine.judge(
            question_scores=self.scores[:16],  # first 16 are actual questions
            sentiment=avg_sentiment,
            months_experience=months_experience,
            wage_expectation=wage_expectation
        )

        # create a summary column
        append_column(
            self.file_path,
            col_name="FINAL",
            rows=[str(final_report)]
        )

        return final_report
