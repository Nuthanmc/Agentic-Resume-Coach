import os
from dotenv import load_dotenv
from google import genai
from qdrant_client import QdrantClient

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
qdrant_path = str(BASE_DIR / "data" / "qdrant_db")

qdrant = QdrantClient(path=qdrant_path)

def ask_resume(question):

    embedding = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    query_vector = embedding.embeddings[0].values

    results = qdrant.query_points(
        collection_name="resume_structured",
        query=query_vector,
        limit=3
    )

    context = ""

    for point in results.points:
        context += point.payload["text"] + "\n\n"

    prompt = f"""
    You are Nuthan's Resume Assistant.

    Answer ONLY using the resume information below.

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


if __name__ == "__main__":

    question = input("Ask: ")

    answer = ask_resume(question)

    print("\nANSWER:\n")
    print(answer)