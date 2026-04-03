import os
import json
import re
import requests
import pdfplumber
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

application = Flask(__name__)
application.secret_key = os.getenv("SECRET_KEY", "dev-secret")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "mistral-large-latest"

ALLOWED_EXTENSIONS = {"pdf"}


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_storage):
    text = ""
    try:
        with pdfplumber.open(file_storage) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print("PDF extraction error:", e)
    return text.strip()


def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ").strip()
    except Exception as e:
        print("URL extraction error:", e)
        return ""


def call_mistral(system_prompt, user_prompt):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(MISTRAL_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


# --------------------------------------------------
# SAFE JSON PARSER (IMPORTANT FIX)
# --------------------------------------------------

def safe_json_parse(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No valid JSON found in model output.")


# --------------------------------------------------
# Extraction
# --------------------------------------------------

def extract_resume_data(resume_text):
    if not resume_text:
        raise ValueError("Resume text is empty.")

    system_prompt = "Extract structured JSON from resumes."

    user_prompt = f"""
Return ONLY valid JSON in this format:

{{
  "skills": [],
  "years_experience_total": 0,
  "education_level": "",
  "industries": [],
  "certifications": []
}}

Resume:
{resume_text}
"""

    result = call_mistral(system_prompt, user_prompt)
    return safe_json_parse(result)


def extract_job_data(job_text):
    if not job_text:
        raise ValueError("Job description text is empty.")

    system_prompt = "Extract structured JSON from job descriptions."

    user_prompt = f"""
Return ONLY valid JSON in this format:

{{
  "required_skills": [],
  "preferred_skills": [],
  "min_years_experience": 0,
  "seniority_level": "",
  "education_required": "",
  "industry_preference": []
}}

Job Description:
{job_text}
"""

    result = call_mistral(system_prompt, user_prompt)
    return safe_json_parse(result)


# --------------------------------------------------
# Scoring (no free points)
# --------------------------------------------------

def calculate_score(resume, job):

    if not resume.get("skills") or not job.get("required_skills"):
        return 0

    score = 0

    required = set(job.get("required_skills", []))
    candidate_skills = set(resume.get("skills", []))

    required_ratio = len(required & candidate_skills) / len(required)
    score += required_ratio * 40

    preferred = set(job.get("preferred_skills", []))
    if preferred:
        preferred_ratio = len(preferred & candidate_skills) / len(preferred)
        score += preferred_ratio * 10

    required_years = job.get("min_years_experience", 0)
    candidate_years = resume.get("years_experience_total", 0)

    if required_years > 0:
        experience_ratio = min(candidate_years / required_years, 1)
        score += experience_ratio * 25

    if resume.get("education_level") == job.get("education_required"):
        score += 5

    job_industries = set(job.get("industry_preference", []))
    candidate_industries = set(resume.get("industries", []))

    if job_industries:
        industry_ratio = len(job_industries & candidate_industries) / len(job_industries)
        score += industry_ratio * 10

    return round(score, 2)


# --------------------------------------------------
# AI Explanation + Cover Letter
# --------------------------------------------------

def generate_explanation(score, resume_json, job_json):
    system_prompt = "You are a brutally honest career analyst."

    user_prompt = f"""
Score: {score}

Resume JSON:
{json.dumps(resume_json, indent=2)}

Job JSON:
{json.dumps(job_json, indent=2)}

Explain clearly:
- Why this score
- Strengths
- Missing skills
- Competitiveness
- 3 improvements
"""

    return call_mistral(system_prompt, user_prompt)


def generate_cover_letter(resume_json, job_json):
    system_prompt = "Write a professional tailored cover letter."

    user_prompt = f"""
Using this resume JSON:
{json.dumps(resume_json, indent=2)}

And this job JSON:
{json.dumps(job_json, indent=2)}

Write a focused, non-generic 1-page cover letter.
"""

    return call_mistral(system_prompt, user_prompt)


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@application.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@application.route("/analyze", methods=["POST"])
def analyze():

    resume_file = request.files.get("resume")
    job_input = request.form.get("job_input")

    if not resume_file or resume_file.filename == "":
        return "Resume required."

    if not allowed_file(resume_file.filename):
        return "Only PDF supported."

    resume_text = extract_text_from_pdf(resume_file)

    if not resume_text:
        return "Could not extract text from resume."

    if not job_input:
        return "Job description or URL required."

    if job_input.startswith("http"):
        job_text = extract_text_from_url(job_input)
    else:
        job_text = job_input.strip()

    if not job_text:
        return "Could not extract job text."

    try:
        resume_json = extract_resume_data(resume_text)
        job_json = extract_job_data(job_text)
    except Exception as e:
        return f"Parsing failed: {str(e)}"

    score = calculate_score(resume_json, job_json)

    if score == 0:
        return "Insufficient match data to calculate score."

    explanation = generate_explanation(score, resume_json, job_json)
    cover_letter = generate_cover_letter(resume_json, job_json)

    return render_template(
        "result.html",
        score=score,
        explanation=explanation,
        cover_letter=cover_letter
    )


if __name__ == "__main__":
    application.run(debug=True)

