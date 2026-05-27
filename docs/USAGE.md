# 📖 DeepSeek Zoograf Client — Usage Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Keyboard Shortcuts](#keyboard-shortcuts)
4. [Working with the AI](#working-with-the-ai)
5. [Agentic Tools](#agentic-tools)
6. [Session Management](#session-management)
7. [Configuration](#configuration)
8. [Tips & Tricks](#tips--tricks)

---

## Getting Started

After installation, launch the client:

```batch
:: From the project directory
run.bat

:: Or manually
venv\Scripts\activate
python main.py
```

The client will connect to DeepSeek's API using the key in your `.env` file. If everything is configured correctly, you'll see the welcome screen with the HERO UI POR theme.

> **First time?** The welcome message will guide you. Just type your question and press `Enter`.

---

## Interface Overview

The interface has four zones:

```
┌──────────────────────────────────────────────┐
│  🚀 HERO UI POR — DeepSeek Agentic Client    │  ← Header
├──────────────────────────────────────────────┤
│                                              │
│  ┌─ You ──────────────────────────────────┐  │
│  │ What's the weather in Tokyo today?     │  │
│  └────────────────────────────────────────┘  │
│                                              │  ← Chat area
│  ┌────────────────────────────────────────┐  │  (streaming
│  │ Let me check that for you!             │  │   markdown
│  │                                        │  │   messages)
│  │ The current weather in Tokyo is...     │  │
│  └────────────────────────────────────────┘  │
│                                              │
├──────────────────────────────────────────────┤
│  ┌ Message ───────────────────────────────┐  │
│  │                                        │  │  ← Input area
│  │ Type here...                           │  │  (multi-line,
│  │                                        │  │   history)
│  └────────────────────────────────────────┘  │
├──────────────────────────────────────────────┤
│  HERO UI POR │ deepseek-chat    tokens/64000│  ← Status bar
└──────────────────────────────────────────────┘
```

- **Header** — App title and current time
- **Chat area** — Conversation history with streaming responses
- **Input area** — Multi-line text input with history navigation
- **Status bar** — Model name, token usage, API connection status

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Send the current message |
| `Shift+Enter` | Insert a new line in the input |
| `↑` | Previous message in input history |
| `↓` | Next message in input history |
| `Ctrl+C` | Quit the application |
| `Ctrl+L` | Clear the entire chat history |
| `Ctrl+S` | Save the current session to disk |
| `Ctrl+N` | Start a new empty session |
| `Ctrl+M` | Toggle between `deepseek-chat` and `deepseek-reasoner` |
| `F5` | Enable/disable tool calling |

---

## Working with the AI

### Basic Chat

Simply type your message and press `Enter`. The AI response streams in real-time with full markdown rendering — code blocks, tables, lists, and formatting all display correctly.

### Asking for Code Help

The AI excels at coding tasks. Try:

```
Write a Python function that reads a CSV file and returns
the average of each column
```

The response will include syntax-highlighted code blocks.

### File Operations

The AI can read and write files in your project directory:

```
Read the file src/ui/app.py and summarize what it does
```

```
Create a new file called utils/helpers.py with a function that
validates email addresses
```

### Shell Commands

The AI can execute shell commands (shown transparently):

```
Find all Python files that contain "TODO" comments
```

```
Show me the directory structure of this project
```

> **Safety:** All shell commands are displayed in the chat before execution. You can see exactly what will run.

---

## Agentic Tools

The AI automatically decides when to use tools. You don't need to invoke them manually — just describe what you want.

### read_file

Reads the full content of any file. The AI will use this when you ask about code or file contents.

### write_file

Creates or overwrites files. The AI will use this when you ask it to write code, create config files, or save output.

### list_directory

Lists files and folders at a given path. The AI uses this to understand your project structure.

### execute_command

Runs shell commands. The command and its purpose are shown in the chat. Never runs silently.

### search_codebase

Searches file contents using regex (ripgrep if available, grep fallback). Use this to find specific patterns across your codebase.

**Example interaction:**
```
You: Find all places where we use the OpenAI client

AI: (uses search_codebase)
  🔍 Searching for "OpenAI"...
  Found in:
    - src/core/client.py: line 12
    - src/core/config.py: line 22

  Here's what I found...
```

---

## Session Management

### Saving a Session

Press `Ctrl+S` to save the current conversation. Sessions are stored as JSON files in:
- **Windows:** `C:\Users\<YourName>\.ds-cli\sessions\`

Each session is timestamped and includes the full message history.

### Loading a Session

Session loading is automatic — the tool saves on demand. To reload a previous session, you can manually load the JSON file from the sessions directory.

### Starting Fresh

Press `Ctrl+N` to clear the chat and start a new session. Token counters reset.

---

## Configuration

### Settings Reference

Edit `.env` in the project root:

```ini
# ── API Configuration ──
DEEPSEEK_API_KEY=sk-your-key-here        # REQUIRED
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# ── Model Settings ──
DEFAULT_MODEL=deepseek-chat               # or deepseek-reasoner
MAX_TOKENS=64000                          # Context window
MAX_OUTPUT_TOKENS=4096                    # Max response length
TEMPERATURE=0.7                           # 0.0 (precise) - 2.0 (creative)

# ── Logging ──
LOG_LEVEL=INFO                            # DEBUG, INFO, WARNING, ERROR
```

### Model Comparison

| Model | Best For | Notes |
|-------|----------|-------|
| `deepseek-chat` | General chat, coding, Q&A | Default, faster responses |
| `deepseek-reasoner` | Complex reasoning, math, logic | Shows reasoning chain |

Switch between them at any time with `Ctrl+M`.

---

## Tips & Tricks

### 💡 Write Clean Prompts

Be specific about what you want:
- ✅ *"Write a Python script to download all images from a webpage"*
- ❌ *"Help me with code"*

### 💡 Use Tools Naturally

The AI will use tools automatically when relevant. You don't need to say "use the read_file tool" — just ask *"What's in main.py?"*

### 💡 Long Conversations

The context manager automatically tracks token usage. If you approach the limit, older messages are summarized or dropped. Press `Ctrl+N` for a fresh start on long sessions.

### 💡 Dark vs Light Terminal

The HERO UI POR Light theme works best on light-background terminals. If your terminal is dark, use the `Ctrl+M` key or consider contributing a dark theme variant.

### 💡 Terminal Choice

- **Windows Terminal** — Best experience with full Unicode and color support
- **PowerShell 7+** — Good, but may need font configuration for Unicode icons
- **Command Prompt** — Works, but emoji rendering may be limited

---

## Keyboard Reference Card

```
┌────────────────────────────────────────────┐
│           HERO UI POR — Quick Ref          │
├────────────────────────────────────────────┤
│  Enter        Send message                 │
│  Shift+Enter  New line                     │
│  ↑ ↓          History                      │
│  Ctrl+C       Quit                         │
│  Ctrl+L       Clear chat                   │
│  Ctrl+S       Save session                 │
│  Ctrl+N       New session                  │
│  Ctrl+M       Switch model                 │
│  F5           Toggle tools                 │
└────────────────────────────────────────────┘
```
