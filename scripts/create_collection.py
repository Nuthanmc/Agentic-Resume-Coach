from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient("localhost", port=6333)

client.recreate_collection(
    collection_name="resume",
    vectors_config=VectorParams(
        size=3072,
        distance=Distance.COSINE
    )
)

print("Collection Created")