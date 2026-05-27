# 🏗️ DeepSeek Zoograf Client — Architecture

Technical overview of the codebase for contributors and curious users.

---

## High-Level Architecture

```
┌────────────────────────────────────────────────────────────┐
│                       main.py                              │
│                  (Entry point)                             │
├────────────────────────────────────────────────────────────┤
│                        │                                   │
│              ┌─────────▼──────────┐                       │
│              │    src/ui/app.py    │                       │
│              │   (DeepSeekTUI)     │   Textual App         │
│              │   Main App class    │                       │
│              └──┬──┬──┬──┬──┬─────┘                       │
│                 │  │  │  │  │                              │
│    ┌────────────┘  │  │  │  └──────────────┐              │
│    ▼               ▼  ▼  ▼                  ▼              │
│ ┌───────┐ ┌─────────┐ ┌──────────┐ ┌────────────┐        │
│ │ Chat  │ │ Input   │ │ Status   │ │ Theme +    │        │
│ │ View  │ │ Area    │ │ Bar      │ │ CSS        │        │
│ └───────┘ └─────────┘ └──────────┘ └────────────┘        │
│    │           │           │                               │
│    ▼           ▼           ▼                               │
│ ┌────────────────────────────────────────────────────┐     │
│ │                  Core Layer                        │     │
│ │  ┌────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐   │     │
│ │  │ Client │ │ Config │ │ Context │ │ Session  │   │     │
│ │  └───┬────┘ └────────┘ └─────────┘ └──────────┘   │     │
│ └──────┼─────────────────────────────────────────────┘     │
│        │                                                    │
│        ▼                                                    │
│ ┌────────────────────────────────────────────────────┐     │
│ │                 Tools Layer                        │     │
│ │  ┌──────────┐ ┌──────────┐ ┌───────┐ ┌─────────┐  │     │
│ │  │ Registry │ │ Filesys  │ │ Shell │ │ Search  │  │     │
│ │  └──────────┘ └──────────┘ └───────┘ └─────────┘  │     │
│ └────────────────────────────────────────────────────┘     │
│                                                             │
│                    DeepSeek API (external)                  │
│                    platform.deepseek.com                    │
└────────────────────────────────────────────────────────────┘
```

---

## Layer Breakdown

### 1. Entry Point (`main.py`)

Minimal bootstrap that:
- Adds `src/` to Python path
- Imports and runs the Textual app
- Handles `--version` flag
- Catches fatal errors gracefully

### 2. UI Layer (`src/ui/`)

Uses **Textual** (Python TUI framework) for the terminal interface.

#### `app.py` — `DeepSeekTUI` (Main App)
- **Inherits:** `textual.app.App`
- **Responsibilities:**
  - Compose UI widgets into layout
  - Handle keyboard bindings (`Ctrl+C`, `Ctrl+L`, etc.)
  - Manage API streaming with tool-call loop
  - Coordinate between chat, input, and status bar
  - Register theme and manage app state
- **Key Methods:**
  - `compose()` — Declare widget layout
  - `on_mount()` — Initialize theme, check config
  - `on_input_area_submitted()` — Receive user input, start API stream
  - `_process_stream()` — Stream API response, handle tool calls in loop

#### `chat_view.py` — `ChatView`
- **Inherits:** `textual.widget.Widget`
- **Responsibilities:**
  - Display conversation history with Rich renderables
  - Stream partial responses with cursor indicator (▊)
  - Convert messages to Rich Markdown panels
- **Key Classes:**
  - `ChatMessage` — Stores role, content, renderable; converts to Rich Panel/Markdown
  - `ChatView` — Manages message list, streaming state, RichLog container

#### `input_area.py` — `InputArea`
- **Inherits:** `textual.widget.Widget`
- **Responsibilities:**
  - Multi-line text input (TextArea widget)
  - Command history with ↑/↓ navigation
  - Submit message on Enter (Shift+Enter for newline)
  - Auto-height adjustment based on content
- **Custom Message:** `Submitted(text)` — Posted when user hits Enter

#### `status_bar.py` — `StatusBar`
- **Inherits:** `textual.widget.Widget`
- **Responsibilities:**
  - Display model name (left side)
  - Show token usage with percentage (right side)
  - API connection indicator (● green / ○ red)

#### `theme.py` — HERO UI POR Light Theme
- **Exports:**
  - `HERO_UI_POR_LIGHT` — Textual Theme object with color palette
  - `APP_CSS` — Textual CSS string for the entire app layout
- **Color Palette:**
  - Primary: `#2563EB` (blue)
  - Secondary: `#7C3AED` (purple)
  - Accent: `#F59E0B` (amber)
  - Background: `#FAFAF8` (off-white)
  - Surface: `#FFFFFF` (white)

### 3. Core Layer (`src/core/`)

#### `client.py` — `DeepSeekClient`
- **Inherits:** Wraps `openai.AsyncOpenAI`
- **Responsibilities:**
  - Async streaming chat via `stream_chat()` generator
  - Tool call detection and execution
  - Handles reasoning content (deepseek-reasoner model)
  - Tracks token usage from stream
- **Stream Events:**
  - `{"type": "content", "content": "..."}` — Text chunk
  - `{"type": "reasoning", "content": "..."}` — Reasoning trace
  - `{"type": "tool_call", "id": "...", "name": "...", "arguments": {...}}`
  - `{"type": "tool_result", "id": "...", "name": "...", "content": "..."}`
  - `{"type": "usage", "prompt_tokens": N, "completion_tokens": N}`
  - `{"type": "error", "content": "..."}`

#### `config.py` — `Config`
- **Inherits:** Plain class
- **Responsibilities:**
  - Load `.env` file with `python-dotenv`
  - Provide typed access to configuration
  - Validate API key presence

#### `context.py` — `ContextManager`
- **Responsibilities:**
  - Token counting with `tiktoken` (cl100k_base)
  - Context window management
  - Message truncation when approaching limits (75% threshold)
  - Track total tokens used in session

#### `session.py` — `SessionManager`
- **Responsibilities:**
  - Save conversations as JSON to `~/.ds-cli/sessions/`
  - Load and list past sessions
  - Delete individual sessions
  - Timestamp-based session IDs

### 4. Tools Layer (`src/tools/`)

#### `registry.py` — Tool Registration
- **Exports:**
  - `get_tool_definitions()` — OpenAI function-calling schemas (5 tools)
  - `get_tool_handlers()` — Map tool names → Python functions

#### `filesystem.py` — File Operations
- **`read_file(path)`** — Read text file, return content with line count
- **`write_file(path, content)`** — Write file, create parent dirs
- **`list_directory(path, recursive)`** — List files with emoji icons and sizes

#### `shell.py` — Command Execution
- **`execute_command(command, description)`** — Requests confirmation via exception
- **`CommandRequiresConfirmation`** — Custom exception for UI to catch
- **`execute_command_approved(command)`** — Async execution with 60s timeout
- **Architecture Note:** The `execute_command` function raises an exception to signal the UI layer, which displays the command for transparency and then calls `execute_command_approved`.

#### `search.py` — Codebase Search
- **`search_codebase(pattern, path, file_glob)`** — Uses ripgrep (preferred) or grep
- 30s timeout, results limited to 200 lines
- Reports match count when truncated

### 5. Utilities (`src/utils/`)

#### `markdown.py` — Markdown Rendering
- Thin wrapper around Rich's Markdown and Syntax renderers
- Graceful fallback if rendering fails

#### `logger.py` — Logging
- Configures structured logging to stderr
- Timestamped log format: `[HH:MM:SS] LEVEL name: message`

---

## Data Flow

### Chat Flow

```
1. User types message → InputArea.Submitted
2. DeepSeekTUI.on_input_area_submitted()
   ├── Adds "user" message to ChatView
   ├── Prepares API messages (system prompt + history)
   ├── Checks context limits → truncates if needed
   └── Calls _process_stream()
3. _process_stream()
   ├── Client.stream_chat() starts streaming
   ├── ChatView.start_streaming() shows cursor
   ├── For each event:
   │   ├── "content" → ChatView.update_streaming()
   │   ├── "tool_call" → Queued for execution
   │   ├── "usage" → Status bar update
   │   └── "error" → Show in chat
   ├── If tool_calls present:
   │   ├── Execute each tool
   │   ├── Show results in chat
   │   └── Call stream_chat() again with tool results
   └── ChatView.finish_streaming()
```

### Tool Call Flow

```
DeepSeek API → tool_call event
    ↓
DeepSeekTUI receives tool_calls list
    ↓
For each tool_call:
    ├── execute_command? → Show Panel with command description
    │                     → Call execute_command_approved()
    └── Other tool?      → Look up handler from registry
                          → Call handler(**arguments)
    ↓
Collect tool_results
    ↓
Append tool_results to messages
    ↓
Call stream_chat() again with updated messages
    ↓
Stream final AI response
```

---

## Dependency Graph

```
main.py
  └── src.ui.app
        ├── src.ui.chat_view → rich
        ├── src.ui.input_area → textual.widgets.TextArea
        ├── src.ui.status_bar → psutil
        ├── src.ui.theme → textual.theme.Theme
        ├── src.core.config → python-dotenv
        ├── src.core.client → openai.AsyncOpenAI
        ├── src.core.context → tiktoken
        ├── src.core.session → json, pathlib
        ├── src.tools.registry
        │     ├── src.tools.filesystem
        │     ├── src.tools.shell → asyncio
        │     └── src.tools.search → subprocess
        └── src.utils.logger → logging
```

---

## Error Handling Strategy

| Layer | Strategy |
|-------|----------|
| UI | try/except wraps all streaming, errors shown as chat messages |
| Client | Connection errors yield `{"type": "error"}` events |
| Tools | Each tool function returns error string, never raises |
| Config | `is_configured()` returns bool, graceful degraded mode |
| Input | All actions guarded by `_streaming` flag (ignore input during stream) |

---

## Extending the Client

### Adding a New Tool

1. **Create the tool function** in `src/tools/`:
   ```python
   def my_tool(param1: str, param2: int) -> str:
       """Do something useful."""
       return result
   ```

2. **Register the schema** in `src/tools/registry.py`:
   ```python
   {
       "type": "function",
       "function": {
           "name": "my_tool",
           "description": "What my tool does",
           "parameters": {"type": "object", "properties": {...}},
       },
   }
   ```

3. **Register the handler** in `get_tool_handlers()`:
   ```python
   return {
       "my_tool": my_tool,
       ...
   }
   ```

### Adding a Theme

1. Define a new `Theme` object in `src/ui/theme.py`
2. Add CSS rules to `APP_CSS`
3. Register in `app.py`'s `on_mount()`:
   ```python
   self.register_theme(MY_THEME)
   self.theme = "my-theme-name"
   ```

### Adding a Keyboard Shortcut

Add a `Binding` to the `BINDINGS` list in `app.py`:
```python
Binding("ctrl+d", "my_action", "My action"),
```
Then implement `action_my_action()` on the `DeepSeekTUI` class.
