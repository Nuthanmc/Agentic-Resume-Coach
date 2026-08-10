import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents="Nuthan knows Python, AI and Machine Learning"
)

print("Embedding Length:", len(response.embeddings[0].values))