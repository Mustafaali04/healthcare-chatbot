import os
from dotenv import load_dotenv
import requests

load_dotenv(dotenv_path="C:/Users/munna/OneDrive/Desktop/healthcare-chatbot/.env")

api_key = os.getenv("OPENROUTER_API_KEY")

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
    },
    json={
        "model": "openrouter/free",
        "messages": [
            {"role": "user", "content": "What is diabetes? Answer in 2 sentences."}
        ]
    }
)

print(response.json()["choices"][0]["message"]["content"])