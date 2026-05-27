# Technical Requirements Document

## 1. Terminal Interface (TUI) Requirements

### 1.1 Visual Requirements
- [x] Render markdown, code blocks, and tables correctly in terminal
- [x] Support syntax highlighting for 20+ programming languages
- [x] Handle terminal resizing gracefully without layout breakage
- [x] Split-pane view: Chat history (top/left), input + status bar (bottom/right)
- [x] Real-time streaming updates at 60fps minimum

### 1.2 Input Requirements
- [x] Multi-line text input with Enter/Shift+Enter handling
- [x] History navigation (Up/Down arrows)
- [x] Auto-focus on input after message submission
- [x] Clear/disabled state during AI response streaming

## 2. API Integration Requirements

### 2.1 DeepSeek API Connection
- [x] Connect to `https://api.deepseek.com/v1`
- [x] Support streaming responses (`stream=True`)
- [x] Handle rate limits with automatic retry (max 3 attempts)
- [x] Automatic error recovery for network issues

### 2.2 Model Support
- [x] `deepseek-chat` - General purpose model
- [x] `deepseek-reasoner` - Reasoning-focused model (R1)
- [x] Configurable default model via `.env`

## 3. Agentic Tool Requirements

### 3.1 File Operations
| Tool | Description | Requires Confirmation |
|------|-------------|---------------------|
| `read_file` | Read file contents | No |
| `write_file` | Create/modify files | Yes |
| `list_dir` | List directory | No |

### 3.2 System Commands
| Tool | Description | Requires Confirmation |
|------|-------------|---------------------|
| `execute_command` | Run shell commands | Yes |
| `search_codebase` | Search file contents | No |

### 3.3 Security Requirements
- [x] Dangerous command detection and blocking
- [x] Explicit user confirmation for write/delete operations
- [x] System directory access prevention
- [x] Timeout enforcement for shell commands (default: 30s)

## 4. Context Management Requirements

### 4.1 Token Management
- [x] Track token usage per session
- [x] Maximum context window: 64k tokens
- [x] Warning display when approaching limit
- [x] Automatic summarization of old messages

### 4.2 Session Persistence
- [x] Save conversations to JSON files
- [x] Load saved sessions
- [x] Branch existing sessions
- [x] Session metadata (name, created_at, updated_at)

## 5. Non-Functional Requirements

### 5.1 Performance
- [x] TUI maintains 60fps during streaming
- [x] Fast response time (<200ms for UI updates)
- [x] Memory efficient (lazy loading, garbage collection)

### 5.2 Security
- [x] API keys from environment variables only
- [x] No hardcoded credentials
- [x] HTTPS-only API connections
- [x] `.env` excluded from version control

### 5.3 Dependencies
- Core: `textual`, `openai`, `rich`, `tiktoken`
- Optional: `python-dotenv`, `aiofiles`
- Dev: `pytest`, `black`, `ruff`, `mypy`
