import pytest
import requests
from unittest.mock import patch, MagicMock

from src.connectors.hugginFaceConnector import aiPromptConnector

input_payload = {
  "model": "test-model",
  "messages": [
    {
        "role": "user",
        "content": "Hello, how are you?",
    }
  ]
}

@pytest.mark.asyncio
async def test_ai_prompt_connector_success():
  mock_response = {
    "choices": [
      {"message": {"content": "Hello, how are you?"}}
    ]
  }

  with patch("requests.post") as mock_post:
    mock_post.return_value = MagicMock(
      status_code=200,
      json=lambda: mock_response,
      raise_for_status=lambda: None
    )

    result = await aiPromptConnector(input_payload)

    assert result == "Hello, how are you?"
    mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_ai_prompt_connector_bad_format():
  bad_response = {"unexpected": "data"}

  with patch("requests.post") as mock_post:
    mock_post.return_value = MagicMock(
      status_code=200,
      json=lambda: bad_response,
      raise_for_status=lambda: None
    )

    with pytest.raises(ValueError):
      await aiPromptConnector(input_payload)


@pytest.mark.asyncio
async def test_ai_prompt_connector_http_error():
  with patch("requests.post") as mock_post:
    def raise_err():
      raise requests.exceptions.HTTPError("API failure")

    mock_post.return_value = MagicMock(
      raise_for_status=raise_err
    )

    with pytest.raises(requests.exceptions.HTTPError):
      await aiPromptConnector(input_payload)
