from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import tempfile

from modules.textGenerator import generatePracticeText
from modules.voiceRecognizer import processAndScore

app = FastAPI(title="Japanese Speaking Coach")

app.add_middleware(
  CORSMiddleware,
  allow_origins="*",
  allow_methods="*",
  allow_headers="*",
)

# @app.post("/analyze/")
# async def analyzeVoice(file: UploadFile = File(...)):
#   with tempfile.NamedTemporaryFile(delete = False, suffix = ".wav") as tmp:
#     tmp.write(await file.read())
#     tmp_path = tmp.name
    
#   transcription = CALL_METHOD
#   correction = CORRECT_METHOD
#   # IMPLEMENTED LATER
#   # scores = score_pronounciation(tmp_path)
  
#   return {
#     "transcription": transcription,
#     "correction": correction
#     # "scores": scores
#   }
  
@app.get("/generate_text")
def generate_text(level: str = Query("basic")):
  data = generatePracticeText(level)
  
  return JSONResponse(content=data)

@app.post("/score_pronunciation")
def score_pronunciation(file: UploadFile = File(...), text: str = ""):
  if not file or not file.filename:
    raise HTTPException(status_code=400, detail="No file uploaded or filename missing")
    
  # safe_filename = "".join(c for c in file.filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
  # if not safe_filename:
  #     raise HTTPException(status_code=400, detail="Invalid filename")
  
  audio_path = f"temp_{file.filename}"
  with open(audio_path, "wb") as f:
      f.write(file.file.read())
      
  print("mana", audio_path)

  result = processAndScore(audio_path, text)
  

  return result
  
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8080)