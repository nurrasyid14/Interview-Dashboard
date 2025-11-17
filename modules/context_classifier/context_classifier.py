# context_classifier/context_classifier.py
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from typing import List, Dict, Any, Optional
import joblib

class ContextClassifier:
    """
    Classifies the contextual domain of interview Q&A text.
    It identifies which category or skill area each text belongs to.
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        categories: Optional[List[str]] = None,
        random_state: int = 42,
    ):
        self.random_state = random_state
        self.categories = categories or [
            "technical_skills",
            "communication",
            "leadership",
            "problem_solving",
            "ethics",
            "self_reflection",
        ]

        # Default pipeline: TF-IDF + Logistic Regression
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=5000, stop_words="english")),
            ("clf", LogisticRegression(max_iter=200, random_state=self.random_state)),
        ])

        self.is_trained = False

        # Optionally load pre-trained model
        if model_path:
            self.load_model(model_path)

    # -------------------------------------------------------
    # Core Training
    # -------------------------------------------------------
    def train(self, texts: List[str], labels: List[str], test_size: float = 0.2):
        """Train the context classifier."""
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=self.random_state, stratify=labels
        )

        self.pipeline.fit(X_train, y_train)
        self.is_trained = True

        preds = self.pipeline.predict(X_test)
        report = classification_report(y_test, preds, output_dict=True)
        return report

    # -------------------------------------------------------
    # Inference
    # -------------------------------------------------------
    def predict(self, text: str) -> Dict[str, Any]:
        """Predict the most likely context for a single text."""
        if not self.is_trained:
            raise RuntimeError("Model is not trained or loaded.")
        label = self.pipeline.predict([text])[0]
        proba = (
            self.pipeline.predict_proba([text])[0]
            if hasattr(self.pipeline, "predict_proba")
            else None
        )
        return {"context": label, "probabilities": dict(zip(self.categories, proba)) if proba is not None else None}

    def predict_batch(self, texts: List[str]) -> pd.DataFrame:
        """Batch classify multiple interview utterances."""
        results = [self.predict(t) for t in texts]
        return pd.DataFrame(results)

    # -------------------------------------------------------
    # Persistence
    # -------------------------------------------------------
    def save_model(self, path: str):
        """Save trained pipeline."""
        if not self.is_trained:
            raise RuntimeError("Model must be trained before saving.")
        joblib.dump({
            "pipeline": self.pipeline,
            "categories": self.categories,
        }, path)

    def load_model(self, path: str):
        """Load pre-trained classifier."""
        saved = joblib.load(path)
        self.pipeline = saved["pipeline"]
        self.categories = saved.get("categories", self.categories)
        self.is_trained = True

    # -------------------------------------------------------
    # Utility
    # -------------------------------------------------------
    def explain_prediction(self, text: str, top_k: int = 5) -> Dict[str, float]:
        """
        Explain which terms influenced the classification most (using feature weights).
        Requires linear classifier (LogisticRegression).
        """
        if not self.is_trained:
            raise RuntimeError("Train or load model before explaining predictions.")
        vectorizer = self.pipeline.named_steps["tfidf"]
        clf = self.pipeline.named_steps["clf"]

        feature_names = np.array(vectorizer.get_feature_names_out())
        vector = vectorizer.transform([text])
        label = clf.predict([text])[0]
        label_index = list(clf.classes_).index(label)
        coefs = clf.coef_[label_index]
        top_indices = np.argsort(vector.toarray()[0] * coefs)[::-1][:top_k]
        top_terms = {feature_names[i]: round(coefs[i], 4) for i in top_indices}
        return {"predicted_context": label, "top_terms": top_terms}
