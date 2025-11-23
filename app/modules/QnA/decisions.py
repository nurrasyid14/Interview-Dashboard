# app/modules/QnA/decisions.py
"""
Decision engine for job-application interview scoring.

Implements:
- Difficulty selection (based on working experience in months)
- Final suitability scoring
- Wage expectation penalty using golden ratio φ
"""

from typing import List, Dict
import math


PHI = (1 + 5 ** 0.5) / 2   # Golden ratio 1.618...
PASS_THRESHOLD = 0.8       # <--- Updated threshold
CONSIDER_THRESHOLD = 0.6   


class DecisionEngine:
    def __init__(self, company_budget: int):
        """
        company_budget : int
            Maximum wage the company can provide.
        """
        self.company_budget = company_budget

    # -------------------------------------------------------------------

    @staticmethod
    def determine_difficulty(months: int) -> str:
        """
        Map number of working months → difficulty level.
        """
        if months < 12:
            return "beginner"
        elif 12 <= months < 18:
            return "intermediate"
        return "advanced"

    # -------------------------------------------------------------------

    @staticmethod
    def compute_final_score(scores: List[float], sentiment: float) -> float:
        """
        Compute final suitability score (0–1).

        scores   : list of per-question scores (0–1)
        sentiment: overall sentiment from text mining (-1 to 1)
        """

        avg_scores = sum(scores) / len(scores)

        # map sentiment [-1,1] → [0,1]
        sent_component = (sentiment + 1) / 2

        # final score = average of relevance + sentiment
        final = (avg_scores + sent_component) / 2
        return round(final, 4)

    # -------------------------------------------------------------------

    def wage_penalty(self, expectation: int) -> float:
        """
        Return penalty value (0 or 0.05).
        Applied if expectation/company_budget ≥ φ
        """
        ratio = expectation / self.company_budget
        return 0.05 if ratio >= PHI else 0.0

    # -------------------------------------------------------------------

    def judge(
        self,
        question_scores: List[float],
        sentiment: float,
        months_experience: int,
        wage_expectation: int
    ) -> Dict[str, any]:
        """
        Main interface for scoring.
        """

        difficulty = self.determine_difficulty(months_experience)

        base_score = self.compute_final_score(question_scores, sentiment)

        penalty = self.wage_penalty(wage_expectation)

        final_score = max(0.0, base_score - penalty)

        # -------------------------
        # NEW LABEL LOGIC:
        # -------------------------
        if final_score >= PASS_THRESHOLD:
            label = "Layak"
        elif final_score >= CONSIDER_THRESHOLD:
            label = "Dipertimbangkan"
        else:
            label = "Tidak Layak"

        return {
            "difficulty": difficulty,
            "base_score": base_score,
            "penalty": penalty,
            "final_score": round(final_score, 4),
            "label": label,
            "threshold_used": PASS_THRESHOLD
        }

FinalDecisions = DecisionEngine
