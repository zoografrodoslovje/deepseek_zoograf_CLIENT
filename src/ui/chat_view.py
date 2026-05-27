"""Chat history widget for streaming markdown responses."""
from textual.widgets import RichLog
from textual.widget import Widget
from rich.text import Text
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
from rich.console import Group, RenderableType
from rich.layout import Layout
import re
from typing import Optional

LANGUAGE_MAP = {
    "py": "python", "js": "javascript", "ts": "typescript",
    "tsx": "typescript", "jsx": "javascript", "rs": "rust",
    "go": "go", "rb": "ruby", "java": "java", "c": "c",
    "cpp": "cpp", "h": "c", "cs": "csharp", "php": "php",
    "swift": "swift", "kt": "kotlin", "scala": "scala",
    "sh": "bash", "bash": "bash", "zsh": "bash",
    "yaml": "yaml", "yml": "yaml", "json": "json",
    "xml": "xml", "html": "html", "css": "css",
    "sql": "sql", "r": "r", "toml": "toml", "md": "markdown",
    "dockerfile": "dockerfile", "makefile": "makefile",
}

class ChatMessage:
    """Stores a single chat message with its renderable."""
    def __init__(self, role: str, content: str, is_streaming: bool = False):
        self.role = role
        self.content = content
        self.is_streaming = is_streaming
        self.renderable = None

    def to_renderable(self) -> RenderableType:
        if self.role == "user":
            return Panel(
                Text(self.content, style="bold #1E293B"),
                border_style="#2563EB",
                title="[bold #2563EB]You[/]",
                title_align="left",
                padding=(0, 1),
            )
        elif self.role == "tool":
            return Panel(
                Text(self.content[:500], style="#64748B"),
                border_style="#CBD5E1",
                title="[bold #64748B]Tool[/]",
                title_align="left",
                padding=(0, 1),
            )
        else:
            return self._render_markdown(self.content)

    @staticmethod
    def _render_markdown(content: str) -> RenderableType:
        if not content:
            return Text("")
        try:
            return Markdown(content, code_theme="default")
        except Exception:
            return Text(content)

    def animate_update(self, new_content: str):
        self.content = new_content
        return self.to_renderable()


class ChatView(Widget):
    """Displays the conversation history with streaming support."""

    DEFAULT_CSS = """
    ChatView {
        overflow-y: auto;
        overflow-x: hidden;
        background: #FFFFFF;
        padding: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.messages: list[ChatMessage] = []
        self._current_streaming: Optional[ChatMessage] = None
        self._container = None

    def compose(self):
        from textual.widgets import RichLog
        self._container = RichLog(
            highlight=True,
            markup=True,
            wrap=True,
            min_width=40,
        )
        yield self._container

    def add_message(self, role: str, content: str):
        msg = ChatMessage(role, content)
        self.messages.append(msg)
        if self._container:
            self._container.write(msg.to_renderable())
        self._current_streaming = None

    def start_streaming(self):
        msg = ChatMessage("assistant", "", is_streaming=True)
        self.messages.append(msg)
        self._current_streaming = msg
        if self._container:
            self._container.write(Text("▊", style="#2563EB"))
        return msg

    def update_streaming(self, text: str):
        if self._current_streaming:
            self._current_streaming.content += text
            if self._container:
                self._container.clear()
                for m in self.messages[:-1]:
                    self._container.write(m.to_renderable())
                try:
                    self._container.write(
                        Markdown(self._current_streaming.content + " ▊", code_theme="default")
                    )
                except Exception:
                    self._container.write(
                        Text(self._current_streaming.content + " ▊")
                    )

    def finish_streaming(self):
        if self._current_streaming:
            self._current_streaming.is_streaming = False
            if self._container:
                self._container.clear()
                for m in self.messages:
                    self._container.write(m.to_renderable())
            self._current_streaming = None

    def clear_all(self):
        self.messages.clear()
        self._current_streaming = None
        if self._container:
            self._container.clear()

    def get_api_messages(self) -> list[dict]:
        result = []
        for m in self.messages:
            if m.role in ("user", "assistant") and m.content:
                result.append({"role": m.role, "content": m.content})
        return result
