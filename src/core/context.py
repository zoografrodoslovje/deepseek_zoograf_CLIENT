"""Token counting and context window management."""
import tiktoken
from typing import Optional


class ContextManager:
    """Tracks token usage and manages context window limits."""

    def __init__(self, max_tokens: int = 64000, model: str = "deepseek-chat"):
        self.max_tokens = max_tokens
        self.summary_threshold = int(max_tokens * 0.75)
        self._prompt_tokens = 0
        self._completion_tokens = 0
        try:
            self._tokenizer = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self._tokenizer = None

    def count_tokens(self, text: str) -> int:
        """Approximate token count."""
        if self._tokenizer:
            return len(self._tokenizer.encode(text))
        return len(text) // 4  # rough estimate

    def count_messages_tokens(self, messages: list[dict]) -> int:
        """Count tokens in a list of messages (approximate)."""
        total = 0
        for msg in messages:
            total += self.count_tokens(str(msg.get("content", "")))
            total += self.count_tokens(str(msg.get("role", "")))
            if msg.get("name"):
                total += self.count_tokens(msg["name"])
            # Tool calls overhead
            if msg.get("tool_calls"):
                total += 20
            if msg.get("tool_call_id"):
                total += 10
        # Per-message overhead (~4 tokens per message)
        total += len(messages) * 4
        return total

    def add_usage(self, prompt_tokens: int, completion_tokens: int):
        self._prompt_tokens += prompt_tokens
        self._completion_tokens += completion_tokens

    @property
    def total_tokens(self) -> int:
        return self._prompt_tokens + self._completion_tokens

    def should_summarize(self, messages: list[dict]) -> bool:
        """Check if approaching context limit."""
        current = self.count_messages_tokens(messages)
        return current > self.summary_threshold

    def needs_truncation(self, messages: list[dict]) -> bool:
        current = self.count_messages_tokens(messages)
        return current > self.max_tokens - 2000  # leave room for response

    def truncate_messages(self, messages: list[dict]) -> list[dict]:
        """Truncate oldest messages while keeping system prompt."""
        if not self.needs_truncation(messages):
            return messages

        # Keep system prompt (first message if it's system)
        keep = []
        rest = list(messages)
        if rest and rest[0].get("role") == "system":
            keep.append(rest.pop(0))

        # Remove oldest user/assistant pairs until under limit
        while rest and self.count_messages_tokens(keep + rest) > self.max_tokens - 2000:
            rest.pop(0)

        return keep + rest

    def reset(self):
        self._prompt_tokens = 0
        self._completion_tokens = 0
