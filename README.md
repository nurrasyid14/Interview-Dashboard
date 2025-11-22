# **Text Mining : AI Interview Evaluation System**
---
## **Overview**
xx
---
## **Ekspektasi Output**
xx
---
## **Blok Program**
### **1. Auth**
xx
### **2. QnA & Judger**
xx
### **3. Evaluator & Reporter**
xx
### **4. Dashboard Builder -- Interface Block**
xx
---

---
## **Arsitektur Program**
``` log
app/
├── data/                          # Stored JSON/CSV/parquet outputs for all users, logs, and analysis artifacts
│
├── modules/
│   ├── auth/
│   │   ├── login.py               # Handles user authentication, sessions, tokens
│   │   ├── metadata_filler.py     # Processes form inputs, validates metadata (name, age, job, username)
│   │   └── table_templater.py     # Generates JSON templates for user profile based on metadata
│   │
│   ├── QnA/
│   │   ├── questions.py           # Question bank for 18-item questionnaire (text + metadata)
│   │   ├── text.py                # NLP engine: preprocessing, LDA topics, sentiment/semantic models
│   │   └── decision.py            # Computes acceptance decisions based on clarity/semantic/relevance scores
│   │
│   ├── evaluation/
│   │   ├── scorer.py              # Converts questionnaire answers into numerical scores (0–1)
│   │   ├── analyser.py            # Text mining: clarity scoring, semantic similarity, relevance, frequent words
│   │   └── aggregator.py          # Merges metadata + scores + text mining into final dashboard CSV
│   │
│   ├── utils/
│   │   ├── idgen.py               # Generates user IDs: ord(m,n,r)<timestamp><counter>
│   │   ├── validators.py          # Username rules, age ≥ 18 check, field validation schemas (e.g., Pydantic)
│   │   └── pipeline.py            # Provides PipelineBlock base class + orchestrates multi-stage execution
│   │
│   ├── io_manager/
│   │   ├── jsonio.py              # Saves/loads metadata & questionnaire JSON files
│   │   ├── csvio.py               # Writes/reads scoring, analysis, and dashboard CSV files
│   │   └── storage_paths.py       # Standardizes file paths for all components (auth, QnA, analysis)
│   │
│   ├── logging/
│   │   └── logger.py              # Central logging utility: pipeline logs, user logs, error tracking
│   │
│   └── __init__.py                # Marks modules folder as a Python package
│
└── README.md                      # High-level documentation for backend structure and workflow
```
---