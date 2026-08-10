import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load Resume Skills
with open("resume_skills.json", "r", encoding="utf-8") as f:
    resume_data = json.load(f)

# Load JD Skills
with open("jobs/jd_skills.json", "r", encoding="utf-8") as f:
    jd_data = json.load(f)

resume_skills = resume_data["skills"]
jd_skills = jd_data["skills"]

prompt = f"""
You are an expert ATS Resume Reviewer and AI Career Coach.

Resume Skills:
{resume_skills}

Job Description Skills:
{jd_skills}

Perform the following:

1. Identify missing skills.
2. Suggest resume improvements.
3. Generate 3 new resume bullet points that improve ATS score.
4. Recommend project descriptions to add.
5. Recommend keywords that should appear in the resume.

Format professionally.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\n" + "="*60)
print("RESUME IMPROVEMENT REPORT")
print("="*60)

print(response.text)