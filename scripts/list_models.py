print("Script Started")

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API Key Found:", api_key is not None)

client = genai.Client(api_key=api_key)

print("Client Created")

for model in client.models.list():
    print(model.name)

print("Finished")