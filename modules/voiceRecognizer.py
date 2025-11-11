from pykakasi import kakasi

import whisper
import Levenshtein

from modules.utils import removeKanjiPunctuation

kks = kakasi()
kks.setMode("J", "a")
kks.setMode("K", "a")
kks.setMode("H", "a")
converter = kks.getConverter()

model = whisper.load_model("base")

def transcribe_audio(audioPath: str, language="ja"):
  result = model.transcribe(audioPath, language=language)
  spoken_text = result["text"].strip()

  return spoken_text


def processAndScore(audioPath: str, referenceText: str):
  spoken_text = transcribe_audio(audioPath)

  refChars = removeKanjiPunctuation(referenceText)
  spokenChars = removeKanjiPunctuation(spoken_text)

  # Compute Levenshtein distance
  distance = Levenshtein.distance("".join(refChars), "".join(spokenChars))
  max_len = max(len(refChars), len(spokenChars))

  score = max(0, 100 * (1 - distance / max_len))

  return {
      "spoken_text": spoken_text,
      "reference_text": referenceText,
      "ref_romaji": "".join(refChars),
      "spoken_romaji": "".join(spokenChars),
      "score": round(score, 2),
  }