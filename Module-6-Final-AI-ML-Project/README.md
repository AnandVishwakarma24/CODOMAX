# AI Resume Analyzer & Intelligent Job Recommendation System

An AI-powered Streamlit app that reads a resume (PDF or DOCX), detects skills, scores the resume, recommends matching job roles, and — optionally — generates personalized career advice using an LLM via OpenRouter.

## Features

- 📄 **Resume upload** — drag-and-drop PDF or DOCX files
- 🔍 **Text extraction** — PyMuPDF for PDFs, python-docx for Word files
- 🧠 **Skill detection** — regex/keyword matching against a curated skills list (Python, SQL, React, Machine Learning, AWS, etc.)
- 📊 **Resume scoring** — a 0–100 score based on detected skills, word count, and presence of key resume sections (Education, Experience, Projects, Skills)
- 💼 **Job recommendations** — matches detected skills against a set of job profiles and ranks them by match percentage, showing missing skills for each role
- 🤖 **AI career advice (optional)** — ask suggested or custom questions and get resume-grounded advice from an LLM through the OpenRouter API
- 🎨 **Polished UI** — custom-styled Streamlit interface with an animated background, step-by-step flow, and responsive layout

## Tech Stack

| Purpose            | Library / Tool         |
|---------------------|------------------------|
| Web app / UI         | Streamlit              |
| PDF parsing          | PyMuPDF (`fitz`)       |
| DOCX parsing         | python-docx            |
| Data handling        | pandas                 |
| ML utilities         | scikit-learn           |
| LLM career advice     | OpenRouter API (`requests`) |
| Config management     | python-dotenv          |

## Project Structure

```text
Module-6-Final-AI-ML-Project/
├── app.py                     # Streamlit application (UI + analysis pipeline)
├── model_training.py          # Optional: trains a resume-category classifier
├── requirements.txt
├── README.md
├── .env                       # Local secrets (OPENROUTER_API_KEY, OPENROUTER_MODEL) — not committed
├── .gitignore
├── data/
│   ├── jobs.csv                # Job titles + required skills used for matching
│   └── resumes_sample.csv      # Sample labeled resume snippets for model_training.py
├── models/                    # Trained model artifacts (empty by default)
├── modules/
│   ├── resume_parser.py        # extract_text() — reads PDF/DOCX into plain text
│   ├── skill_extractor.py      # extract_skills() — keyword-based skill detection
│   ├── job_matcher.py           # recommend_jobs(), calculate_resume_score()
│   └── ai_advisor.py            # generate_advice() — OpenRouter LLM integration
├── utils/
│   └── helpers.py               # clean_text() text-cleaning utility
└── screenshots/                # App screenshots for documentation
```

## How It Works

1. **Upload** — user uploads a resume as PDF or DOCX.
2. **Extract** — `resume_parser.extract_text()` pulls raw text from the file.
3. **Detect skills** — `skill_extractor.extract_skills()` scans the text against a predefined skills list using word-boundary regex matching.
4. **Score** — `job_matcher.calculate_resume_score()` combines a skills score, a resume-length score, and a section-presence score into a single 0–100 rating.
5. **Match jobs** — `job_matcher.recommend_jobs()` compares detected skills to each job profile in `data/jobs.csv` and ranks roles by percentage match, listing missing skills.
6. **Get AI advice (optional)** — `ai_advisor.generate_advice()` sends the resume text, detected skills, and the user's question to an LLM via OpenRouter and returns grounded, actionable feedback. If no API key is configured, the app falls back to general resume-writing tips.

## Installation

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Module-6-Final-AI-ML-Project
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

The app opens in your browser (default: `http://localhost:8501`).

## Optional: AI Career Advice Setup

The app works fully without this — you'll just get general resume tips instead of LLM-generated advice.

To enable it, create a `.env` file in the project root:

```text
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=google/gemma-3-27b-it
```

Get a free/paid API key at [openrouter.ai](https://openrouter.ai). `.env` is already listed in `.gitignore` — **never commit real API keys to GitHub.**

> ⚠️ **Security note:** if a real API key was ever placed in a `.env` file and shared or committed anywhere, treat it as compromised — rotate/regenerate it on OpenRouter immediately, since anyone with the key can use it against your account.

## Optional: Training a Resume Classifier

`model_training.py` is a standalone extension that trains a TF-IDF + Logistic Regression classifier to categorize resumes (e.g., "Machine Learning", "Web Development", "Data Analytics").

```bash
python model_training.py
```

- Reads labeled data from `data/resumes.csv` (columns: `text`, `category`) — a small sample is provided in `data/resumes_sample.csv`
- Saves the trained model to `models/resume_classifier.pkl`
- This step is not yet wired into `app.py`; it's a foundation for future extension

## ML/NLP Explanation

The core pipeline uses **keyword/regex-based skill extraction** rather than a trained model — it matches known skill terms against resume text with word-boundary-safe patterns. Job matching computes a simple **set-overlap score** between detected skills and each job's required-skills list. The `model_training.py` script demonstrates how this could evolve into a supervised **TF-IDF + Logistic Regression** text classifier for resume categorization.

## Future Scope

- ATS keyword optimization
- Expand and diversify the job dataset
- TF-IDF + cosine similarity for smarter resume-to-job matching
- Wire up the resume-category classifier (`model_training.py`) into the live app
- LinkedIn-style job matching
- Interview question generation
- Downloadable PDF resume report

## License

This project was built as a final module submission and is free to use for learning purposes.
