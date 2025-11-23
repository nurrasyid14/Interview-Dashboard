# app/modules/QnA/judger.py
"""
Judger module orchestrates:
- question sequencing
- text-mining scoring
- decision engine evaluation
- CSV report writing (incremental)
"""

from typing import List, Dict
from pathlib import Path
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

    CSV layout per column (vertical):
      Row 0: Label (L1, L2, Q1..Q16, Wage_Expectation, FINAL)
      Row 1: Question text
      Row 2: Answer text
      Row 3: Score (float)
    """

    def __init__(
        self,
        user_id: str,
        company_budget: int,
        use_stem: bool = False,
        use_lemma: bool = True,
    ):
        self.user_id = user_id
        # REPORTS_DIR is a Path (from storage_paths.py)
        self.file_path = Path(REPORTS_DIR) / f"{user_id}.csv"
        self.company_budget = company_budget
        self.questions = load_questions()  # dict with keys leveling/beginner/...
        self.collected_answers: List[str] = []
        self.scores: List[float] = []
        self.use_stem = use_stem
        self.use_lemma = use_lemma

        # internal counter for columns added (0-based)
        self._col_counter = 0

        # Initialize preprocessors
        self.tokenizer = Tokenizer()
        self.stemmer = Stemmer() if self.use_stem else None
        self.lemmatizer = Lemmatizer() if self.use_lemma else None
        self.behavior_engine = BehavioralSentiment()

        # Ensure reports directory and base CSV exist (we will append columns later)
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
    def _compute_sentiment_score(self, answer: str) -> float:
        """
        Returns sentiment score in range [-1, 1], as the BehavioralSentiment
        engine produces. We'll store it as-is in row 3 and also use it later.
        """
        try:
            tokens = self._preprocess_tokens(answer)
            axes = self.behavior_engine.score_axes(tokens)
            sentiment_score = round(sum(axes.values()) / 4, 4)
            return sentiment_score
        except Exception as e:
            return 0.0

    # -------------------------------------------------------------------
    def _next_label(self) -> str:
        """
        Decide label for the next column based on internal counter and leveling size.
        Labels:
          L1, L2, Q1..Q16, Wage_Expectation
        """
        leveling = self.questions.get("leveling", [])
        leveling_len = len(leveling)
        # If still in leveling questions
        if self._col_counter < leveling_len:
            return f"L{self._col_counter + 1}"
        # After leveling, map following columns to Q1..Q16 etc.
        q_index = self._col_counter - leveling_len + 1
        # If we exceed 16, we may be writing wage or extra columns
        if q_index <= 16:
            return f"Q{q_index}"
        # Otherwise it's wage or extras; name Wage_Expectation explicitly
        return "Wage_Expectation"

    # -------------------------------------------------------------------
    def process_answer(self, question: str, answer: str) -> float:
        """
        Process one QnA pair:
          - compute sentiment score
          - append a column with 4 rows: [Label, Question, Answer, Score]
          - increment counters and store locally
        Returns the sentiment score (float).
        """
        try:
            # compute sentiment
            sentiment_score = self._compute_sentiment_score(answer)

            # store sequential scores and answers
            self.scores.append(sentiment_score)
            self.collected_answers.append(answer)

            # determine label for this column (L1/L2/Q1..)
            label = self._next_label()

            # Ensure rows length == 4: [label, question, answer, score]
            rows = [label, question or "", answer or "", float(sentiment_score)]

            # Append column (csvio.append_column pads/truncates as needed)
            append_column(self.file_path, col_name=label if label else f"Col{self._col_counter+1}", rows=rows)

            # increment internal counter
            self._col_counter += 1

            return float(sentiment_score)
        except Exception as e:
            import traceback
            print(f"Error in process_answer: {e}")
            traceback.print_exc()
            return 0.0

    # -------------------------------------------------------------------
    def append_wage_and_finalize_column(self, wage_expectation: int):
        """
        Append the wage expectation as its own column following the Q columns.
        This will write a column with label 'Wage_Expectation', question as the wage prompt,
        answer as the numeric wage, and score as 0.0 (or you may choose another scheme).
        """
        wage_q = self.questions.get("wage", ["Berapa ekspektasi gaji Anda? (angka)"])[0]
        label = "Wage_Expectation"
        rows = [label, wage_q, str(wage_expectation), 0.0]
        append_column(self.file_path, col_name=label, rows=rows)
        self._col_counter += 1
        # also store into metadata lists for completeness
        self.collected_answers.append(str(wage_expectation))
        self.scores.append(0.0)

    # -------------------------------------------------------------------
    def finalize(self, months_experience: int, wage_expectation: int) -> Dict:
        """
        Triggered after all questions (16 + wage) are answered.
        Computes final decision using DecisionEngine and appends a FINAL column
        with a stringified summary.

        Returns the final_report dict.
        """
        try:
            # make sure wage column exists in CSV
            self.append_wage_and_finalize_column(wage_expectation)

            engine = DecisionEngine(self.company_budget)

            avg_sentiment = sum(self.scores[:16]) / len(self.scores[:16]) if len(self.scores) >= 16 else (sum(self.scores) / len(self.scores) if self.scores else 0.0)

            # Use only first 16 question sentiment scores for decision (per design)
            question_scores = [float(x) for x in (self.scores[:16] if len(self.scores) >= 16 else self.scores)]

            final_report = engine.judge(
                question_scores=question_scores,
                sentiment=avg_sentiment,
                months_experience=months_experience,
                wage_expectation=wage_expectation,
            )

            # append a FINAL column with the summary string (rows padded to 4)
            append_column(self.file_path, col_name="FINAL", rows=["FINAL", "Summary", str(final_report), 0.0])

            return final_report
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "error": str(e),
                "label": "Error",
                "final_score": 0.0
            }

InterviewJudger = Judger
