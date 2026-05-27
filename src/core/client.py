"""AsyncOpenAI wrapper for DeepSeek API with streaming and tool calling."""
import json
from typing import AsyncGenerator, Callable
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from src.core.config import Config


class DeepSeekClient:
    """Manages communication with the DeepSeek API."""

    def __init__(self, config: Config):
        self.config = config
        self.client = AsyncOpenAI(**config.get_client_kwargs())
        self.model = config.default_model
        self._tools: list[dict] = []
        self._tool_handlers: dict[str, Callable] = {}
        self._last_response_headers = {}

    def register_tools(self, tools: list[dict], handlers: dict[str, Callable]):
        self._tools = tools
        self._tool_handlers = handlers

    async def stream_chat(
        self,
        messages: list[dict],
    ) -> AsyncGenerator[dict, None]:
        """Stream a chat response, yielding content chunks and tool calls."""
        kwargs = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        if self._tools:
            kwargs["tools"] = self._tools
            kwargs["tool_choice"] = "auto"

        try:
            stream = await self.client.chat.completions.create(**kwargs)
        except Exception as e:
            yield {"type": "error", "content": str(e)}
            return

        tool_calls_buffer: dict[int, dict] = {}
        finish_reason = None

        async for chunk in stream:
            if hasattr(chunk, "usage") and chunk.usage:
                yield {"type": "usage", "prompt_tokens": chunk.usage.prompt_tokens or 0,
                       "completion_tokens": chunk.usage.completion_tokens or 0}

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            finish_reason = chunk.choices[0].finish_reason

            # Reasoning content (R1 model)
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                yield {"type": "reasoning", "content": delta.reasoning_content}

            # Regular content
            if delta.content:
                yield {"type": "content", "content": delta.content}

            # Tool calls
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx not in tool_calls_buffer:
                        tool_calls_buffer[idx] = {
                            "id": tc.id or "",
                            "function": {"name": "", "arguments": ""},
                        }
                    if tc.id:
                        tool_calls_buffer[idx]["id"] = tc.id
                    if tc.function:
                        if tc.function.name:
                            tool_calls_buffer[idx]["function"]["name"] += tc.function.name
                        if tc.function.arguments:
                            tool_calls_buffer[idx]["function"]["arguments"] += tc.function.arguments

        # Process tool calls if any
        if finish_reason == "tool_calls" and tool_calls_buffer:
            for tc in tool_calls_buffer.values():
                tool_name = tc["function"]["name"]
                try:
                    tool_args = json.loads(tc["function"]["arguments"])
                except json.JSONDecodeError:
                    tool_args = {}
                yield {
                    "type": "tool_call",
                    "id": tc["id"],
                    "name": tool_name,
                    "arguments": tool_args,
                }

                # Execute tool
                handler = self._tool_handlers.get(tool_name)
                if handler:
                    try:
                        result = handler(**tool_args)
                        yield {"type": "tool_result", "id": tc["id"],
                               "name": tool_name, "content": str(result)}
                    except Exception as e:
                        yield {"type": "tool_result", "id": tc["id"],
                               "name": tool_name, "content": f"Error: {e}"}
                else:
                    yield {"type": "tool_result", "id": tc["id"],
                           "name": tool_name, "content": f"Unknown tool: {tool_name}"}

    async def simple_chat(self, messages: list[dict]) -> str:
        """Non-streaming chat for tool call follow-ups."""
        try:
            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            return f"Error: {e}"
