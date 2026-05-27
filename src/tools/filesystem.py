"""Filesystem tool implementations — read, write, list directory."""
import os
from pathlib import Path


def read_file(path: str) -> str:
    """Read a file and return its content."""
    try:
        expanded = os.path.expanduser(path)
        p = Path(expanded).resolve()
        if not p.exists():
            return f"Error: File not found: {path}"
        if not p.is_file():
            return f"Error: Not a file: {path}"
        content = p.read_text(encoding="utf-8", errors="replace")
        size = len(content)
        lines = content.count("\\n") + 1
        return f"File: {p} ({size} bytes, {lines} lines)\\n\\n{content}"
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file, creating parent directories if needed."""
    try:
        expanded = os.path.expanduser(path)
        p = Path(expanded).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} bytes to {p}"
    except Exception as e:
        return f"Error writing file: {e}"


def list_directory(path: str = ".", recursive: bool = False) -> str:
    """List files in a directory."""
    try:
        expanded = os.path.expanduser(path)
        p = Path(expanded).resolve()
        if not p.exists():
            return f"Error: Path not found: {path}"
        if not p.is_dir():
            return f"Error: Not a directory: {path}"

        lines = []
        if recursive:
            for item in sorted(p.rglob("*")):
                rel = item.relative_to(p)
                if item.is_dir():
                    lines.append(f"📁 {rel}/")
                else:
                    size = item.stat().st_size
                    lines.append(f"📄 {rel} ({size} bytes)")
        else:
            for item in sorted(p.iterdir()):
                name = item.name
                if item.is_dir():
                    lines.append(f"📁 {name}/")
                else:
                    size = item.stat().st_size
                    lines.append(f"📄 {name} ({size} bytes)")

        total = len(lines)
        header = f"Directory listing: {p} ({total} items)"
        return header + "\\n" + "\\n".join(lines) if lines else header + "\\n(empty)"
    except Exception as e:
        return f"Error listing directory: {e}"
