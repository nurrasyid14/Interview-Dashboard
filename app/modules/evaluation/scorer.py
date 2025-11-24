# app/modules/evaluation/scorer.py
"""
Converts textual answers into numerical scores using Text Mining engine.
"""
from typing import Dict
from ..QnA.text_mining import behavioral_analyze

class Scorer:
    """
    Compute per-question scores for a single answer.
    """

    def __init__(self):
        pass

    def score_answer(self, answer: str) -> Dict[str, float]:
        """
        Returns per-axis scores and overall sentiment in [-1, 1]
        """
        result = behavioral_analyze(answer)
        return result

    def overall_score(self, axis_scores: Dict[str, float]) -> float:
        """
        Computes a single combined score (average of axes)
        """
        axes = [v for k,v in axis_scores.items() if k != "overall"]
        if not axes:
            return 0.0
        return round(sum(axes)/len(axes), 4)
