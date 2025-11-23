# AI Job Interview Evaluation System - Setup & Run Guide

## Overview
This is a Streamlit-based AI interview system that:
1. Authenticates candidates
2. Collects professional background (Identity)
3. Conducts adaptive interviews (2-level leveling + 16 difficulty-matched questions)
4. Scores candidates using NLP sentiment analysis (Behavioral axes: Determination, Willingness, Reliability, Honesty)
5. Generates hiring recommendations based on configurable thresholds
6. Provides analytics dashboard

## Prerequisites
- Python 3.9+
- pip

## Installation

### 1. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Download NLTK Data (automatic on first run, but can pre-download)
\`\`\`bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('wordnet'); nltk.download('omw-1.4')"
\`\`\`

## Running the Application

### Start Streamlit
\`\`\`bash
streamlit run main.py
\`\`\`

The app will open at `http://localhost:8501`

## Test Credentials

### Option 1: Create New Account
1. Go to **Login** page
2. Click **Signup** tab
3. Use credentials:
   - Username: `dev.premium1`
   - Password: `DevTest@2024`
   - Full Name: `Test User` (optional)

### Option 2: Pre-created Account
If you've already created an account, use those credentials.

## Application Flow

### 1. Login / Signup Page
- Create new account or login with existing credentials
- Username: lowercase, letters + digits + dots/underscores
- Password: 8+ chars, uppercase + lowercase + digit + special char

### 2. Identity Page
- Fill professional profile:
  - Full Name
  - Birthdate (dd-mm-yyyy, must be 18+)
  - Months of experience
  - Address
  - Position (dropdown)
  - Specialties (multiselect)

### 3. Interview Page
- **Leveling Questions (2):** Determine difficulty level based on experience
- **Main Questions (16):** Difficulty-matched based on months of experience
  - < 12 months → Beginner
  - 12-18 months → Intermediate
  - > 18 months → Advanced
- **Wage Expectation:** Final salary expectation

### 4. Result Page
- View final scoring and recommendation:
  - **Layak** (Suitable): Score ≥ 0.80
  - **Dipertimbangkan** (Consider): 0.60 ≤ Score < 0.80
  - **Tidak Layak** (Not Suitable): Score < 0.60

### 5. Dashboard Page
- Analytics on interview performance:
  - Relevance score (average of 16 main questions)
  - Sentiment score
  - Most frequent words
  - Most weighted words (by behavioral axes)
  - Bar chart of all scores

## Data Storage

All data is stored locally in:
\`\`\`
app/data/
├── users/           # User credentials & metadata (JSON)
├── reports/         # Interview results (CSV per user)
└── temp/counters/   # Internal ID generation counters
\`\`\`

## Password Requirements

- Minimum 8 characters
- Must contain: uppercase + lowercase + digit + special character
- Cannot contain username
- Example: `DevTest@2024`

## Username Requirements

- Lowercase only
- Can contain: letters, digits, dots (.), underscores (_)
- Must contain at least 1 letter
- Example: `dev.premium1`, `qa.test.user`

## Scoring Algorithm

### Per-Question Sentiment (Behavioral Axes)
Each answer is analyzed on 4 axes:
- **Determination:** Persistence, motivation, drive
- **Willingness:** Eagerness, flexibility, cooperation
- **Reliability:** Consistency, punctuality, dependability
- **Honesty:** Transparency, integrity, truthfulness

### Final Score Calculation
\`\`\`
base_score = (average_question_scores + normalized_sentiment) / 2
penalty = 0.05 if (wage_expectation / company_budget) >= φ (1.618)
final_score = max(0, base_score - penalty)
\`\`\`

## Troubleshooting

### Session State Errors
- Clear browser cache
- Restart Streamlit: `streamlit run main.py`
- Navigate through pages in order: Login → Identity → Interview → Result

### NLTK Data Errors
- Run: `python -c "import nltk; nltk.download('punkt_tab'); nltk.download('wordnet')"`
- Or restart app (automatic download on first run)

### CSV Not Found
- Dashboard only shows data after interview is completed
- Try refreshing the page

### File Permission Errors
- Ensure `app/data/` directory is writable
- Check file permissions in terminal

## Configuration

Edit thresholds in `/app/modules/QnA/decisions.py`:
\`\`\`python
PASS_THRESHOLD = 0.8       # Score for "Layak"
CONSIDER_THRESHOLD = 0.6   # Score for "Dipertimbangkan"
\`\`\`

## Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## Notes

- All data is stored locally on your machine
- No internet connection required after installation
- First run may take longer due to NLTK data downloads
- Interview sessions persist in Streamlit session state

---

**Ready to run!** Start with: `streamlit run main.py`
