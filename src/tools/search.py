"""Codebase search using ripgrep or fallback grep."""
import subprocess
import shutil
from pathlib import Path


def search_codebase(pattern: str, path: str = ".", file_glob: str = "") -> str:
    """Search file contents using ripgrep or grep."""
    try:
        expanded = str(Path(path).expanduser().resolve())
    except Exception:
        expanded = path

    has_rg = shutil.which("rg") is not None

    try:
        if has_rg:
            cmd = ["rg", "-n", "--color", "never", pattern, expanded]
            if file_glob:
                cmd.extend(["-g", file_glob])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        else:
            cmd = ["grep", "-rn", "--color=never", pattern, expanded]
            if file_glob:
                cmd.extend([f"--include={file_glob}"])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        output = result.stdout
        if not output:
            return f"No matches found for: {pattern}"

        # Limit output
        lines = output.split("\\n")
        if len(lines) > 200:
            output = "\\n".join(lines[:200]) + f"\\n... and {len(lines) - 200} more matches"

        return f"Search results for '{pattern}' in {expanded}:\\n\\n{output}"

    except subprocess.TimeoutExpired:
        return f"Search timed out for pattern: {pattern}"
    except FileNotFoundError:
        return f"Error: grep not available on this system"
    except Exception as e:
        return f"Error searching codebase: {e}"
