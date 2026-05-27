"""Markdown Rendering Utilities for Terminal"""

from typing import Optional


def escape_terminal(text: str) -> str:
    """Escape terminal special characters for safe display.

    Args:
        text: Input text to escape

    Returns:
        Escaped text safe for terminal output
    """
    # Escape ANSI sequences that could be injected maliciously
    dangerous_chars = ["\x1b", "\033"]  # Escape sequence prefixes
    result = text

    for char in dangerous_chars:
        if char in result:
            result = result.replace(char, "[ESCAPED]")

    return result


def render_code_block(content: str, language: str = "") -> str:
    """Format code block for terminal display.

    Args:
        content: Code content
        language: Programming language identifier

    Returns:
        Formatted code block string
    """
    lines = content.splitlines()

    if not lines:
        return "```\n\n```"

    # Add line numbers for larger outputs
    max_width = len(str(len(lines))) + 2
    padding = " " * max_width

    result_lines = [f"{padding}{'┌' + '─' * max(5, len(lines[0])) + '┐'}"]

    for i, line in enumerate(lines, 1):
        line_num = str(i).rjust(max_width - 1)
        # Truncate long lines for display
        display_line = line[:100] + "..." if len(line) > 100 else line
        result_lines.append(f"{line_num}│ {display_line}")

    result_lines.append(f"{padding}{'└' + '─' * max(5, len(lines[-1])) + '┘'}")

    return "\n".join(result_lines)


def format_message(role: str, content: str) -> tuple[str, str]:
    """Format a chat message with role styling.

    Args:
        role: Message role ('user', 'assistant', 'system')
        content: Message content

    Returns:
        Tuple of (role_label, formatted_content)
    """
    role_styles = {
        "user": ("You", "#7aa2f7"),  # Blue
        "assistant": ("DeepSeek", "#9ece6a"),  # Green
        "system": ("System", "#e0af68"),  # Orange
    }

    label, color = role_styles.get(role, ("Unknown", "#ffffff"))
    escaped_content = escape_terminal(content)

    return f"[{label}]", escaped_content


__all__ = ["escape_terminal", "render_code_block", "format_message"]
