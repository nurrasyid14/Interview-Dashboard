# Dependency Explanation

## Core Dependencies

### streamlit>=1.28.0
- Web app framework for rapid prototyping
- Handles UI, session state, and routing

### pandas>=2.0.0
- Data manipulation and CSV I/O
- Used for report generation and dashboard analytics

### numpy>=1.24.0
- Numerical computing
- Used by pandas and sklearn

### python-dateutil>=2.8.0
- Date parsing and validation
- Used for birthdate validation (dd-mm-yyyy format)

### nltk>=3.8.0
- Natural Language Toolkit
- Provides:
  - Tokenization (word_tokenize)
  - Stemming (PorterStemmer)
  - Lemmatization (WordNetLemmatizer)

### scikit-learn>=1.3.0
- Machine learning library
- Used for TF-IDF vectorization in text mining

### scipy>=1.11.0
- Scientific computing
- Dependency for scikit-learn

### loguru>=0.7.0
- Logging library (ready for future enhancements)
- Better than standard logging

### pyyaml>=6.0
- YAML parsing (prepared for future config files)

## Installation

\`\`\`bash
pip install -r requirements.txt
\`\`\`

All versions are pinned for consistency.
