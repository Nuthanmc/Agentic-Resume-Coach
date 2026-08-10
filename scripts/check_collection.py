from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

info = client.get_collection("resume")

print(info)