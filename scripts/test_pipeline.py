import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
from google import genai
from ingestion.resume_processor import (
    extract_text_from_pdf,
    parse_resume_with_gemini,
    build_in_memory_vector_store,
    query_resume_rag,
    extract_jd_skills_with_gemini
)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

sample_pdf = BASE_DIR / "data" / "My_Resume (1).pdf"
if sample_pdf.exists():
    with open(sample_pdf, "rb") as f:
        pdf_bytes = f.read()

    print("1. Extracting PDF text...")
    text = extract_text_from_pdf(pdf_bytes)
    print(f"Extracted {len(text)} characters.")

    print("\n2. Parsing with Gemini...")
    parsed = parse_resume_with_gemini(text, client)
    print("Candidate:", parsed.get("candidate_name"))
    print("Skills extracted:", len(parsed.get("skills", [])))
    print("Sections parsed:", len(parsed.get("sections", [])))

    print("\n3. Building in-memory vector store...")
    qdrant = build_in_memory_vector_store(parsed.get("sections", []), client)
    print("In-memory store built successfully.")

    print("\n4. Testing RAG Query...")
    answer = query_resume_rag(qdrant, client, "What degrees and GPA does the candidate have?")
    print("RAG Answer:\n", answer)

    print("\n5. Testing JD Skills Extraction...")
    jd_sample = "Looking for Senior AI Engineer skilled in Python, PyTorch, LangChain, Docker, and AWS."
    jd_skills = extract_jd_skills_with_gemini(jd_sample, client)
    print("JD Skills:", jd_skills)

    print("\n✅ All pipeline steps verified successfully!")
