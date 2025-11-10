from transformers import AutoTokenizer, AutoModelForCausalLM
from modules.utils import generatePromptByLevel, convertToRomaji, translateToEng
from connectors.hugginFaceConnector import aiPromptConnector

tokenizer = AutoTokenizer.from_pretrained("rinna/japanese-gpt2-small")
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt2-small")
MODEL_ID = "moonshotai/Kimi-K2-Instruct-0905"

def generatePracticeText(level="basic"):
  # Generate Result
  selectedPrompt = generatePromptByLevel(level)
  prompt, topic = selectedPrompt
  inputs = tokenizer(prompt, return_tensors="pt")
  outputs = model.generate(
      **inputs,
      max_new_tokens=60,
      temperature=1.0,
      top_k=50,
      top_p=0.9,
      do_sample=True
  )

  # Decode and clean output
  generated = outputs[0][inputs["input_ids"].shape[-1]:]
  result = tokenizer.decode(generated, skip_special_tokens=True).strip()
  if "。" in result:
      result = result.split("。")[0] + "。"

  # Create Romaji 
  romaji = convertToRomaji(result)
  
  # Create Translation
  translation = translateToEng(result)

  return {
      "level": level,
      "topic": topic,
      "source": "local-model",
      "practice_text": result,
      "romaji": romaji,
      "translation": translation
  }


def generatePracticeText(level="basic"):
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

    # Call Hugging Face API
    result = aiPromptConnector(constructedInput)

    # Clean output to end at first '。'
    if "。" in result:
        result = result.split("。")[0] + "。"

    # Convert to Romaji
    romaji = convertToRomaji(result)

    # Translate to English
    translation = translateToEng(result)

    return {
        "level": level,
        "topic": topic,
        "source": "api",
        "practice_text": result,
        "romaji": romaji,
        "translation": translation
    }