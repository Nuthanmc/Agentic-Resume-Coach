import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

with open(
    "structured_resume.json",
    "r",
    encoding="utf-8"
) as f:
    resume_data = json.load(f)

resume_text = ""

for item in resume_data:
    resume_text += item["text"] + "\n\n"

prompt = f"""
Extract all technical skills from this resume.

Return ONLY valid JSON.

Example:
{{
  "skills": ["Python", "Machine Learning", "MongoDB"]
}}

Resume:
{resume_text}
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

with open("resume_skills.json", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Resume skills saved successfully!")