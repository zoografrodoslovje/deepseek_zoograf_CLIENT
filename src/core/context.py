"""Context Management - Token Counting and Window Management"""

import asyncio
from typing import Any, Optional
from .client import DeepSeekClient


class ContextManager:
    """Manages conversation context and token usage."""

    def __init__(self, client: DeepSeekClient):
        """Initialize context manager with a DeepSeekClient.

        Args:
            client: DeepSeek API client instance
        """
        self._client = client
        self._messages: list[dict[str, Any]] = []
        self._token_count: int = 0

    @property
    def messages(self) -> list[dict[str, Any]]:
        """Get current message history."""
        return self._messages.copy()

    @property
    def token_count(self) -> int:
        """Get approximate token count."""
        return self._token_count

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history.

        Args:
            role: Message role ('user', 'assistant', 'tool', 'system')
            content: Message content
        """
        self._messages.append({"role": role, "content": content})
        # Rough token estimation (1 token ≈ 4 characters for ASCII)
        self._token_count += len(content) // 4

    async def check_context_limit(self) -> tuple[bool, int]:
        """Check if context limit is approached.

        Returns:
            Tuple of (is_within_limit, remaining_tokens)
        """
        stats = await self._client.get_usage_stats()
        remaining = stats["remaining"]
        return (remaining > 0, remaining)

    async def summarize_old_messages(self) -> None:
        """Summarize older messages to free up context space."""
        if len(self._messages) < 3:
            return

        # Keep the last 2 user/assistant pairs
        keep_last = 4
        messages_to_summarize = self._messages[:-keep_last]

        if not messages_to_summarize:
            return

        system_prompt = {
            "role": "system",
            "content": "Summarize this conversation history into brief bullet points.",
        }

        summary_content = "\n".join(
            f"- {m['role']}: {m['content']}" for m in messages_to_summarize
        )

        try:
            response = await self._client.chat_complete(
                messages=[system_prompt, {"role": "user", "content": summary_content}]
            )

            new_system_message = {
                "role": "system",
                "content": f"Conversation history summarized:\n{response['content']}",
            }

            # Update messages
            self._messages = [new_system_message] + self._messages[-keep_last:]
            self._token_count = len(summary_content) // 4

        except Exception as e:
            print(f"Error summarizing context: {e}")

    async def get_messages_for_api(self) -> list[dict[str, Any]]:
        """Prepare messages for API call with context management."""
        # Check if we need to summarize
        within_limit, _ = await self.check_context_limit()

        if not within_limit:
            await self.summarize_old_messages()

        return self.messages.copy()

    async def clear(self) -> None:
        """Clear all message history."""
        self._messages.clear()
        self._token_count = 0

    async def add_system_message(self, content: str) -> None:
        """Add a system-level instruction."""
        self._messages.insert(0, {"role": "system", "content": content})
        self._token_count += len(content) // 4
