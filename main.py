#!/usr/bin/env python3
"""
HERO UI POR — DeepSeek Agentic Terminal Client
================================================
A Textual TUI for chatting with DeepSeek's API, with
file editing, shell commands, and codebase search.

Usage:
    python main.py              # Run the TUI
    python main.py --version    # Show version
"""

import sys
import os

# Ensure src is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.ui.app import run
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("   Make sure dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


def main():
    if "--version" in sys.argv or "-v" in sys.argv:
        print("HERO UI POR v0.1.0 — DeepSeek Agentic Terminal Client")
        return

    try:
        run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
