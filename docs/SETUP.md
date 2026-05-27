# Installation and Setup Guide

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- A valid DeepSeek API Key

## Step 1: Environment Setup

Create a dedicated directory on your Desktop:

```bash
# macOS/Linux
mkdir ~/Desktop/Deepseek\ CLI\ TOOL
cd ~/Desktop/Deepseek\ CLI\ TOOL

# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\Desktop\Deepseek CLI TOOL"
cd "$env:USERPROFILE\Desktop\Deepseek CLI Tool"
```

## Step 2: Initialize Project

If you haven't already, initialize git repository:

```bash
git init
```

## Step 3: Set Up Virtual Environment

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
venv\Scripts\activate.bat
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

To install with development tools:

```bash
pip install -r requirements.txt -e .[dev]
```

## Step 5: Configure API Key

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your DeepSeek API key:

```env
DEEPSEEK_API_KEY=sk-your-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEFAULT_MODEL=deepseek-chat
MAX_CONTEXT_TOKENS=64000
LOG_LEVEL=INFO
```

**Important:** Never commit `.env` files to version control!

## Step 6: Run the Application

### Development Mode

```bash
python main.py
```

### With Installed Package

After installing with `pip install -e .`, you can use the CLI command:

```bash
ds-cli
```

### With Docker (Future)

```bash
docker build -t deepseek-cli .
docker run -it --env-file .env deepseek-cli
```

## Verification

Test that everything is working:

```bash
# Check installation
python -c "import textual; import openai; print('✓ All dependencies installed')"

# Verify environment
python -c "from dotenv import load_dotenv; load_dotenv(); print(f'API key set: {bool(__import__(\"os\").environ.get(\"DEEPSEEK_API_KEY\"))}')"

# Run tests
pytest tests/ -v
```

## Troubleshooting

### Issue: ModuleNotFoundError

```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# OR
.\venv\Scripts\Activate.ps1  # PowerShell
```

### Issue: Permission Denied

```bash
# On Unix systems
chmod +x main.py

# Or run with python directly
python main.py
```

### Issue: API Authentication Failed

```bash
# Double-check .env file exists and contains correct key
cat .env | grep DEEPSEEK_API_KEY

# Make sure you're using https://platform.deepseek.com/ for key generation
```

### Issue: Terminal Display Issues

```bash
# Reset terminal
reset

# Check terminal size
stty size
```

## Next Steps

1. ✓ Review README.md for features overview
2. ✓ Review docs/ARCHITECTURE.md for technical details
3. ✓ Try running the application
4. ✓ Read docs/DEEPSEEK_API.md for API usage patterns
5. ✓ Contribute by forking on GitHub

## Uninstallation

To remove the tool completely:

```bash
# Deactivate virtual environment
deactivate

# Remove directory
rm -rf ~/Desktop/Deepseek\ CLI\ TOOL
# OR on Windows
Remove-Item -Recurse -Force "$env:USERPROFILE\Desktop\Deepseek CLI TOOL"
```
