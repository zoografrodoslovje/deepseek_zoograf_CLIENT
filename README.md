<div align="center">

# 🚀 HERO UI POR — DeepSeek Zoograf Client

**An agentic terminal client for DeepSeek AI — built with Textual, live on Windows.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)](https://www.python.org/downloads/)
[![Textual](https://img.shields.io/badge/TUI-Textual-2563EB?logo=textual)](https://textual.textualize.io/)
[![DeepSeek](https://img.shields.io/badge/API-DeepSeek-4A6CF7)](https://platform.deepseek.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

---

## ✨ Features

- 💬 **Chat with DeepSeek** — Stream responses with live markdown rendering
- 🛠️ **Agentic Tools** — Read/write files, run shell commands, search codebases
- 📋 **Session Management** — Save and reload conversations
- 🔄 **Model Switching** — Toggle between `deepseek-chat` and `deepseek-reasoner`
- 🎨 **HERO UI POR Light Theme** — Clean, bright terminal UI
- 📊 **Token Tracking** — Real-time token usage in the status bar
- 🪟 **Windows-native** — One-click installers, virtual environment management

---

## 🚀 One-Shot Install (Windows)

**Requirements:** Windows 10+, Python 3.10+ ([download](https://www.python.org/downloads/))

### PowerShell (Recommended)
```powershell
iex (iwr -Uri https://raw.githubusercontent.com/zoografrodoslovje/deepseek_zoograf_CLIENT/main/install-online.ps1)
```

This single command:
1. ✅ Checks your Python installation
2. ✅ Downloads the latest client (git or ZIP)
3. ✅ Creates an isolated virtual environment
4. ✅ Installs all dependencies
5. ✅ Opens `.env` so you can paste your API key

When prompted, **paste your DeepSeek API key** into `.env` (get one free at [platform.deepseek.com](https://platform.deepseek.com/api_keys)).

### CMD (Command Prompt)
```batch
@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/zoografrodoslovje/deepseek_zoograf_CLIENT/main/install-online.ps1'))"
```

### Alternative: Clone + Install
```batch
git clone https://github.com/zoografrodoslovje/deepseek_zoograf_CLIENT.git
cd deepseek_zoograf_CLIENT
install.bat
```

### Launch After Install
```batch
cd deepseek_zoograf_CLIENT
.\run.bat
```
*Note: In PowerShell, always use `.\run.bat` (not just `run.bat`).*

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
1. Launch with `.\run.bat`
2. Type your question or task
3. Press `Enter` to send
4. The AI responds with streaming markdown

**Example prompts:**
- *"Read main.py and explain it"*
- *"Find all TODO comments in this project"*
- *"Create a file called hello.py"*
- *"List all files in the src directory"*

---

## 🧰 Agentic Tools

The AI assistant uses these tools automatically when helpful:

| Tool | Description |
|------|-------------|
| `read_file` | Read any file in the project |
| `write_file` | Create or overwrite files |
| `list_directory` | Browse files and folders |
| `execute_command` | Run shell commands (shown before execution) |
| `search_codebase` | Search file contents with regex |

---

## 📁 Project Structure

```
deepseek_zoograf_CLIENT/
├── main.py                    # Entry point
├── install.bat                # Windows installer (CMD)
├── install.ps1                # Windows installer (PowerShell)
├── install-online.ps1         # One-shot online installer
├── run.bat                    # Quick launcher
├── requirements.txt           # Dependencies
├── .env.example               # API key template
├── .gitignore
├── README.md                  # ← This file
├── pyproject.toml             # Project metadata
├── LICENSE                    # MIT License
│
├── src/                       # Source code
│   ├── ui/                    # User interface (Textual)
│   │   ├── app.py             # Main App (DeepSeekTUI)
│   │   ├── chat_view.py       # Streaming chat display
│   │   ├── input_area.py      # Multi-line input with history
│   │   ├── status_bar.py      # Model / token / connection status
│   │   └── theme.py           # HERO UI POR Light theme + CSS
│   ├── core/                  # Core logic
│   │   ├── client.py          # AsyncOpenAI DeepSeek client
│   │   ├── config.py          # .env configuration loader
│   │   ├── context.py         # Token tracking & context window
│   │   └── session.py         # Session save/load
│   ├── tools/                 # Agentic tools
│   │   ├── registry.py        # Tool definitions + handler mapping
│   │   ├── filesystem.py      # read_file, write_file, list_directory
│   │   ├── shell.py           # execute_command (with confirmation)
│   │   └── search.py          # search_codebase
│   └── utils/                 # Utilities
│       ├── markdown.py        # Rich markdown rendering
│       └── logger.py          # Logging setup
│
└── docs/                      # Documentation
    ├── USAGE.md               # Full usage guide
    ├── TROUBLESHOOTING.md     # Common issues & solutions
    └── ARCHITECTURE.md        # Technical architecture
```

---

## ⚙️ Configuration

Edit `.env` in the project root:

| Variable | Default | Description |
|----------|---------|-------------|
| `DEEPSEEK_API_KEY` | — | **Required.** Your DeepSeek API key |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | API endpoint |
| `DEFAULT_MODEL` | `deepseek-chat` | Default model |
| `MAX_TOKENS` | `64000` | Context window size |
| `MAX_OUTPUT_TOKENS` | `4096` | Max response tokens |
| `TEMPERATURE` | `0.7` | Response creativity (0.0–2.0) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [`docs/USAGE.md`](docs/USAGE.md) | Complete usage guide with interface diagram and keyboard reference |
| [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | Solutions for all common errors (Python PATH, API keys, Unicode display, anyio corruption, etc.) |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Technical overview for contributors |

---

## ❓ Common Issues

| Problem | Fix |
|---------|-----|
| `'python' not recognized` | Reinstall Python, check **Add Python to PATH** |
| `No module named 'anyio.to_thread'` | `pip install --force-reinstall anyio` |
| PowerShell says `&&` is invalid | Use PowerShell 7+ or run `install.bat` instead |
| `run.bat` not found | Use `.\run.bat` in PowerShell |
| Unicode boxes show garbage | Use **Windows Terminal** with Cascadia Code font |
| `401 Unauthorized` | Check your API key in `.env` |
| `429 Too Many Requests` | Wait a minute and retry |

See [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) for detailed solutions.

---

## 📄 License

MIT — See [LICENSE](LICENSE) for details.

---

<div align="center">
Made with ❤️ by <a href="https://github.com/zoografrodoslovje">Sitcode</a>
</div>
