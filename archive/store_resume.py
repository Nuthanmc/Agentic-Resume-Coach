import os
from dotenv import load_dotenv
from google import genai

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

load_dotenv()

gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

qdrant = QdrantClient(
    host="localhost",
    port=6333
)

chunks = [
    "Chunk 1 text here",
    "Chunk 2 text here",
    "Chunk 3 text here",
    "Chunk 4 text here",
    "Chunk 5 text here",
    "Chunk 6 text here"
]

points = []

for i, chunk in enumerate(chunks):

    response = gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )

    vector = response.embeddings[0].values

    points.append(
        PointStruct(
            id=i,
            vector=vector,
            payload={
                "text": chunk
            }
        )
    )

qdrant.upsert(
    collection_name="resume",
    points=points
)

print("Resume Stored Successfully")