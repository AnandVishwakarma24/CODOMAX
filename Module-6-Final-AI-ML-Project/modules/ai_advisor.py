import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_advice(resume_text, skills, question):
    api_key=os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return (
            "OPENROUTER_API_KEY is not configured.\n\n"
            "General advice:\n"
            "- Add measurable achievements to projects and experience.\n"
            "- Match important skills from the target job description.\n"
            "- Keep the resume concise and ATS-friendly.\n"
            "- Add GitHub/project links where relevant."
        )

    prompt=f"""You are an expert AI career advisor specializing in resumes, machine learning careers, ATS optimization, and entry-level job preparation.

You must analyze the user's actual resume and answer ONLY the user's question.

Detected skills:
{skills}

User question:
{question}

Resume:
{resume_text[:12000]}

Instructions:
1. Base your answer on the resume provided. Do not invent achievements, experience, projects, metrics, accuracy scores, CGPA, or technologies.
2. If a metric is missing, explicitly say that it should be measured rather than creating a value.
3. Give specific, actionable recommendations instead of generic career advice.
4. Identify exact weaknesses or missing information from the resume when relevant.
5. When suggesting rewritten resume content, provide ready-to-use wording.
6. For technical or machine-learning questions, prioritize relevant ML, Python, NLP, data, deployment, and software-engineering skills only when supported by the resume.
7. Keep the response concise and structured.
8. Do not repeat the entire resume.
9. Do not give advice unrelated to the user's question.

Response format:
- Start with a short direct answer to the user's question.
- Then provide the most important improvements as bullet points.
- If rewriting is requested, show the improved version clearly.
- If the resume lacks information needed for a recommendation, state exactly what is missing.
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": os.getenv("OPENROUTER_MODEL", "google/gemma-3-27b-it"),
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as error:
        return (
            "OpenRouter could not generate advice right now. "
            f"Please check your API key, model, or account quota. ({error})"
        )
    except (KeyError, TypeError, ValueError):
        return "OpenRouter returned an unexpected response. Please try again."
