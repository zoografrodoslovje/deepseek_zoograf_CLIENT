"""Terminal markdown rendering utilities."""
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.console import Group, RenderableType
from rich.text import Text


def render_markdown(content: str) -> RenderableType:
    """Render markdown string to a Rich renderable."""
    if not content:
        return Text("")
    try:
        return Markdown(content, code_theme="default")
    except Exception:
        return Text(content)


def render_code(code: str, language: str = "") -> RenderableType:
    """Render a code block with syntax highlighting."""
    if not language:
        language = "text"
    try:
        return Syntax(code, language, theme="default", line_numbers=True)
    except Exception:
        return Text(code)
