"""Unit Tests for Context Management"""

import pytest


class TestContextManager:
    """Tests for ContextManager class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        return MagicMock()

    def test_add_message(self, mock_client):
        """Test adding messages to context."""
        from src.core.context import ContextManager

        manager = ContextManager(mock_client)
        manager.add_message("user", "Hello")
        manager.add_message("assistant", "Hi!")

        assert len(manager.messages) == 2
        assert manager.messages[0]["role"] == "user"

    def test_clear(self, mock_client):
        """Test clearing all messages."""
        from src.core.context import ContextManager

        manager = ContextManager(mock_client)
        manager.add_message("user", "Test")
        manager.clear()

        assert len(manager.messages) == 0

    @pytest.mark.asyncio
    async def test_check_context_limit(self, mock_client):
        """Test checking if within token limits."""
        from src.core.context import ContextManager

        mock_client.get_usage_stats = AsyncMock(
            return_value={"tokens_used": 100, "max_tokens": 64000, "remaining": 63900}
        )

        manager = ContextManager(mock_client)
        within_limit, remaining = await manager.check_context_limit()

        assert within_limit is True
        assert remaining > 0
