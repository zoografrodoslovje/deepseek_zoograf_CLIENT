"""Tool Registry - Maps tool names to functions and generates JSON schemas"""

import inspect
from typing import Any, Callable
from .filesystem import read_file, write_file, list_dir
from .shell import execute_command
from .search import search_codebase


TOOL_REGISTRY: dict[str, dict[str, Any]] = {}


def register_tool(
    func: Callable, schema_override: dict | None = None
) -> dict[str, Any]:
    """Register a function as an available tool.

    Args:
        func: The function to register
        schema_override: Optional custom schema instead of auto-generated

    Returns:
        Tool specification dictionary for API
    """
    name = func.__name__
    doc = func.__doc__ or "No description available"

    if schema_override:
        schema = schema_override
    else:
        # Auto-generate schema from function signature
        sig = inspect.signature(func)
        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue

            # Infer type from default values or annotations
            param_type = "string"  # Default type
            description = f"Parameter {param_name}"

            if param.default is not inspect.Parameter.empty:
                description += f" (default: {param.default})"

            properties[param_name] = {"type": param_type, "description": description}
            required.append(param_name)

        schema = {
            "type": "object",
            "properties": properties,
            "required": required,
        }

    tool_spec = {
        "type": "function",
        "function": {
            "name": name,
            "description": doc.split("\n\n")[0].strip(),  # First line as short desc
            "parameters": schema,
        },
    }

    TOOL_REGISTRY[name] = {
        "function": func,
        "schema": tool_spec,
    }

    return tool_spec


def get_all_tools() -> list[dict[str, Any]]:
    """Get all registered tools as a list of API-compatible specifications."""
    return [data["schema"] for data in TOOL_REGISTRY.values()]


def get_tool_executor(name: str) -> Callable | None:
    """Get the executor function for a tool by name.

    Args:
        name: Tool name

    Returns:
        Function reference or None if tool not found
    """
    tool_data = TOOL_REGISTRY.get(name)
    return tool_data["function"] if tool_data else None


def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    """Execute a registered tool with given arguments.

    Args:
        name: Tool name
        arguments: Dictionary of arguments

    Returns:
        Result as string
    """
    executor = get_tool_executor(name)

    if not executor:
        return f"Error: Unknown tool '{name}'"

    try:
        result = executor(**arguments)
        return result
    except Exception as e:
        return f"Error executing '{name}': {str(e)}"


# Register built-in tools
register_tool(read_file)
register_tool(write_file)
register_tool(list_dir)
register_tool(execute_command)
register_tool(search_codebase)


__all__ = [
    "register_tool",
    "get_all_tools",
    "get_tool_executor",
    "execute_tool",
    "TOOL_REGISTRY",
]
