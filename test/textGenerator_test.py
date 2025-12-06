import pytest
import json
from unittest.mock import patch, AsyncMock

from src.modules.textGenerator import generatePracticeText, generatePracticeTextLocalModel

@pytest.mark.asyncio
@patch("src.modules.textGenerator.translateToEng", return_value="Hello")
@patch("src.modules.textGenerator.convertToRomaji", return_value="konnichiha")
@patch("src.modules.textGenerator.aiPromptConnector", new_callable=AsyncMock)
@patch("src.modules.textGenerator.generatePromptByLevel", return_value=("prompt", "食べ物"))
async def test_generate_practice_text_api_success(
    mock_prompt,
    mock_api,
    mock_romaji,
    mock_translate
):
    mock_api.return_value = "こんにちは。"

    response = await generatePracticeText("basic")
    result = json.loads(response.body.decode())

    assert result["source"] == "api"
    assert result["practice_text"] == "こんにちは。"
    assert result["romaji"] == "konnichiha"
    assert result["translation"] == "Hello"
    assert result["topic"] == "食べ物"


@pytest.mark.asyncio
@patch("src.modules.textGenerator.translateToEng", return_value="Hello")
@patch("src.modules.textGenerator.convertToRomaji", return_value="konnichiha")
@patch("src.modules.textGenerator.generatePracticeTextLocalModel", return_value="おはよう。")
@patch("src.modules.textGenerator.aiPromptConnector", side_effect=Exception("API DOWN"))
@patch("src.modules.textGenerator.generatePromptByLevel", return_value=("prompt", "天気"))
async def test_generate_practice_text_local_fallback(
    mock_prompt,
    mock_api,
    mock_local,
    mock_romaji,
    mock_translate
):
    response = await generatePracticeText("basic")
    result = json.loads(response.body.decode())

    assert result["source"] == "local_model"
    assert result["practice_text"] == "おはよう。"
    assert result["romaji"] == "konnichiha"
    assert result["translation"] == "Hello"
    assert result["topic"] == "天気"


@pytest.mark.asyncio
@patch("src.modules.textGenerator.aiPromptConnector", side_effect=Exception("API FAIL"))
@patch("src.modules.textGenerator.generatePracticeTextLocalModel", side_effect=Exception("LOCAL FAIL"))
@patch("src.modules.textGenerator.generatePromptByLevel", return_value=("prompt", "友達"))
async def test_generate_practice_text_both_fail(
    mock_prompt,
    mock_api,
    mock_local
):
    response = await generatePracticeText("basic")
    result = json.loads(response.body.decode())

    assert response.status_code == 500
    assert result["error"] == "Both API and local model generation failed"


@pytest.mark.asyncio
@patch("src.modules.textGenerator.aiPromptConnector", new_callable=AsyncMock)
@patch("src.modules.textGenerator.convertToRomaji", side_effect=Exception("ROMAJI ERROR"))
@patch("src.modules.textGenerator.translateToEng", return_value="Test")
@patch("src.modules.textGenerator.generatePromptByLevel", return_value=("prompt", "映画"))
async def test_generate_practice_text_romaji_fail(
    mock_prompt,
    mock_translate,
    mock_romaji,
    mock_api
):
    mock_api.return_value = "映画を見る。"

    response = await generatePracticeText("intermediate")
    data = json.loads(response.body.decode())

    # Romaji should fallback to empty string
    assert data["romaji"] == ""
    assert data["translation"] == "Test"


@pytest.mark.asyncio
@patch("src.modules.textGenerator.aiPromptConnector", new_callable=AsyncMock)
@patch("src.modules.textGenerator.convertToRomaji", return_value="eiga o miru")
@patch("src.modules.textGenerator.translateToEng", side_effect=Exception("TRANSLATE ERROR"))
@patch("src.modules.textGenerator.generatePromptByLevel", return_value=("prompt", "音楽"))
async def test_generate_practice_text_translation_fail(
    mock_prompt,
    mock_translate,
    mock_romaji,
    mock_api
):
    mock_api.return_value = "音楽が好き。"

    response = await generatePracticeText("advanced")
    data = json.loads(response.body.decode())

    assert data["translation"] == ""
    assert data["romaji"] == "eiga o miru"
