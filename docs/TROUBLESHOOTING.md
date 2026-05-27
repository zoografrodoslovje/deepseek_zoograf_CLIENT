# 🔧 DeepSeek Zoograf Client — Troubleshooting Guide

Common issues and their solutions.

---

## Installation Issues

### "Python not found" or "'python' is not recognized"

**Cause:** Python is not installed or not on your PATH.

**Solution:**
1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
2. **During installation, check "Add Python to PATH"**
3. Restart your terminal
4. Verify: `python --version`

> 💡 After installing Python, try using `py` instead of `python`. On Windows, the Python launcher (`py`) often works even when `python` doesn't.

### "pip is not recognized"

**Cause:** pip not installed or not on PATH.

**Solution:**
```bash
python -m ensurepip --upgrade
```
Or reinstall Python and check "Install pip" during setup.

### "externally-managed-environment" error

**Cause:** Your Python installation blocks system-wide package installs (common on Linux/WSL, rare on Windows).

**Solution (Windows):** Use the included virtual environment:
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Solution (WSL/Linux):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "No module named 'anyio.to_thread'"

**Root Cause:** A corrupted `anyio` package — missing `__init__.py`.

**Fix:**
```bash
pip install --force-reinstall anyio
```

> This can happen if pip was interrupted during installation or if there are two Python installations with conflicting packages.

### Permission denied creating venv

**Solution:**
- Run PowerShell/Terminal **as Administrator**
- Or install to a directory you own (not `C:\Program Files`)
- Or use the system Python without a venv: `pip install --user -r requirements.txt`

---

## Runtime Issues

### Client opens and immediately closes

**Cause:** The window closes before you can read the error.

**Fix:** Run from a terminal manually:
```bash
cd C:\path\to\deepseek_zoograf_CLIENT
venv\Scripts\activate
python main.py
```
This keeps the terminal open so you can see the error message.

### "InvalidThemeError: Theme has not been registered"

**Cause:** Theme registration failed during startup.

**Fix:** This is usually a one-time issue. Re-run the client. If it persists:
```bash
pip install --upgrade textual
```

### Unicode boxes or weird characters in the UI

**Cause:** The terminal doesn't support Unicode box-drawing characters.

**Fix:**
- **Windows Terminal** — Get from [Microsoft Store](https://apps.microsoft.com/detail/9n0dx20hk701)
- **PowerShell 7+** — Update to the latest version
- Install a font like **Cascadia Code** or **JetBrains Mono Nerd Font**

### Text area not responding to keyboard

**Cause:** The input area lost focus.

**Fix:**
- Click on the input area
- Press `Tab` to cycle focus
- Restart the client

### Chat history lost after restart

**Cause:** Sessions are saved manually, not automatically.

**Fix:** Press `Ctrl+S` before closing to save the current session. Sessions are stored in `%USERPROFILE%\.ds-cli\sessions\`.

---

## API & Connection Issues

### "API Error" / Connection refused

**Cause 1:** No internet connection.
**Fix:** Check your internet.

**Cause 2:** Invalid API key.
**Fix:** Open `.env` and verify your `DEEPSEEK_API_KEY`. It should start with `sk-`.

**Cause 3:** Incorrect API URL.
**Fix:** Make sure `DEEPSEEK_BASE_URL` is `https://api.deepseek.com/v1`

### "401 Unauthorized"

**Cause:** API key is wrong, expired, or missing.

**Fix:**
1. Check your key at [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
2. Make sure `.env` has the correct key (no extra spaces or quotes)
3. Regenerate the key if it might be compromised

### "429 Too Many Requests"

**Cause:** You've hit DeepSeek's rate limit.

**Fix:**
- Wait a few minutes and try again
- Check your plan's rate limits on the DeepSeek platform
- DeepSeek's free tier typically allows ~60 requests per minute

### "503 Service Unavailable"

**Cause:** DeepSeek's API is temporarily down.

**Fix:**
- Check [status.deepseek.com](https://status.deepseek.com) for outages
- Wait and retry

### Slow response times

**Possible causes:**
- DeepSeek server load
- Your internet connection
- Large context window (token processing overhead)

**Tips:**
- Start a new session (`Ctrl+N`) if the conversation is very long
- Use `deepseek-chat` instead of `deepseek-reasoner` for faster responses
- Check `LOG_LEVEL=DEBUG` in `.env` to see detailed timing info

---

## Display & Rendering Issues

### Code blocks not syntax-highlighted

**Cause:** The language wasn't specified in the markdown code block.

**Fix:** This depends on the AI — ask it to specify the language in code blocks.

### Markdown not rendering correctly

**Cause:** Some complex markdown might not render perfectly in terminal.

**Fix:** This is a Textual/Rich limitation. Most standard markdown (bold, italic, code, lists, tables) works fine.

### Emoji not displaying

**Cause:** Terminal font doesn't support emoji.

**Fix:**
- Use Windows Terminal with **Segoe UI Emoji** font
- Or install a [Nerd Font](https://www.nerdfonts.com/)

---

## Tool Issues

### "Tool 'X' not found"

**Cause:** The AI tried to use a tool that doesn't exist.

**Fix:** The built-in tools are: `read_file`, `write_file`, `list_directory`, `execute_command`, `search_codebase`. If the AI invokes something else, it should gracefully handle the error and continue.

### Write file permission denied

**Cause:** The tool doesn't have permission to write to the target directory.

**Fix:** Run the terminal/command prompt **as Administrator** or choose a writable directory.

### Command execution appears to hang

**Cause:** The command is waiting for input or is a long-running process.

**Fix:**
- Avoid running interactive commands (like `vim`, `nano`, or long-running servers)
- The tool has a 60-second timeout for shell commands
- Use `Ctrl+C` to quit the client if needed

---

## Environment Issues

### I have two Python versions (Python + py)

On Windows, `python` and `py` can point to different Python installations. The installers use `python` by default.

**Check which is which:**
```powershell
python --version
py --version
python -c "import sys; print(sys.executable)"
py -c "import sys; print(sys.executable)"
```

**Fix:** Use the one that has all dependencies. Or use the virtual environment (it uses the Python that created it).

### Virtual environment activation fails

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
# If blocked, run:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```batch
venv\Scripts\activate.bat
```

---

## Getting Help

If you've tried everything and still have issues:

1. **Check the logs** — Set `LOG_LEVEL=DEBUG` in `.env` and re-run
2. **Open an issue** — [github.com/zoografrodoslovje/deepseek_zoograf_CLIENT/issues](https://github.com/zoografrodoslovje/deepseek_zoograf_CLIENT/issues)
3. **Include:**
   - Your Windows version
   - Python version (`python --version`)
   - The full error message
   - What you've tried so far
