import re

SKILLS = [
    "python","java","c++","javascript","typescript","sql","mongodb",
    "html","css","react","node.js","django","flask","machine learning",
    "deep learning","artificial intelligence","nlp","tensorflow",
    "pytorch","scikit-learn","pandas","numpy","git","github","docker",
    "aws","azure","gcp","power bi","tableau","excel","rest api",
    "android","kotlin","flutter","streamlit","linux","cyber security"
]

def extract_skills(text):
    lower = text.lower()
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, lower):
            found.append(skill)
    return sorted(set(found))
