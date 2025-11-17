# 🧠 Context Classifier

Detects the **semantic domain** of an interview Q&A text, enabling adaptive evaluation.

---

## 📦 Structure
```
context_classifier/
├── init.py
└── context_classifier.py
```
---

## ⚙️ Features
- TF-IDF + Logistic Regression baseline
- Easily swappable for BERT, RoBERTa, or DistilBERT embeddings
- Training, evaluation, saving, and loading
- Explainable term-level feature contribution

---

## 🧩 Example Usage
```python
from context_classifier import ContextClassifier

texts = [
    "I prefer to solve problems analytically before coding.",
    "I always communicate clearly in team meetings.",
    "I value integrity when handling user data."
]

labels = ["problem_solving", "communication", "ethics"]

clf = ContextClassifier()
report = clf.train(texts, labels)
print(report["accuracy"])

# Predict
print(clf.predict("How do you resolve conflicts in a team?"))
```

## 📤 Integration Points
Upstream: Receives interview Q&A text streams from the main controller.

Downstream: Feeds detected context to:

ensemble/ensemble_controller.py (to adapt model focus)

learning_evaluation/evaluation_pipeline.py (to correlate fairness across topics)

visualizer/ (for per-topic insights)

## 🔮 Future Expansion
Add transformer-based embeddings via sentence-transformers.

Integrate context memory for conversational flow.

Domain fine-tuning for specific job types.