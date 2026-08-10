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

query = "What blockchain projects has Nuthan worked on?"

embedding = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query
)

query_vector = embedding.embeddings[0].values

results = qdrant.query_points(
    collection_name="resume",
    query=query_vector,
    limit=3
)

for point in results.points:
    print("\nScore:", point.score)
    print(point.payload["text"])