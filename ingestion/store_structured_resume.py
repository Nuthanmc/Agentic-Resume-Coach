import json
import os

from dotenv import load_dotenv
from google import genai

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    Distance,
    VectorParams
)

load_dotenv()

gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

qdrant = QdrantClient(
    host="localhost",
    port=6333
)

with open(
    "structured_resume.json",
    "r",
    encoding="utf-8"
) as f:
    sections = json.load(f)

# Recreate collection
qdrant.recreate_collection(
    collection_name="resume_structured",
    vectors_config=VectorParams(
        size=3072,
        distance=Distance.COSINE
    )
)

points = []

for idx, item in enumerate(sections):

    embedding = gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=item["text"]
    )

    vector = embedding.embeddings[0].values

    points.append(
        PointStruct(
            id=idx,
            vector=vector,
            payload={
                "section": item["section"],
                "text": item["text"]
            }
        )
    )

qdrant.upsert(
    collection_name="resume_structured",
    points=points
)

print(f"Stored {len(points)} sections")