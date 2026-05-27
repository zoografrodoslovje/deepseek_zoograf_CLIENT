"""DeepSeek API Client - AsyncOpenAI Wrapper"""

import os
from typing import Any, AsyncGenerator, Optional
from openai import AsyncOpenAI, NotFoundError, RateLimitError
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from .config import Config

API_RETRIES = 3


class DeepSeekClient:
    """Asynchronous client for DeepSeek API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str | None = None,
    ):
        """Initialize the DeepSeek client.

        Args:
            api_key: API key (defaults to DEEPSEEK_API_KEY env var)
            base_url: Base URL (defaults to DEEPSEEK_BASE_URL env var)
            model: Default model to use
        """
        self._api_key = api_key or Config.DEEPSEEK_API_KEY
        self._base_url = base_url or Config.DEEPSEEK_BASE_URL
        self._model = model or Config.DEFAULT_MODEL

        if not self._api_key:
            raise ValueError("API key is required")

        self._client = AsyncOpenAI(
            api_key=self._api_key,
            base_url=self._base_url,
        )

        # Track context tokens
        self._tokens_used: int = 0
        self._last_response_time: float | None = None

    @property
    def current_model(self) -> str:
        """Get current model name."""
        return self._model

    @property
    def tokens_used(self) -> int:
        """Get total tokens used in current session."""
        return self._tokens_used

    @property
    def config(self) -> Config:
        """Get application configuration."""
        return Config

    async def chat_stream(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        tools: list[dict] | None = None,
    ) -> AsyncGenerator[tuple[str, Any], None]:
        """Stream chat completion response from DeepSeek.

        Args:
            messages: List of chat messages
            model: Model to use (overrides default)
            tools: Optional function calling tools schema

        Yields:
            Tuple of (chunk_type, content):
            - ('content', str) for regular content
            - ('reasoning', str) for reasoning content (R1 models)
            - ('tool_call', dict) for tool call information
        """
        model = model or self._model
        attempt = 0

        while attempt < API_RETRIES:
            try:
                params: dict[str, Any] = {
                    "model": model,
                    "messages": messages,
                    "stream": True,
                    "temperature": 0.7,
                }

                if tools:
                    params["tools"] = tools
                    params["tool_choice"] = "auto"

                stream = await self._client.chat.completions.create(**params)

                async for chunk in stream:
                    choices = chunk.choices
                    if not choices:
                        continue

                    delta = choices[0].delta
                    content = delta.content or ""
                    reasoning_content = getattr(delta, "reasoning_content", "") or ""

                    # Handle reasoning content first (for R1 models)
                    if reasoning_content:
                        yield ("reasoning", reasoning_content)

                    if content:
                        yield ("content", content)

                    # Handle tool calls
                    if delta.tool_calls:
                        for tool_call in delta.tool_calls:
                            if tool_call.id and hasattr(tool_call.function, "name"):
                                args = getattr(tool_call.function, "arguments", None)
                                yield (
                                    "tool_call",
                                    {
                                        "id": tool_call.id,
                                        "name": tool_call.function.name,
                                        "arguments": args,
                                    },
                                )

                    self._tokens_used += chunk.usage.prompt_tokens
                    self._last_response_time = chunk.created

                break

            except RateLimitError as e:
                attempt += 1
                wait_time = min(2**attempt * 2, 30)  # Exponential backoff
                print(f"Rate limited. Retrying in {wait_time}s... ({attempt}/{API_RETRIES})")
                await asyncio.sleep(wait_time)
            except Exception as e:
                print(f"API error: {e}")
                raise

    async def chat_complete(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        tools: list[dict] | None = None,
    ) -> dict[str, Any]:
        """Get a complete chat response (non-streaming).

        Args:
            messages: List of chat messages
            model: Model to use (overrides default)
            tools: Optional function calling tools schema

        Returns:
            Complete completion response dictionary
        """
        response = await self._chat_complete(messages, model, tools)
        return {
            "content": response.choices[0].message.content,
            "role": response.choices[0].message.role,
            "tool_calls": [
                {
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                }
                for tc in (response.choices[0].message.tool_calls or [])
            ],
        }

    async def _chat_complete(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        tools: list[dict] | None = None,
    ) -> Any:
        """Internal method for non-streaming completion."""
        model = model or self._model

        params: dict[str, Any] = {"model": model, "messages": messages}
        if tools:
            params["tools"] = tools
            params["tool_choice"] = "auto"

        response = await self._client.chat.completions.create(**params)

        self._tokens_used += response.usage.total_tokens

        return response

    async def get_usage_stats(self) -> dict[str, int]:
        """Get current usage statistics."""
        return {
            "tokens_used": self._tokens_used,
            "max_tokens": Config.MAX_CONTEXT_TOKENS,
            "remaining": Config.MAX_CONTEXT_TOKENS - self._tokens_used,
        }
