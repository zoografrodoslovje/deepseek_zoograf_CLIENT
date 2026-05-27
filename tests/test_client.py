"""Unit Tests for Client Module"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Import module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestDeepSeekClient:
    """Tests for DeepSeekClient class."""

    @pytest.fixture
    def mock_config(self):
        """Mock configuration."""
        with patch("src.core.client.Config") as mock_config:
            mock_config.DEEPSEEK_API_KEY = "test-api-key"
            mock_config.DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
            yield mock_config

    @pytest.mark.asyncio
    async def test_initialization_with_api_key(self, mock_config):
        """Test client initialization with valid API key."""
        from core.client import DeepSeekClient

        client = DeepSeekClient()
        assert client is not None
        assert client.config.DEEPSEEK_API_KEY == "test-api-key"

    @pytest.mark.asyncio
    async def test_stream_response(self, mock_config):
        """Test streaming chat response."""
        from core.client import DeepSeekClient

        client = DeepSeekClient()

        # Mock the stream response
        mock_chunk = MagicMock()
        mock_chunk.choices[0].delta.content = "Hello"
        mock_chunk.usage.prompt_tokens = 10

        async def mock_stream():
            yield mock_chunk

        with patch.object(client._client.chat.completions, "create", return_value=mock_stream()):
            chunks = []
            async for chunk_type, chunk_data in client.chat_stream([]):
                if chunk_type == "content":
                    chunks.append(chunk_data)

            assert "".join(chunks) == "Hello"

    def test_get_model_options(self, mock_config):
        """Test getting available models."""
        from core.client import DeepSeekClient
        from core.config import Config

        options = Config.get_model_options()
        assert "deepseek-chat" in options
        assert "deepseek-reasoner" in options


@pytest.fixture
def sample_messages():
    """Sample conversation messages."""
    return [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
