"""Codebase Search Tools - Search file contents and patterns"""

import asyncio
from pathlib import Path
from typing import Optional
from core.config import Config


def search_codebase(
    pattern: str,
    path: str | None = None,
    extensions: list[str] | None = None,
    max_results: int = 20,
) -> str:
    """Search for text patterns in codebase files.

    Args:
        pattern: Text or regex pattern to search for
        path: Directory to search (default: project root)
        extensions: File extensions to filter (e.g., ['.py', '.js'])
        max_results: Maximum results to return

    Returns:
        Search results as formatted string
    """
    try:
        # Resolve search path
        if path is None:
            search_path = Config.ROOT_DIR
        elif not Path(path).is_absolute():
            search_path = Config.ROOT_DIR / path
        else:
            search_path = Path(path)

        if not search_path.exists():
            return f"Error: Search path not found: '{path}'"

        if not search_path.is_dir():
            return f"Error: Search path must be a directory: '{path}'"

        results = []
        files_searched = 0

        # Walk directory tree
        for file_path in search_path.rglob("*"):
            if not file_path.is_file():
                continue

            # Filter by extension if specified
            if extensions:
                if file_path.suffix.lower() not in [ext.lower() for ext in extensions]:
                    continue

            files_searched += 1

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                # Simple substring search (could be enhanced with re for regex)
                if pattern.lower() in content.lower():
                    lines = content.splitlines()
                    matching_lines = [
                        line.strip()
                        for line in lines
                        if pattern.lower() in line.lower()
                    ][:3]  # Show first 3 matches per file

                    results.append(
                        {
                            "file": str(file_path.relative_to(search_path)),
                            "matches": matching_lines,
                            "total_matches": len([l for l in lines if pattern.lower() in l.lower()]),
                        }
                    )

                    if len(results) >= max_results:
                        break

            except (PermissionError, UnicodeDecodeError):
                continue

        # Format results
        result = f"Search results for '{pattern}':\n\n"
        result += "-" * 40 + "\n"

        if not results:
            result += f"No matches found in {files_searched} files searched.\n"
        else:
            for i, r in enumerate(results[:max_results], 1):
                result += f"\n[{i}] {r['file']}\n"
                result += "-" * 30 + "\n"
                for match in r["matches"]:
                    result += f"  → {match}\n"
                result += f"  ({r['total_matches']} total matches)\n"

        result += "\n" + "-" * 40
        result += f"\nSearched {files_searched} files, found {len(results)} matches."

        return result

    except Exception as e:
        return f"Error during search: {str(e)}"


async def find_files(pattern: str, path: str | None = None) -> str:
    """Find files matching a glob pattern.

    Args:
        pattern: Glob pattern (e.g., '*.py', '**/*.json')
        path: Directory to search (default: project root)

    Returns:
        Matching files as formatted string
    """
    try:
        search_path = Config.ROOT_DIR if path is None else Path(path)

        if not search_path.exists():
            return f"Error: Path not found: '{path}'"

        files = sorted(search_path.glob(pattern))
        relative_paths = [f.relative_to(search_path) for f in files]

        result = f"Files matching '{pattern}':\n\n" + "-" * 40 + "\n"

        for file_path in relative_paths[:50]:  # Limit to 50 results
            icon = "📄" if ".md" not in str(file_path).lower() else "📝"
            result += f"{icon} {file_path}\n"

        if len(files) > 50:
            result += f"\n... and {len(files) - 50} more files"

        result += "\n" + "-" * 40
        result += f"\nTotal: {len(files)} files"

        return result

    except Exception as e:
        return f"Error finding files: {str(e)}"


__all__ = ["search_codebase", "find_files"]
