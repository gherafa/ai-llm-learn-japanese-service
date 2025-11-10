import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "moonshotai/Kimi-K2-Instruct-0905"
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def aiPromptConnector(input):
    response = requests.post(HF_API_URL, headers=headers, json=input)
    response.raise_for_status()
    data = response.json()
    
    # Extract generated content
    try:
        result = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        raise ValueError("Unexpected API response format: " + str(data))

    return result