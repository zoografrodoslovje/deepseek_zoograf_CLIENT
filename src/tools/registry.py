"""Tool registry — maps tool names to functions and generates JSON schemas."""
from typing import Any, Callable
from src.tools.filesystem import read_file, write_file, list_directory
from src.tools.shell import execute_command
from src.tools.search import search_codebase


def get_tool_definitions() -> list[dict]:
    """Return the list of tool definitions in OpenAI function calling format."""
    return [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the contents of a local file. Returns the full file content or an error.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative or absolute path to the file to read.",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Write content to a local file. Creates parent directories if needed. Overwrites existing files.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative or absolute path to the file to write.",
                        },
                        "content": {
                            "type": "string",
                            "description": "The full content to write to the file.",
                        },
                    },
                    "required": ["path", "content"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_directory",
                "description": "List files and directories at a given path. Returns names, types, and sizes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path to list (default: current directory).",
                        },
                        "recursive": {
                            "type": "boolean",
                            "description": "Whether to list recursively (default: false).",
                        },
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "execute_command",
                "description": "Execute a shell command. User must explicitly confirm before running. Returns stdout, stderr, and exit code.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to execute.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Brief explanation of what this command does for user confirmation.",
                        },
                    },
                    "required": ["command", "description"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_codebase",
                "description": "Search file contents using regex patterns (ripgrep-style). Returns matching files and lines.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Regex pattern to search for.",
                        },
                        "path": {
                            "type": "string",
                            "description": "Directory or file to search in (default: current directory).",
                        },
                        "file_glob": {
                            "type": "string",
                            "description": "Optional file glob filter (e.g., '*.py', '*.ts').",
                        },
                    },
                    "required": ["pattern"],
                },
            },
        },
    ]


def get_tool_handlers() -> dict[str, Callable]:
    """Return a dict mapping tool names to their Python functions."""
    return {
        "read_file": read_file,
        "write_file": write_file,
        "list_directory": list_directory,
        "execute_command": execute_command,
        "search_codebase": search_codebase,
    }
