import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chunks = [
    "Nuthan M C Bengaluru Karnataka AI ML",
    "FarmersHub MERN CNN NLP",
    "GradeChain Solidity IPFS Ethereum",
]

for i, chunk in enumerate(chunks):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )

    vector = response.embeddings[0].values

    print(f"Chunk {i+1}")
    print("Dimension:", len(vector))
    print()