# AI Resume Analyzer & Intelligent Job Recommendation System

An AI-powered resume analysis and job recommendation application built with Python and Streamlit.

## Features
- PDF/DOCX resume upload
- Resume text extraction
- Automatic skill extraction using NLP-style keyword matching
- Resume scoring
- Job-role recommendation
- Skill-gap analysis
- Optional LLM-powered career advice through OpenRouter

## Tech Stack
- Python
- Streamlit
- PyMuPDF
- python-docx
- Scikit-learn
- OpenRouter API
- Pandas

## Project Structure
```text
AI-Resume-Analyzer/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── data/jobs.csv
├── modules/
│   ├── resume_parser.py
│   ├── skill_extractor.py
│   ├── job_matcher.py
│   └── ai_advisor.py
└── utils/helpers.py
```

## Installation
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Resume-Analyzer
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```

## Optional AI Setup
Create a `.env`/environment configuration containing:
```text
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=google/gemma-3-27b-it
```

Never commit API keys to GitHub.

## ML/NLP Explanation
The project performs skill extraction from resume text and calculates job-role similarity based on required versus detected skills. The architecture can later be extended with TF-IDF + cosine similarity or a supervised resume-classification model.

## Future Scope
- ATS keyword optimization
- More job datasets
- TF-IDF/cosine similarity
- Resume category classifier
- LinkedIn-style job matching
- Interview question generation
- Resume PDF report generation
