from pykakasi import kakasi
from fastapi.responses import JSONResponse
import whisper
import Levenshtein

from modules.utils import removeKanjiPunctuation, convertToRomaji

kakasiLib = kakasi()
kakasiLib.setMode("J", "a")
kakasiLib.setMode("K", "a")
kakasiLib.setMode("H", "a")
converter = kakasiLib.getConverter()

model = whisper.load_model("base")

def transcribe_audio(audioPath: str, language="ja"):
  result = model.transcribe(audioPath, language=language)
  spokenText = result["text"].strip()

  return spokenText


def processAndScore(audioPath: str, referenceText: str):
  spokenText = transcribe_audio(audioPath)

  refChars = removeKanjiPunctuation(referenceText)
  spokenChars = removeKanjiPunctuation(spokenText)
  
  if "。" in referenceText:
        refSplitResult = referenceText.split("。")[0] + "。"
  else:
      refSplitResult = referenceText

  if "。" in spokenText:
      spokenSplitResult = spokenText.split("。")[0] + "。"
  else:
      spokenSplitResult = spokenText

  refRomaji = convertToRomaji(refSplitResult)
  spokenRomaji = convertToRomaji(spokenSplitResult)

  # Compute error distance
  distance = Levenshtein.distance("".join(refChars), "".join(spokenChars))
  max_len = max(len(refChars), len(spokenChars))

  score = max(0, 100 * (1 - distance / max_len))

  payloadResult = {
    "spoken_text": spokenText,
    "reference_text": referenceText,
    "ref_romaji": refRomaji,
    "spoken_romaji": spokenRomaji,
    "score": round(score, 2),
  }
  
  return JSONResponse(content=payloadResult)