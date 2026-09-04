import os

import requests
import streamlit as st
from dotenv import load_dotenv

from ui import configure_page, record_activity, render_bento_grid, render_controls, render_header, render_stats, show_error, show_result

load_dotenv()

configure_page()

MODEL = "google/gemma-3-27b-it"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
if not api_key:
    st.error("OPENROUTER_API_KEY is missing. Add it to a .env file.")
    st.stop()

render_header(MODEL)
render_stats(MODEL)
render_bento_grid()

def generate_response(prompt):
    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "AI Study Assistant",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=90,
    )

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", "a short while")
        raise RuntimeError(
            f"OpenRouter rate limit reached. Try again after {retry_after}, or choose another model."
        )

    if not response.ok:
        try:
            error_message = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            error_message = response.text
        raise RuntimeError(f"OpenRouter error ({response.status_code}): {error_message}")

    return response.json()["choices"][0]["message"]["content"]

mode, topic, submitted = render_controls()

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic or question.")
    else:
        if mode == "Ask a Question":
            prompt = f"Answer this question clearly for a college student. Give examples where useful:\n{topic}"
        elif mode == "Summarize a Topic":
            prompt = f"Create a concise, exam-friendly summary of this topic. Use headings and bullet points:\n{topic}"
        else:
            prompt = f"Create 5 multiple-choice questions on this topic. Give 4 options for each and clearly mark the correct answer with a short explanation:\n{topic}"

        with st.spinner("Generating..."):
            try:
                result = generate_response(prompt)
                record_activity(mode, topic)
                show_result(result)
            except Exception as e:
                show_error(e)
