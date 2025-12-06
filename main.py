from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.modules.textGenerator import generatePracticeText
from src.modules.voiceRecognizer import processAndScore

app = FastAPI(title="Japanese Speaking Coach")

app.add_middleware(
  CORSMiddleware,
  allow_origins="*",
  allow_methods="*",
  allow_headers="*",
)
  
@app.get("/generate_text")
async def generate_text(level: str = Query("basic")):
  data = await generatePracticeText(level)
  
  return data

@app.post("/score_pronunciation")
def score_pronunciation(file: UploadFile = File(...), text: str = ""):
  if not file or not file.filename:
    raise HTTPException(status_code=400, detail="No file uploaded or filename missing")
    
  safe_filename = "".join(c for c in file.filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
  if not safe_filename:
      raise HTTPException(status_code=400, detail="Invalid filename")
  
  audio_path = f"temp_{file.filename}"
  with open(audio_path, "wb") as f:
      f.write(file.file.read())

  result = processAndScore(audio_path, text)
  

  return result
  
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8080)