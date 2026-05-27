# System Architecture

## Overview

DeepSeek CLI Tool uses an **Event-Driven Architecture** pattern that separates concerns between:
1. User Interface (TUI)
2. Business Logic (Core)
3. External Services (API, File System, Shell)

## Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    TUI Layer (Textual)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Chat Widget  │  │ Input Area   │  │ Status Bar   │   │
│  │              │  │              │  │              │   │
│  └───────┬──────┘  └───────┬──────┘  └───────┬──────┘   │
└──────────┼──────────────────┼─────────────────┼──────────┘
           │                  │                 │
           ▼                  ▼                 ▼
┌──────────────────────────────────────────────────────────┐
│                Core Controller (Asyncio)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Message      │  │ Tool         │  │ Context      │   │
│  │ Router       │  │ Executor     │  │ Manager      │   │
│  └───────┬──────┘  └───────┬──────┘  └───────┬──────┘   │
└──────────┼──────────────────┼─────────────────┼──────────┘
           │                  │                 │
           ▼                  ▼                 ▼
┌──────────────────────────────────────────────────────────┐
│               External Interfaces                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ DeepSeek     │  │ File System  │  │ Shell        │   │
│  │ API Client   │  │ Operations   │  │ Commands     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└──────────────────────────────────────────────────────────┘
```

## Detailed Components

### 1. UI Layer (`src/ui/`)

#### `app.py` - Main Application Orchestrator
- Initializes Textual app and all widgets
- Manages event bindings and lifecycle
- Coordinates between widgets and core logic

#### `chat_view.py` - Conversation Display
- Extends Textual's ScrollableContainer
- Renders user/assistant messages with visual differentiation
- Supports streaming content updates

#### `input_area.py` - User Input Handling
- Multi-line text input widget
- History navigation (Up/Down arrows)
- Enter/Shift+Enter support for submission/newline

#### `status_bar.py` - Information Display
- Token usage counter
- Current model indicator
- Connection status indicator

### 2. Core Layer (`src/core/`)

#### `config.py` - Configuration Management
- Loads environment variables from `.env`
- Provides validation and default values
- Exposes application settings to other modules

#### `client.py` - API Communication
- AsyncOpenAI wrapper for DeepSeek API
- Handles streaming responses
- Implements retry logic for rate limits
- Tracks token usage per session

#### `context.py` - Conversation State
- Maintains message history
- Counts tokens against context window
- Triggers summarization when limit approached
- Prepares messages for API calls

#### `session.py` - Persistence Layer
- Saves/load chat histories as JSON
- Session ID generation and management
- Branching support for conversation forks

### 3. Tools Layer (`src/tools/`)

#### `registry.py` - Tool Registration
- Auto-discovers available tools
- Generates OpenAI-compatible function schemas
- Routes AI tool calls to implementations

#### `filesystem.py` - File Operations
- `read_file()`: Read file contents safely
- `write_file()`: Create/modify files with confirmation
- `list_dir()`: Directory listing

#### `shell.py` - Command Execution
- `execute_command()`: Run shell commands with timeout
- Security filters for dangerous operations
- Confirmation requirement for write/delete

#### `search.py` - Codebase Search
- `search_codebase()`: Pattern search in files
- `find_files()`: Glob pattern matching

### 4. Utils Layer (`src/utils/`)

#### `markdown.py` - Text Rendering
- Terminal-safe escape sequences
- Code block formatting with line numbers
- Message role styling

#### `logger.py` - Logging Infrastructure
- Console and optional file logging
- Configurable log levels
- Standardized logger instance

## Data Flow

### Normal Message Flow

```
User Input → InputArea → Event → App → 
    ↓
ContextManager.add_message() → Message Router
    ↓
DeepSeekClient.chat_stream() → Streaming Response
    ↓
Tool Detection? → Yes: Execute Tool → Add Result → Repeat
    ↓ No
Update ChatWidget → Add to History → Ready for Next
```

### Tool Call Flow

```
AI Request with tool_calls → Message Router
    ↓
Parse tool name + arguments → Registry.get_tool_executor()
    ↓
Execute local function → Capture output
    ↓
Append tool result to messages → Call API again
    ↓
Receive final response → Update UI
```

## Threading Model

The application uses Python's `asyncio` for asynchronous operations:

- **Main Event Loop**: Runs the Textual UI
- **Async Tasks**: API calls, file I/O, shell commands
- **Yield Points**: `await asyncio.sleep(0)` between chunks for UI responsiveness

## State Management

| State Type | Location | Persistence |
|------------|----------|-------------|
| Messages | `ContextManager.messages` | Via SessionManager |
| Token Count | `DeepSeekClient.tokens_used` | Ephemeral |
| Session ID | `SessionManager.current_session_id` | N/A |
| Config | `Config` class | `.env` file |

## Error Handling Strategy

1. **Network Errors**: Retry with exponential backoff (max 3 attempts)
2. **Rate Limits**: Wait, then retry automatically
3. **Tool Execution**: Catch exceptions, return error message to AI
4. **Invalid Input**: Show helpful error, keep application running
