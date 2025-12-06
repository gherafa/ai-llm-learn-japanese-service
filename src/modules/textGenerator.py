from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import asyncio

from src.modules.utils import generatePromptByLevel, convertToRomaji, translateToEng
from src.connectors.hugginFaceConnector import aiPromptConnector

load_dotenv()

MODEL_ID = os.getenv("MODEL_ID")
LOCAL_MODEL = "rinna/japanese-gpt2-small"
tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL)
model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL)

def generatePracticeTextLocalModel(prompt):
  inputs = tokenizer(prompt, return_tensors="pt")
  outputs = model.generate(
    **inputs,
    max_new_tokens=60,
    temperature=1.0,
    top_k=50,
    top_p=0.9,
    do_sample=True
  )

  generated = outputs[0][inputs["input_ids"].shape[-1]:]
  result = tokenizer.decode(generated, skip_special_tokens=True).strip()
  
  return result

async def generatePracticeText(level="basic"):
  # Generate prompt
  selectedPrompt = generatePromptByLevel(level)
  prompt, topic = selectedPrompt
  constructedInput = {
    "model": MODEL_ID,
    "messages": [
        {
            "role": "user",
            "content": prompt,
        }
    ],
    "max_tokens": 60,
    "temperature": 1.0
  }

  try:
    print(f"[INFO] Using API model generation {MODEL_ID}")
    result = await aiPromptConnector(constructedInput)
    source = "api"
  
  except Exception as e:
    print(f"[WARNING] API generation failed: {e}")
    
    try:
      print(f"[INFO] Using local model generation {LOCAL_MODEL}")
      loop = asyncio.get_running_loop()
      local_result = await loop.run_in_executor(None, generatePracticeTextLocalModel, prompt)
      result = local_result
      source = "local_model"

    except Exception as local_err:
      print(f"[ERROR] Local generation failed: {local_err}")
  
      return JSONResponse(
          status_code=500,
          content={"error": "Both API and local model generation failed"}
      )
      
  if not result or not isinstance(result, str):
    return JSONResponse(status_code=500, content={"error": "No valid text generated"})

  # Clean output to end at first '。'
  if "。" in result:
    result = result.split("。")[0] + "。"

  # Convert to romaji
  try:
    romaji = convertToRomaji(result)
  except Exception as e:
    print(f"[WARNING] Romaji conversion failed: {e}")
    romaji = ""

  # Translate to English
  try:
    translation = translateToEng(result)
  except Exception as e:
    print(f"[WARNING] Translation failed: {e}")
    translation = ""
  
  payloadResult = {
    "level": level,
    "topic": topic,
    "source": source,
    "practice_text": result,
    "romaji": romaji,
    "translation": translation
  }

  return JSONResponse(content=payloadResult)