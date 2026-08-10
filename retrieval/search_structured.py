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

query = input("Ask: ")

embedding = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query
)

query_vector = embedding.embeddings[0].values

results = qdrant.query_points(
    collection_name="resume_structured",
    query=query_vector,
    limit=3
)

for point in results.points:
    print("\n" + "="*50)
    print("SECTION:", point.payload["section"])
    print("="*50)
    print(point.payload["text"][:500])