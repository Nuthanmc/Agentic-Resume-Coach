import fitz
import json

PDF_PATH = r"D:\Resume RAG\data\My_Resume (1).pdf"

pdf = fitz.open(PDF_PATH)

text = ""

for page in pdf:
    text += page.get_text()

sections = [
    "Education",
    "Projects",
    "Research Publications",
    "Technical Skills",
    "Certifications",
    "Hackathons"
]

structured_data = []

for i, section in enumerate(sections):

    start = text.find(section)

    if start == -1:
        continue

    if i < len(sections) - 1:
        next_section = sections[i + 1]
        end = text.find(next_section)

        if end == -1:
            end = len(text)
    else:
        end = len(text)

    content = text[start:end]

    structured_data.append({
        "section": section.lower().replace(" ", "_"),
        "text": content.strip()
    })

with open(
    "structured_resume.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        structured_data,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Sections Extracted")
print(f"Total Sections: {len(structured_data)}")