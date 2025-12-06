from unittest.mock import patch
from fastapi.responses import JSONResponse

from src.modules.voiceRecognizer import (
  transcribe_audio,
  processAndScore
)

@patch("src.modules.voiceRecognizer.model")
def test_transcribe_audio(mock_model):
  mock_model.transcribe.return_value = {
      "text": "  こんにちは。 "
  }

  result = transcribe_audio("dummy.wav")

  assert result == "こんにちは。"
  mock_model.transcribe.assert_called_once_with("dummy.wav", language="ja")

@patch("src.modules.voiceRecognizer.convertToRomaji")
@patch("src.modules.voiceRecognizer.removeKanjiPunctuation")
@patch("src.modules.voiceRecognizer.Levenshtein.distance")
@patch("src.modules.voiceRecognizer.transcribe_audio")
def test_process_and_score(
  mock_transcribe,
  mock_distance,
  mock_remove_punct,
  mock_romaji
):
  mock_transcribe.return_value = "こんにちは。"
  mock_remove_punct.side_effect = [
      ["k", "o", "n", "n", "i", "c", "h", "i"],
      ["k", "o", "n", "n", "i", "c", "h", "i"],
  ]
  mock_romaji.side_effect = ["konnichi", "konnichi"]
  mock_distance.return_value = 0
  
  response: JSONResponse = processAndScore("dummy.wav", "こんにちは。")
  json_result = response.body.decode("utf-8")

  assert "spoken_text" in json_result
  assert "reference_text" in json_result
  assert "ref_romaji" in json_result
  assert "spoken_romaji" in json_result
  assert "score" in json_result
  assert '"score":100' in json_result
  mock_transcribe.assert_called_once()
  assert mock_remove_punct.call_count == 2
  assert mock_romaji.call_count == 2
  mock_distance.assert_called_once()

@patch("src.modules.voiceRecognizer.transcribe_audio", return_value="")
@patch("src.modules.voiceRecognizer.removeKanjiPunctuation", return_value=[""])
@patch("src.modules.voiceRecognizer.convertToRomaji", return_value="")
@patch("src.modules.voiceRecognizer.Levenshtein.distance", return_value=1)
def test_process_and_score_empty_spoken(
  mock_transcribe,
  mock_remove,
  mock_romaji,
  mock_distance
):
  response = processAndScore("dummy.wav", "こんにちは。")
  result = response.body.decode()

  assert "score" in result
