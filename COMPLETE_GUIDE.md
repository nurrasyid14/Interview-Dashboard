# AI Job Interview Evaluation System - Complete Setup & Testing Guide

## Quick Start (30 seconds)

\`\`\`bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run system verification
python scripts/quick_test.py

# 3. Start application
streamlit run main.py
\`\`\`

Then open: http://localhost:8501

---

## Full Installation Guide

### Step 1: Clone/Extract Project
\`\`\`bash
cd Interview-Dashboard
\`\`\`

### Step 2: Create Virtual Environment (Recommended)
\`\`\`bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
\`\`\`

### Step 3: Install All Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 4: Verify Installation
\`\`\`bash
python scripts/quick_test.py
\`\`\`

Expected output:
\`\`\`
============================================================
AI Interview System - Module Verification
============================================================

1. Testing imports...
   ✓ Auth module
   ✓ Validators module
   ✓ I/O manager module
   ✓ QnA module

2. Testing directories...
   ✓ Users directory: app/data/users
   ✓ Reports directory: app/data/reports

3. Testing validators...
   ✓ Username validation
   ✓ Password validation

4. Testing NLTK tokenization...
   ✓ Tokenization: [...]

5. Testing sentiment analysis...
   ✓ Behavioral analysis: {...}

6. Testing question bank...
   ✓ Leveling questions: 2
   ✓ Beginner questions: 16
   ✓ Intermediate questions: 16
   ✓ Advanced questions: 16

============================================================
ALL TESTS PASSED ✓
============================================================

You can now run: streamlit run main.py
\`\`\`

### Step 5: Run Application
\`\`\`bash
streamlit run main.py
\`\`\`

Or use convenience scripts:
\`\`\`bash
# macOS/Linux
bash scripts/run.sh

# Windows
scripts\run.bat
\`\`\`

---

## Test Scenario

### Scenario: Complete Interview Test

#### 1. Create Account
1. Open http://localhost:8501
2. Navigate to **Login** page
3. Click **Signup** tab
4. Enter credentials:
   - Username: `junior.dev2025`
   - Password: `JuniorDev@123`
   - Full Name: `Alex Johnson`
5. Click **Create account**

#### 2. Login
1. Click **Login** tab
2. Enter credentials:
   - Username: `junior.dev2025`
   - Password: `JuniorDev@123`
3. Click **Login**

#### 3. Fill Identity
1. Navigate to **Identity** page
2. Fill form:
   - Full Name: `Alex Johnson`
   - Birthdate: `15-03-1995` (aged 30)
   - Months of experience: `8`
   - Address: `123 Tech Street`
   - Position: `Chef` (or any option)
   - Specialties: Select any
3. Click **Save & Continue**

#### 4. Take Interview
1. Navigate to **Interview** page
2. **Leveling Questions (2):**
   - Q1: "Berapa lama Anda telah bekerja dalam bidang Anda?"
     - Answer: "I've been working in the culinary field for 8 months..."
   - Q2: "Ceritakan secara singkat pengalaman kerja paling signifikan Anda."
     - Answer: "My most significant experience was leading a team project..."

3. **Main Questions (16)** - Since experience is 8 months → **Beginner level**
   - Answer all 16 questions with meaningful responses
   - Example answers should include behavioral keywords:
     - "determination", "persistent", "motivated" (Determination axis)
     - "willing", "adaptable", "flexible" (Willingness axis)
     - "reliable", "punctual", "organized" (Reliability axis)
     - "honest", "transparent", "truthful" (Honesty axis)

4. **Wage Expectation:**
   - Enter: `5000` (or any number)
   - Click **Submit Wage**

#### 5. View Results
1. Navigate to **Result** page
2. See final report with:
   - Difficulty level: `beginner`
   - Base score: calculated from sentiment analysis
   - Final score: after wage penalty
   - Label: `Layak`, `Dipertimbangkan`, or `Tidak Layak`

#### 6. View Dashboard
1. Navigate to **Dashboard** page
2. See analytics:
   - Relevance score
   - Sentiment score
   - Most frequent words
   - Most weighted words (by behavioral axes)
   - Bar chart of all scores

---

## Test Credentials Reference

| Username | Password | Experience | Level |
|----------|----------|------------|-------|
| junior.dev2025 | JuniorDev@123 | < 12 mo | Beginner |
| mid.engineer99 | MidEng@2024 | 12-18 mo | Intermediate |
| senior.lead88 | SeniorLead@321 | 24+ mo | Advanced |

---

## Scoring Algorithm Reference

### Behavioral Axes Scoring

Each answer is tokenized and scored on 4 axes:

#### 1. Determination
**Positive Words:** dedicated, persistent, determined, motivated, driven, resilient, committed, ambitious
**Negative Words:** unmotivated, give up, quit, apathetic, indifferent, disengaged

#### 2. Willingness
**Positive Words:** willing, eager, enthusiastic, open, cooperative, adaptable, flexible, proactive
**Negative Words:** unwilling, reluctant, resistant, hesitant, avoid, averse

#### 3. Reliability
**Positive Words:** punctual, consistent, dependable, responsible, organized, reliable, steady, trustworthy
**Negative Words:** late, inconsistent, unreliable, irresponsible, careless, erratic

#### 4. Honesty
**Positive Words:** honest, transparent, truthful, sincere, straightforward, upfront, trustworthy
**Negative Words:** dishonest, untruthful, deceptive, evasive, misleading, conceal

### Score Calculation

\`\`\`
Per-Axis Score = (positive_word_count - negative_word_count) / (positive_word_count + negative_word_count + 1)
Range: [-1, 1]

Question Sentiment = average of 4 axes = [-1, 1]
Base Score = (avg_question_scores + normalized_sentiment) / 2
           where normalized_sentiment = (sentiment + 1) / 2 → [0, 1]

Wage Penalty:
  If (wage_expectation / company_budget) >= φ (1.618):
    penalty = 0.05
  Else:
    penalty = 0.0

Final Score = max(0, base_score - penalty)

Decision Labels:
  ≥ 0.80 → "Layak" (Suitable) ✓
  0.60-0.79 → "Dipertimbangkan" (Consider) ~
  < 0.60 → "Tidak Layak" (Not Suitable) ✗
\`\`\`

---

## File Structure

\`\`\`
Interview-Dashboard/
├── main.py                          # Entry point (Streamlit)
├── requirements.txt                 # Python dependencies
├── README_SETUP.md                  # Setup guide
├── COMPLETE_GUIDE.md                # This file
│
├── app/
│   ├── data/
│   │   ├── users/                   # User credentials (JSON)
│   │   ├── reports/                 # Interview results (CSV)
│   │   └── temp/counters/           # ID generation counters
│   │
│   └── modules/
│       ├── __init__.py              # Module exports
│       ├── auth/                    # Authentication
│       │   ├── auth_manager.py      # User CRUD
│       │   └── login.py             # (legacy, auth_manager recommended)
│       ├── QnA/                     # Interview engine
│       │   ├── questions.py         # Question bank
│       │   ├── judger.py            # Interview orchestrator
│       │   ├── decisions.py         # Scoring engine
│       │   ├── text_mining.py       # NLP sentiment analysis
│       │   └── dashboard.py         # Analytics builder
│       ├── io_manager/              # Data I/O
│       │   ├── csvio.py             # CSV operations
│       │   ├── jsonio.py            # JSON operations
│       │   └── storage_paths.py     # Directory configuration
│       ├── utils/                   # Utilities
│       │   ├── validators.py        # Input validation
│       │   └── idgen.py             # User ID generation
│       └── evaluation/              # (future enhancements)
│
├── pages/                           # Streamlit pages
│   ├── 1_Login.py                   # Authentication page
│   ├── 2_Identity.py                # Profile collection page
│   ├── 3_Interview.py               # Interview execution page
│   ├── 4_Result.py                  # Results display page
│   └── 5_Dashboard.py               # Analytics dashboard page
│
└── scripts/
    ├── quick_test.py                # Module verification
    ├── run.sh                       # Unix launcher
    └── run.bat                      # Windows launcher
\`\`\`

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Issue: "NLTK data not found" (punkt_tab missing)
**Solution:** Automatic on first run. Or manually download:
\`\`\`bash
python -c "import nltk; nltk.download('punkt_tab')"
\`\`\`

### Issue: "session_state has no attribute" error
**Solution:** Navigate pages in order (don't skip steps):
1. Start at **Login**
2. Go to **Identity**
3. Go to **Interview**
4. Go to **Result**

### Issue: "FileNotFoundError: app/data/reports"
**Solution:** App auto-creates directories. If not:
\`\`\`bash
mkdir -p app/data/reports
mkdir -p app/data/users
mkdir -p app/data/temp/counters
\`\`\`

### Issue: Port 8501 already in use
**Solution:** Use different port
\`\`\`bash
streamlit run main.py --server.port 8502
\`\`\`

### Issue: "Password does not meet complexity requirements"
**Solution:** Password must have:
- 8+ characters
- Uppercase letter (A-Z)
- Lowercase letter (a-z)
- Digit (0-9)
- Special character (!@#$%^&*)
- Cannot contain username

**Example valid password:** `SecurePass123!`

---

## Performance Notes

- First run: ~10 seconds (NLTK downloads)
- Subsequent runs: <2 seconds startup
- Interview answer processing: ~1 second per answer (NLP analysis)
- Full interview: ~30 seconds (2 leveling + 16 main + sentiment analysis)

---

## Production Checklist

Before deploying to production:

- [ ] Use proper password hashing (`bcrypt` instead of SHA256)
- [ ] Add database instead of JSON files
- [ ] Implement proper authentication (JWT tokens)
- [ ] Add role-based access control (admin, interviewer, candidate)
- [ ] Implement API rate limiting
- [ ] Add input sanitization/XSS prevention
- [ ] Enable HTTPS
- [ ] Add audit logging
- [ ] Implement backup system
- [ ] Configure proper CORS
- [ ] Add error monitoring (Sentry, etc.)

---

## Support & Troubleshooting

For detailed error logs:
\`\`\`bash
# Run with debug logging
streamlit run main.py --logger.level=debug
\`\`\`

Check logs in browser console (F12 → Console tab)

---

**Ready to go! Run: `streamlit run main.py`**
