import os

from dotenv import load_dotenv
from google import genai
from qdrant_client import QdrantClient

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

qdrant = QdrantClient(
    host="localhost",
    port=6333
)

question = input("Ask: ")

# Embed query
embedding = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question
)

query_vector = embedding.embeddings[0].values

# Retrieve
results = qdrant.query_points(
    collection_name="resume",
    query=query_vector,
    limit=3
)

context = "\n\n".join(
    point.payload["text"]
    for point in results.points
)

prompt = f"""
You are Nuthan's Resume Assistant.

Resume Context:
{context}

Question:
{question}

Answer based only on the resume.
"""
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\nAnswer:")
print(response.text)