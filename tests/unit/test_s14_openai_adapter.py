"""Tests unitaires — S14 OpenAI LLM Adapter.

Couvre :
- Génération d'une réponse via OpenAI avec mapping correct du payload.
- Récupération correcte du token count (usage).
- Fallback/Exception handling en cas d'erreur API.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from callibr_contracts import ModelRequest
from callibr_conversation.adapters import OpenAIAdapter


class TestOpenAIAdapter:
    @patch("openai.OpenAI")
    def test_generate_maps_request_correctly_and_returns_model_response(
        self, mock_openai_class
    ) -> None:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Mock completion response
        mock_choice = MagicMock()
        mock_choice.message.content = "Bonjour, ceci est la réponse."
        mock_choice.finish_reason = "stop"

        mock_usage = MagicMock()
        mock_usage.prompt_tokens = 15
        mock_usage.completion_tokens = 10

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.usage = mock_usage

        mock_client.chat.completions.create.return_value = mock_response

        adapter = OpenAIAdapter(api_key="sk-test-123", model="gpt-test-model")

        request = ModelRequest(
            system_prompt="Tu es un assistant SAV.",
            messages=[{"role": "user", "content": "J'ai un problème."}],
            temperature=0.5,
            max_tokens=100,
        )

        result = adapter.generate(request)

        # Verify OpenAI API call
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-test-model",
            messages=[
                {"role": "system", "content": "Tu es un assistant SAV."},
                {"role": "user", "content": "J'ai un problème."},
            ],
            temperature=0.5,
            max_tokens=100,
        )

        # Verify returned ModelResponse
        assert result.content == "Bonjour, ceci est la réponse."
        assert result.model_id == "gpt-test-model"
        assert result.finish_reason == "stop"
        assert result.usage["prompt_tokens"] == 15
        assert result.usage["completion_tokens"] == 10

        assert adapter.call_count == 1
        assert adapter.last_request == request

    @patch("openai.OpenAI")
    def test_generate_raises_error_on_api_failure(self, mock_openai_class) -> None:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Simulate API Error
        mock_client.chat.completions.create.side_effect = Exception("API Timeout")

        adapter = OpenAIAdapter(api_key="sk-test-123")

        with pytest.raises(Exception, match="API Timeout"):
            adapter.generate(ModelRequest())

    @patch("openai.OpenAI")
    def test_health_check_success(self, mock_openai_class) -> None:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # list() will not raise -> success
        adapter = OpenAIAdapter(api_key="sk-test-123")
        assert adapter.health() is True

    @patch("openai.OpenAI")
    def test_health_check_failure(self, mock_openai_class) -> None:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_client.models.list.side_effect = Exception("Auth Error")

        adapter = OpenAIAdapter(api_key="sk-invalid")
        assert adapter.health() is False
