import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_TOKEN")
HUGGIN_FACE_BASE_URL = os.getenv("HUGGIN_FACE_BASE_URL")
LLM_URL = "v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

async def aiPromptConnector(input):
  try:
    response = requests.post(f"{HUGGIN_FACE_BASE_URL}{LLM_URL}", headers=headers, json=input)
    response.raise_for_status()
    data = response.json()
    
    result = data["choices"][0]["message"]["content"].strip()
  except (KeyError, IndexError):
      raise ValueError("Unexpected API response format: " + str(data))

  return result