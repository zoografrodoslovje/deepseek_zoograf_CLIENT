#!/usr/bin/env python3
"""
DeepSeek CLI Tool - Main Entry Point

An agentic Terminal User Interface (TUI) client for DeepSeek API.
Run this script or use `ds-cli` command after installation.
"""

import sys
from pathlib import Path

# Ensure src is in path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def check_dependencies():
    """Check if all required dependencies are installed."""
    required = [
        ("textual", "Textual TUI framework"),
        ("openai", "OpenAI/DeepSeek SDK"),
        ("rich", "Rich terminal formatting"),
        ("tiktoken", "Token counting"),
        ("dotenv", "Environment variable loading"),
    ]

    missing = []

    for module, description in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(f"{description} ({module})")

    if missing:
        print("\n❌ Missing dependencies:")
        for pkg in missing:
            print(f"   • {pkg}")
        print("\n💡 Install them with:")
        print("   pip install -r requirements.txt\n")
        sys.exit(1)


def check_env():
    """Check if .env file exists and has API key."""
    env_file = Path(".env")

    if not env_file.exists():
        print("\n❌ .env file not found!")
        print("\n📝 Create one by copying the example:")
        print("   cp .env.example .env\n")
        print("Then add your DeepSeek API key to the .env file.\n")
        sys.exit(1)

    from dotenv import load_dotenv
    import os

    load_dotenv()

    if not os.getenv("DEEPSEEK_API_KEY"):
        print("\n❌ DEEPSEEK_API_KEY not set in .env file!")
        print("\n🔑 Get your API key from: https://platform.deepseek.com/\n")
        sys.exit(1)


async def run_app():
    """Run the DeepSeek CLI application."""
    from textual.app import App

    # Import after checks pass
    from ui.app import DeepSeekApp

    app = DeepSeekApp()

    try:
        await app.run_async()
    except KeyboardInterrupt:
        print("\n[Quit]")
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    print("\n🚀 DeepSeek CLI Tool v1.0.0")
    print("=" * 50 + "\n")

    # Check dependencies
    print("✓ Checking dependencies...")
    check_dependencies()

    # Check environment
    print("✓ Checking configuration...")
    check_env()

    # Validate config
    from core.config import Config

    is_valid, errors = Config.validate()
    if not is_valid:
        print("\n❌ Configuration errors:")
        for error in errors:
            print(f"   • {error}")
        print()
        sys.exit(1)

    # Run app
    print("✓ Starting TUI...\n")
    asyncio.run(run_app())


if __name__ == "__main__":
    import asyncio

    main()
