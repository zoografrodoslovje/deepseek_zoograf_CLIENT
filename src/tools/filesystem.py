"""File System Tools - Read, write, list files and directories"""

import os
from pathlib import Path
from typing import Optional
from core.config import Config


def read_file(path: str) -> str:
    """Read contents of a local file.

    Args:
        path: Relative or absolute path to the file

    Returns:
        File contents as string
    """
    try:
        # Resolve path relative to project root if not absolute
        if not os.path.isabs(path):
            full_path = Config.ROOT_DIR / path
        else:
            full_path = Path(path)

        if not full_path.exists():
            return f"Error: File not found at '{path}'"

        if not full_path.is_file():
            return f"Error: '{path}' is not a file"

        content = full_path.read_text(encoding="utf-8")
        lines = len(content.splitlines())
        return f"Successfully read {path} ({lines} lines):\n\n{content}"

    except PermissionError:
        return f"Error: Permission denied reading '{path}'"
    except UnicodeDecodeError:
        return f"Error: Cannot decode '{path}' as text (binary file?)"
    except Exception as e:
        return f"Error reading '{path}': {str(e)}"


def write_file(path: str, content: str) -> str:
    """Create or overwrite a file with given content.

    Args:
        path: Relative or absolute path to the file
        content: Content to write

    Returns:
        Success/error message
    """
    try:
        # Resolve path
        if not os.path.isabs(path):
            full_path = Config.ROOT_DIR / path
        else:
            full_path = Path(path)

        # Create parent directories if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        full_path.write_text(content, encoding="utf-8")
        lines = len(content.splitlines())

        return f"Successfully wrote '{path}' ({lines} lines)"

    except PermissionError:
        return f"Error: Permission denied writing to '{path}'"
    except Exception as e:
        return f"Error writing to '{path}': {str(e)}"


def list_dir(path: str | None = None) -> str:
    """List contents of a directory.

    Args:
        path: Directory path (default: current working directory)

    Returns:
        Directory listing as formatted string
    """
    try:
        if path is None:
            target_path = Path.cwd()
        elif not os.path.isabs(path):
            target_path = Config.ROOT_DIR / path
        else:
            target_path = Path(path)

        if not target_path.exists():
            return f"Error: Directory not found at '{path}'"

        if not target_path.is_dir():
            return f"Error: '{path}' is not a directory"

        items = sorted(target_path.iterdir())
        result = f"Contents of '{target_path}':\n" + "-" * 40 + "\n"

        for item in items:
            icon = "📁" if item.is_dir() else "📄"
            name = item.name
            if item.is_dir():
                name += "/"
            result += f"{icon} {name}\n"

        result += "-" * 40
        result += f"\nTotal: {len(items)} items"

        return result

    except PermissionError:
        return f"Error: Permission denied listing '{path}'"
    except Exception as e:
        return f"Error listing '{path}': {str(e)}"


__all__ = ["read_file", "write_file", "list_dir"]
