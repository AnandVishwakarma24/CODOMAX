# AI Study Assistant

## Project Overview

AI-powered study workspace built with Streamlit and OpenRouter. Choose a study mode, enter a topic or question, and generate:

- Clear explanations for study questions
- Concise, exam-friendly topic summaries
- Five multiple-choice questions with answers and explanations

The app uses the `google/gemma-3-27b-it` model through OpenRouter.

## Interface

- Light, responsive workspace layout
- Animated response statistics
- Radio-style study mode cards
- Expandable details for each mode
- Animated generate button and focused prompt composer

## Technologies

- Python
- Streamlit
- OpenRouter API
- python-dotenv

## Setup and Run

1. Install Python 3.10+.
2. Open the project folder in VS Code/Terminal.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create an API key at [OpenRouter](https://openrouter.ai/keys).
5. Create a `.env` file in the project root and add your key:
   ```text
   OPENROUTER_API_KEY=your_key_here
   ```
6. Start the Streamlit app:
   ```bash
   python -m streamlit run app.py
   ```
7. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Project Files

- `app.py` - application entry point and OpenRouter request flow
- `ui.py` - page layout, styling, controls, stats, and result display
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit theme and server settings

Never commit `.env` or expose the OpenRouter API key.

## Demo Evidence

Take screenshots of:

1. The home screen.
2. A generated answer.
3. Generated MCQs.

## Learning Outcome

This project demonstrates how AI tools can be integrated into a focused educational productivity application.
