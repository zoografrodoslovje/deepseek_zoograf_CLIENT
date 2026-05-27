# Quick Start Guide

## One-Command Setup (Linux/macOS)

```bash
mkdir -p ~/Desktop/Deepseek\ CLI\ TOOL && cd "$_" && git init && \
python3 -m venv venv && source venv/bin/activate && \
pip install textual openai rich tiktoken python-dotenv aiofiles && \
echo "DEEPSEEK_API_KEY=your-key-here" > .env && python main.py
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python main.py` | Run the application |
| `pytest tests/ -v` | Run all tests |
| `black src/ tests/` | Format code |
| `ruff check .` | Lint code |
| `mypy src/` | Type checking |

## Project Structure at a Glance

```
deepseek-cli-tool/
├── main.py                 # Entry point
├── pyproject.toml          # Package configuration
├── requirements.txt        # Dependencies
├── .env                    # Your API key
├── README.md               # Documentation
│
├── src/
│   ├── ui/                 # Textual TUI components
│   │   ├── app.py          # Main application
│   │   ├── chat_view.py    # Message display
│   │   ├── input_area.py   # User input
│   │   └── status_bar.py   # Token/model display
│   │
│   ├── core/               # Business logic
│   │   ├── client.py       # DeepSeek API client
│   │   ├── context.py      # Conversation context
│   │   ├── session.py      # Save/load sessions
│   │   └── config.py       # Settings loader
│   │
│   ├── tools/              # Agentic tools
│   │   ├── registry.py     # Tool definitions
│   │   ├── filesystem.py   # File operations
│   │   ├── shell.py        # Command execution
│   │   └── search.py       # Codebase search
│   │
│   └── utils/              # Helpers
│       ├── markdown.py     # Text rendering
│       └── logger.py       # Logging
│
└── tests/                  # Unit tests
```

## First Time Usage

1. **Set your API key** in `.env`:
   ```env
   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Start chatting**: Type your message and press Enter

4. **Use agent features**: Ask AI to read files, run commands, or search codebase

## Available Commands

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Ctrl+C` | Interrupt current operation |
| `D` | Clear conversation |
| `S` | Save current session |
| `O` | Load saved session |
| `?` | Show help |
| `Q` | Quit application |

## Default Models

- `deepseek-chat` - General purpose (default)
- `deepseek-reasoner` - Complex reasoning tasks

Change model in `.env`:
```env
DEFAULT_MODEL=deepseek-reasoner
```

## Tips

- Press `Tab` in input to see available files (future feature)
- Use `/read <file>` syntax to quickly read a file
- Ask questions about your codebase - AI can analyze multiple files
- Session history auto-saves when you quit

## Security Notes

- Never share your API key publicly
- Review commands before executing
- AI cannot access restricted system paths
- Local files only - no network uploads

## Need Help?

- Check `README.md` for full documentation
- See `docs/ARCHITECTURE.md` for technical details
- Open an issue on GitHub for bugs/suggestions

---

Happy coding! 🚀
