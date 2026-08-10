import json

# Load resume skills
with open("resume_skills.json", "r", encoding="utf-8") as f:
    resume_data = json.load(f)

# Load JD skills
with open("jobs/jd_skills.json", "r", encoding="utf-8") as f:
    jd_data = json.load(f)

resume_skills = {skill.lower() for skill in resume_data["skills"]}
jd_skills = {skill.lower() for skill in jd_data["skills"]}

matched = resume_skills.intersection(jd_skills)
missing = jd_skills - resume_skills

score = round((len(matched) / len(jd_skills)) * 100, 2)

print("\n" + "=" * 50)
print("RESUME MATCH REPORT")
print("=" * 50)

print(f"\nMatch Score: {score}%")

print("\nMatched Skills:")
for skill in sorted(matched):
    print(f"✓ {skill}")

print("\nMissing Skills:")
for skill in sorted(missing):
    print(f"✗ {skill}")