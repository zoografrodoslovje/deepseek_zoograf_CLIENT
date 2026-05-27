"""Status bar showing model, token count, and connection status."""
from textual.widget import Widget
from textual.widgets import Static
from rich.text import Text
from typing import Optional
import psutil


class StatusBar(Widget):
    """Thin status bar at the bottom of the screen."""

    DEFAULT_CSS = """
    StatusBar {
        height: 1;
        background: #F1F5F9;
        color: #64748B;
        border-top: solid #E2E8F0;
        layout: horizontal;
        padding: 0 2;
    }

    StatusBar > #status-left {
        width: 1fr;
        content-align: left middle;
    }

    StatusBar > #status-right {
        width: 1fr;
        content-align: right middle;
    }
    """

    def __init__(self):
        super().__init__()
        self._model = "deepseek-chat"
        self._tokens = 0
        self._max_tokens = 64000
        self._connected = False
        self._left: Optional[Static] = None
        self._right: Optional[Static] = None

    def compose(self):
        self._left = Static("", id="status-left")
        self._right = Static("", id="status-right")
        yield self._left
        yield self._right

    def on_mount(self):
        self._refresh()

    def set_model(self, model: str):
        self._model = model
        self._refresh()

    def set_tokens(self, used: int, max_tokens: int = 64000):
        self._tokens = used
        self._max_tokens = max_tokens
        self._refresh()

    def set_connected(self, connected: bool):
        self._connected = connected
        self._refresh()

    def _refresh(self):
        if not self._left or not self._right:
            return

        left = Text()
        left.append(" HERO", style="bold #2563EB")
        left.append(" UI", style="bold #7C3AED")
        left.append(" POR ", style="bold #F59E0B")
        left.append(f"│ {self._model}", style="#64748B")
        self._left.update(left)

        pct = int((self._tokens / self._max_tokens) * 100) if self._max_tokens > 0 else 0
        right = Text()
        right.append(f"tokens: {self._tokens:,}/{self._max_tokens:,} ({pct}%)", style="#94A3B8")
        right.append(" │ ")
        dot = "●" if self._connected else "○"
        dot_style = "#10B981" if self._connected else "#EF4444"
        right.append(f"{dot} API", style=dot_style)
        self._right.update(right)
