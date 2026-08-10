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
You are an expert AI Career Coach.

Resume Skills:
{resume_skills}

Job Description Skills:
{jd_skills}

Analyze:

1. Match Strength
2. Missing Skills
3. Learning Roadmap
4. Resume Improvements
5. Career Advice

Format the response professionally.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\n" + "="*60)
print("AI SKILL GAP ANALYSIS")
print("="*60)
print(response.text)