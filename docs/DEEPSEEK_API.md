# DeepSeek API Integration Guide

## Overview

DeepSeek provides an API that is fully compatible with the OpenAI SDK. This means we can use the official `openai` Python package by simply changing the `base_url`.

## 1. Basic Chat Completion (Streaming)

### Setup Client

```python
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)
```

### Stream Response

```python
async def stream_response(messages):
    stream = await client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True,
    )
    
    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
```

### Usage Example

```python
from core.client import DeepSeekClient
from core.context import ContextManager

client = DeepSeekClient()
context = ContextManager(client)

context.add_message("user", "Write a Python function")
context.add_message("assistant", "Of course! Here's a simple example:")

async for chunk_type, chunk_data in client.chat_stream(context.messages):
    if chunk_type == "content":
        print(chunk_data, end="", flush=True)
```

## 2. Tool Calling (Function Calling)

DeepSeek CLI uses tool calling to enable agentic behavior.

### Define Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a local file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative or absolute path to the file."
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Execute a shell command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Shell command to execute"
                    }
                },
                "required": ["command"]
            }
        }
    }
]
```

### Make Request with Tools

```python
response = await client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message
```

### Handle Tool Calls in Loop

```python
if message.tool_calls:
    for tool_call in message.tool_calls:
        # 1. Parse arguments
        args = json.loads(tool_call.function.arguments)
        
        # 2. Execute local function
        result = execute_local_tool(tool_call.function.name, args)
        
        # 3. Append tool result to messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })
    
    # 4. Call API again to get final answer
    final_response = await client.chat.completions.create(...)
```

## 3. Using DeepSeek Reasoner (R1)

For complex coding tasks, switch to the reasoning model.

### Model Configuration

```python
model = "deepseek-reasoner"  # For R1 reasoning capabilities
```

### Handle Reasoning Content

```python
async for chunk in stream:
    delta = chunk.choices[0].delta
    
    # Handle reasoning content (R1 specific)
    if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
        yield ("reasoning", delta.reasoning_content)
        
    # Handle final content
    if delta.content:
        yield ("content", delta.content)
```

### Rendering Reasoning Output

The reasoning output shows the AI's thought process before giving final answer. Style it distinctly in your UI:

```css
/* Textual CSS styling */
.reasoning-output {
    color: $text-muted;
    opacity: 0.7;
    border-left: 2px dashed $border-default;
    padding-left: 1em;
}

.final-output {
    color: $text-primary;
    font-weight: bold;
}
```

## 4. Rate Limits and Best Practices

### Check Rate Limit Headers

```python
headers = response.headers
rate_limit = headers.get("x-ratelimit-limit-requests")
remaining = headers.get("x-ratelimit-remaining-requests")
```

### Context Window Sizes

| Model | Context Window | Max Output |
|-------|---------------|------------|
| `deepseek-chat` | 64k tokens | Depends on input |
| `deepseek-reasoner` | 64k tokens | 8k tokens |

### Caching Strategy

DeepSeek supports automatic context caching. To maximize cache hits:

1. **Keep system prompt at start** of messages array
2. **Use consistent prefixes** for repeated prompts
3. **Avoid unnecessary variation** in static content

```python
# Optimal message structure for caching
messages = [
    {"role": "system", "content": "[Your fixed system prompt]"},
    {"role": "user", "content": "[Dynamic user query]"},
]
```

### Error Handling Best Practices

```python
try:
    stream = await client.chat.completions.create(...)
    async for chunk in stream:
        process_chunk(chunk)
except RateLimitError:
    # Wait and retry
    await asyncio.sleep(exponential_backoff(attempt))
except NotFoundError:
    # Model doesn't exist - fallback
    model = "deepseek-chat"
except Exception as e:
    # Log and handle gracefully
    logger.error(f"API error: {e}")
    return None
```

## 5. Complete Implementation Example

```python
# Full streaming handler with tool support
async def handle_deepseek_chat(user_input: str) -> str:
    from core.client import DeepSeekClient
    from core.context import ContextManager
    from core.config import Config
    from tools.registry import get_all_tools
    
    client = DeepSeekClient()
    context = ContextManager(client)
    
    # Add user message
    context.add_message("user", user_input)
    messages = context.messages
    
    # Get available tools
    tools = get_all_tools()
    
    full_response = ""
    async for chunk_type, chunk_data in client.chat_stream(messages, tools=tools):
        if chunk_type == "tool_call":
            # Execute tool and continue
            result = execute_tool(chunk_data["name"], chunk_data["arguments"])
            messages.append({
                "role": "tool",
                "tool_call_id": chunk_data["id"],
                "content": result
            })
            continue
            
        if chunk_type == "content":
            full_response += chunk_data
            yield chunk_data
    
    # Store assistant response
    context.add_message("assistant", full_response)
    
    return full_response
```

## 6. API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/chat/completions` | POST | Send chat messages |
| `/v1/models` | GET | List available models |
| `/v1/assistants` | POST/GET | (If supported) Assistant creation |

Base URL: `https://api.deepseek.com/v1`
