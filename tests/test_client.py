"""Unit Tests for Client Module"""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Import module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def mock_config():
    """Mock configuration by patching Config class attributes directly."""
    with patch("core.config.Config.DEEPSEEK_API_KEY", "test-api-key"):
        with patch("core.config.Config.DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"):
            with patch("core.config.Config.DEFAULT_MODEL", "deepseek-chat"):
                yield


class TestDeepSeekClient:
    """Tests for DeepSeekClient class."""

    @pytest.mark.asyncio
    async def test_initialization_with_api_key(self, mock_config):
        """Test client initialization with valid API key."""
        from core.client import DeepSeekClient

        client = DeepSeekClient()
        assert client is not None
        assert client.current_model == "deepseek-chat"

    @pytest.mark.asyncio
    async def test_stream_response(self, mock_config):
        """Test streaming chat response."""
        from core.client import DeepSeekClient

        client = DeepSeekClient(api_key="test-key")

        # Mock chunk matching ChatCompletionChunk shape
        mock_chunk = MagicMock()
        delta = MagicMock()
        delta.content = "Hello"
        delta.reasoning_content = None
        delta.tool_calls = None
        mock_chunk.choices = [MagicMock(delta=delta)]
        mock_chunk.usage = MagicMock(prompt_tokens=10)
        mock_chunk.created = 1234567890

        async def mock_stream():
            yield mock_chunk

        # create() is awaited and must return an async iterable
        async def mock_create(*args, **kwargs):
            return mock_stream()

        with patch.object(
            client._client.chat.completions, "create", new=mock_create
        ):
            chunks = []
            async for chunk_type, chunk_data in client.chat_stream([]):
                if chunk_type == "content":
                    chunks.append(chunk_data)

            assert "".join(chunks) == "Hello"

    def test_get_model_options(self):
        """Test getting available models."""
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
