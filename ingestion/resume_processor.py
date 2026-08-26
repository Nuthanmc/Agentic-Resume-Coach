import json
import re
import pymupdf as fitz
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract raw text from PDF bytes using PyMuPDF."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text_chunks = []
    for page in doc:
        text_chunks.append(page.get_text())
    return "\n".join(text_chunks).strip()

def parse_resume_with_gemini(resume_text: str, client: genai.Client) -> dict:
    """Use Gemini to segment resume into structured sections and extract technical skills."""
    prompt = f"""
You are an expert ATS Resume Parser. Analyze the following resume text and parse it into structured components.

Return ONLY a valid JSON object matching this exact structure:
{{
  "candidate_name": "Full Name or Candidate",
  "skills": ["Python", "Machine Learning", "SQL"],
  "sections": [
    {{
      "section": "Education",
      "text": "Detailed text of education section"
    }},
    {{
      "section": "Experience",
      "text": "Detailed text of work experience"
    }},
    {{
      "section": "Projects",
      "text": "Detailed text of projects"
    }},
    {{
      "section": "Technical Skills",
      "text": "Detailed technical skills"
    }},
    {{
      "section": "Certifications",
      "text": "Certifications and courses"
    }},
    {{
      "section": "Research or Achievements",
      "text": "Publications, hackathons, or achievements"
    }}
  ]
}}

Only include sections that have meaningful content in the resume.

Resume Text:
{resume_text}
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    try:
        data = json.loads(response.text)
        return data
    except Exception:
        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return {
            "candidate_name": "Candidate",
            "skills": [],
            "sections": [{"section": "Full Resume", "text": resume_text}]
        }

def build_in_memory_vector_store(sections: list, client: genai.Client) -> QdrantClient:
    """Create an in-memory Qdrant client, embed each section, and index vectors."""
    qdrant = QdrantClient(location=":memory:")
    collection_name = "resume_collection"
    
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=3072,
            distance=Distance.COSINE
        )
    )
    
    points = []
    for idx, item in enumerate(sections):
        sec_text = item.get("text", "")
        if not sec_text.strip():
            continue
            
        embedding = client.models.embed_content(
            model="gemini-embedding-001",
            contents=sec_text
        )
        vector = embedding.embeddings[0].values
        
        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "section": item.get("section", "General"),
                    "text": sec_text
                }
            )
        )
    
    if points:
        qdrant.upsert(
            collection_name=collection_name,
            points=points
        )
    
    return qdrant

def query_resume_rag(qdrant: QdrantClient, client: genai.Client, question: str, candidate_name: str = "the candidate") -> str:
    """Embed query, retrieve top sections from in-memory Qdrant, and generate an answer."""
    embedding = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )
    query_vector = embedding.embeddings[0].values
    
    results = qdrant.query_points(
        collection_name="resume_collection",
        query=query_vector,
        limit=4
    )
    
    context_chunks = [point.payload.get("text", "") for point in results.points]
    context = "\n\n---\n\n".join(context_chunks)
    
    prompt = f"""
You are an expert AI Resume Assistant representing {candidate_name}.
Answer the user's question accurately and professionally, using ONLY the verified resume context below.
If the information is not present in the context, politely state that it is not mentioned in the resume.

Resume Context:
{context}

Question:
{question}
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

def extract_jd_skills_with_gemini(jd_text: str, client: genai.Client) -> list:
    """Extract technical skills from a Job Description using Gemini."""
    prompt = f"""
Extract all technical skills, programming languages, tools, frameworks, and core domain requirements from this Job Description.

Return ONLY a JSON array of strings:
["Skill1", "Skill2", "Skill3"]

Job Description:
{jd_text}
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    try:
        skills = json.loads(response.text)
        if isinstance(skills, list):
            return skills
        elif isinstance(skills, dict) and "skills" in skills:
            return skills["skills"]
        return []
    except Exception:
        return []
