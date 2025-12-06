from unittest.mock import patch

from src.modules.utils import (
  generatePromptByLevel,
  convertToRomaji,
  translateToEng,
  removeKanjiPunctuation
)

@patch("src.modules.utils.random.choice", return_value="食べ物")
def test_generate_prompt_basic(mock_choice):
  prompt, topic = generatePromptByLevel("basic")

  assert topic == "食べ物"
  assert "短くて簡単な日本語の文" in prompt
  assert "文:" in prompt


@patch("src.modules.utils.random.choice", return_value="学校")
def test_generate_prompt_intermediate(mock_choice):
  prompt, topic = generatePromptByLevel("intermediate")

  assert topic == "学校"
  assert "自然な会話文" in prompt
  assert "文:" in prompt


@patch("src.modules.utils.random.choice", return_value="仕事")
def test_generate_prompt_advanced(mock_choice):
  prompt, topic = generatePromptByLevel("advanced")

  assert topic == "仕事"
  assert "高度な語彙と文法" in prompt
  assert "文:" in prompt


@patch("src.modules.utils.kakasiLib.convert")
def test_convert_to_romaji(mock_convert):
  mock_convert.return_value = [
      {"hepburn": "konnichi"},
      {"hepburn": "wa"}
  ]

  result = convertToRomaji("こんにちは")
  assert result == "konnichi wa"


@patch("src.modules.utils.GoogleTranslator")
def test_translate_to_eng(mock_translator):
  instance = mock_translator.return_value
  instance.translate.return_value = "Hello"

  result = translateToEng("こんにちは")
  assert result == "Hello"

  instance.translate.assert_called_once_with("こんにちは")


@patch("src.modules.utils.kanjiConverter.convert")
def test_remove_kanji_punctuation(mock_convert):
  mock_convert.return_value = [
      {"hepburn": "a"},
      {"hepburn": "ri"},
      {"hepburn": "ga"},
      {"hepburn": "to"}
  ]

  result = removeKanjiPunctuation("ありがとう。")
  assert result == ["a", "r", "i", "g", "a", "t", "o"]  # list of chars

  mock_convert.assert_called_once()
