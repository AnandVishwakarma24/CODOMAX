from modules.skill_extractor import SKILLS

JOBS = [
    {"title":"Python Developer","skills":["python","sql","git","rest api","django"]},
    {"title":"Data Analyst","skills":["python","sql","excel","power bi","pandas","numpy"]},
    {"title":"Machine Learning Engineer","skills":["python","machine learning","scikit-learn","pandas","numpy","tensorflow","git"]},
    {"title":"Frontend Developer","skills":["html","css","javascript","react","git"]},
    {"title":"Full Stack Developer","skills":["html","css","javascript","react","node.js","mongodb","git"]},
    {"title":"Cloud Engineer","skills":["linux","aws","docker","git"]},
    {"title":"AI/NLP Engineer","skills":["python","artificial intelligence","nlp","machine learning","pytorch","tensorflow"]}
]

def recommend_jobs(candidate_skills, limit=5):
    candidate = set(s.lower() for s in candidate_skills)
    results=[]
    for job in JOBS:
        required=set(job["skills"])
        matched=candidate & required
        score=round(len(matched)/len(required)*100)
        missing=sorted(required-candidate)
        results.append({"title":job["title"],"match":score,"missing":missing})
    return sorted(results, key=lambda x:x["match"], reverse=True)[:limit]

def calculate_resume_score(text, skills):
    words=len(text.split())
    skill_score=min(len(skills)*4, 40)
    length_score=30 if words >= 250 else 20 if words >= 120 else 10
    section_score=30 if any(x in text.lower() for x in ["education","experience","projects","skills"]) else 15
    return min(100, skill_score+length_score+section_score)
