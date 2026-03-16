import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions" 
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "arcee-ai/trinity-mini:free"

def ask_llm(prompt: str) -> str:
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    result = response.json()
    print(result)

    return result["choices"][0]["message"]["content"]