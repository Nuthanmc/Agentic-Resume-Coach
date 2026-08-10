import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

with open(
    "jobs/ai_engineer.txt",
    "r",
    encoding="utf-8"
) as f:
    jd_text = f.read()

prompt = f"""
Extract only technical skills from this job description.

Return ONLY valid JSON.

Example:
{{
  "skills": ["Python", "Docker"]
}}

Job Description:
{jd_text}
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

with open("jobs/jd_skills.json", "w", encoding="utf-8") as f:
    f.write(response.text)

print("JD skills saved successfully!")