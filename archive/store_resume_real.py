import os
import fitz

from dotenv import load_dotenv
from google import genai

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

load_dotenv()

# Gemini
gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Qdrant
qdrant = QdrantClient(
    host="localhost",
    port=6333
)

# Read PDF
pdf = fitz.open(r"D:\Resume RAG\data\My_Resume (1).pdf")

text = ""

for page in pdf:
    text += page.get_text()


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


chunks = chunk_text(text)

# Recreate collection
qdrant.recreate_collection(
    collection_name="resume",
    vectors_config=VectorParams(
        size=3072,
        distance=Distance.COSINE,
    )
)

points = []

for idx, chunk in enumerate(chunks):

    emb = gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk,
    )

    vector = emb.embeddings[0].values

    points.append(
        PointStruct(
            id=idx,
            vector=vector,
            payload={
                "text": chunk,
            },
        )
    )

qdrant.upsert(
    collection_name="resume",
    points=points,
)

print(f"Stored {len(points)} chunks")