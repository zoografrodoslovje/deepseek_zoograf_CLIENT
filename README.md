<div align="center">

# 🚀 HERO UI POR — DeepSeek Zoograf Client

**An agentic terminal client for DeepSeek AI — built with Textual, live on Windows.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)](https://www.python.org/downloads/)
[![Textual](https://img.shields.io/badge/TUI-Textual-2563EB?logo=textual)](https://textual.textualize.io/)
[![DeepSeek](https://img.shields.io/badge/API-DeepSeek-4A6CF7)](https://platform.deepseek.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

![Hero UI Demo](./docs/demo.gif)

</div>

---

## ✨ Features

- 💬 **Chat with DeepSeek** — Stream responses with live markdown rendering
- 🛠️ **Agentic Tools** — Read/write files, run shell commands, search codebases — all through the AI
- 📋 **Session Management** — Save and reload conversations (`Ctrl+S`, `Ctrl+N`)
- 🔄 **Model Switching** — Toggle between `deepseek-chat` and `deepseek-reasoner` (`Ctrl+M`)
- 🎨 **HERO UI POR Light Theme** — Clean, bright terminal UI with hero-style accents
- 📊 **Token Tracking** — Real-time token usage in the status bar
- 🪟 **Windows-native** — One-click installer, PowerShell/BAT setup, virtual env management

---

## 📦 Quick Install (Windows)

### Prerequisites
- **Python 3.10+** — [Download here](https://www.python.org/downloads/) (check *"Add Python to PATH"*)
- **Windows Terminal** (recommended) — Get it from the [Microsoft Store](https://apps.microsoft.com/detail/9n0dx20hk701)
- A **DeepSeek API key** — Get one free at [platform.deepseek.com](https://platform.deepseek.com/api_keys)

### Option 1: One-Click Setup (Recommended)

```batch
:: 1. Download or clone the repository
git clone https://github.com/zoografrodoslovje/deepseek_zoograf_CLIENT.git
cd deepseek_zoograf_CLIENT

:: 2. Run the installer — it does everything
install.bat
```

The installer will:
1. ✅ Check your Python installation
2. ✅ Create an isolated virtual environment (`venv\`)
3. ✅ Install all dependencies (textual, openai, rich, etc.)
4. ✅ Open `.env` so you can paste your API key
5. ✅ Verify everything works

Then launch with:
```batch
run.bat
```

### Option 2: PowerShell Setup
```powershell
.\install.ps1
# If you get a security error, run:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

### Option 3: Manual Setup
```batch
:: Create virtual environment
python -m venv venv

:: Activate it
venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Configure API key
copy .env.example .env
:: → Edit .env and set DEEPSEEK_API_KEY

:: Run
python main.py
```

---

## 🎮 Usage

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Shift+Enter` | New line in input |
| `↑ / ↓` | Navigate input history |
| `Ctrl+C` | Quit the client |
| `Ctrl+L` | Clear chat history |
| `Ctrl+S` | Save current session |
| `Ctrl+N` | Start new session |
| `Ctrl+M` | Toggle between models |
| `F5` | Toggle tool calling on/off |

**Getting started:**
1. Launch the client with `run.bat`
2. Type your question or task in the input area
3. Press `Enter` to send
4. Watch the AI respond with streaming markdown
5. The AI can use tools — file operations, shell commands, codebase search

**Example prompts:**
- *"Read the main.py file and explain what it does"*
- *"Search for all TODO comments in this project"*
- *"Create a new Python script named hello.py that prints 'Hello from DeepSeek!'"*
- *"List all files in the src directory"*

---

## 🧰 Built-in Tools

The AI assistant can autonomously use these tools when helpful:

| Tool | Description |
|------|-------------|
| `read_file` | Read any file in the project |
| `write_file` | Create or overwrite files (creates directories) |
| `list_directory` | Browse files and folders |
| `execute_command` | Run shell commands (execution is shown transparently) |
| `search_codebase` | Search file contents with regex (ripgrep/grep) |

All shell commands are shown to you before execution — nothing runs silently.

---

## 📁 Project Structure

```
deepseek_zoograf_CLIENT/
├── main.py                    # Entry point — double-click or "python main.py"
├── install.bat                # One-click Windows installer
├── install.ps1                # PowerShell installer
├── run.bat                    # Quick launch after setup
├── requirements.txt           # Python dependencies
├── .env.example               # API key template
├── .gitignore
├── README.md                  # ← This file
├── pyproject.toml             # Project metadata
│
├── src/                       # Source code
│   ├── ui/                    # User interface layer
│   │   ├── app.py             # Main Textual App (DeepSeekTUI)
│   │   ├── chat_view.py       # Streaming markdown chat display
│   │   ├── input_area.py      # Multi-line input with history
│   │   ├── status_bar.py      # Model / token / connection status
│   │   └── theme.py           # HERO UI POR Light theme + CSS
│   ├── core/                  # Core logic
│   │   ├── client.py          # AsyncOpenAI DeepSeek client
│   │   ├── config.py          # .env configuration loader
│   │   ├── context.py         # Token tracking & context window
│   │   └── session.py         # Session save/load persistence
│   ├── tools/                 # Agentic tool implementations
│   │   ├── registry.py        # Tool definitions + handler mapping
│   │   ├── filesystem.py      # read_file, write_file, list_directory
│   │   ├── shell.py           # execute_command (with confirmation)
│   │   └── search.py          # search_codebase (ripgrep/grep)
│   └── utils/                 # Utilities
│       ├── markdown.py        # Rich markdown rendering
│       └── logger.py          # Logging setup
│
└── docs/                      # Documentation
    ├── USAGE.md               # Full usage guide
    ├── TROUBLESHOOTING.md     # Common issues & solutions
    └── ARCHITECTURE.md        # Technical architecture overview
```

---

## ⚙️ Configuration

All settings live in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DEEPSEEK_API_KEY` | — | **Required.** Your DeepSeek API key |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | API endpoint URL |
| `DEFAULT_MODEL` | `deepseek-chat` | Default model (`deepseek-chat` or `deepseek-reasoner`) |
| `MAX_TOKENS` | `64000` | Context window size |
| `MAX_OUTPUT_TOKENS` | `4096` | Max tokens per response |
| `TEMPERATURE` | `0.7` | Response creativity (0.0–2.0) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## 🚢 Sessions

Sessions are automatically saved to `~/.ds-cli/sessions/` as JSON files.

- **`Ctrl+S`** — Save the current conversation
- **`Ctrl+N`** — Start a fresh session
- Sessions include full message history and metadata (model, timestamp)

---

## 🧪 Development

```bash
# Install in dev mode
pip install -e .

# Run with Textual dev tools for debugging
textual run --dev main.py

# Run with live CSS reloading
textual run --dev main.py --css src/ui/theme.py
```

---

## ❓ Troubleshooting

See [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) for solutions to common issues:

- *"No module named 'anyio.to_thread'"*
- *"Python not found"* or *"pip is not recognized"*
- *Terminal display issues / unicode boxes*
- *API key / connection errors*

---

## 📄 License

MIT — See [LICENSE](LICENSE) for details.

---

<div align="center">
Made with ❤️ by <a href="https://github.com/zoografrodoslovje">Sitcode</a>
</div>
