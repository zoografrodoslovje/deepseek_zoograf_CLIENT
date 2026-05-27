"""Input Area Widget - Multi-line input with history navigation"""

from textual.app import ComposeResult
from textual.widgets import Input, Button
from textual.containers import Horizontal
from textual.binding import Binding
from textual.message import Message


class InputArea(Horizontal):
    """Custom input area with message history support."""

    class Submit(Message):
        """Posted when the user presses Enter to submit input."""

        def __init__(self, text: str) -> None:
            super().__init__()
            self.text = text

    CSS = """
    #input-area {
        height: 3;
        width: 1fr;
        padding: 0 1;
        background: $bg-light;
    }

    #input-field {
        width: 1fr;
        color: $text-primary;
    }

    #send-btn {
        margin-left: 1;
    }
    """

    BINDINGS = [
        Binding("enter", "submit", "Send"),
        Binding("shift+enter", "newline", "Newline"),
        Binding("ctrl+k", "clear", "Clear"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._history: list[str] = []
        self._history_index: int = -1
        self._has_sended: bool = False

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Type your message...", id="input-field")
        yield Button("Send", id="send-btn")

    async def on_mount(self):
        """Focus input field when mounted."""
        self.query_one("#input-field", Input).focus()

    @property
    def text(self) -> str:
        """Get current input text."""
        return self.query_one("#input-field", Input).value

    @text.setter
    def text(self, value: str):
        """Set input text."""
        self.query_one("#input-field", Input).value = value

    def action_submit(self):
        """Handle Enter key press."""
        self.post_message(self.Submit(self.text))

    def action_newline(self):
        """Handle Shift+Enter for new line."""
        pass

    def action_clear(self):
        """Clear input field."""
        self.text = ""
        self._history_index = -1
        self._has_sended = False

    def get_text_and_reset(self) -> str | None:
        """Get current text and reset. Returns None if empty."""
        text = self.text.strip()
        if not text:
            return None

        # Add to history only if different from last entry
        if not self._history or self._history[-1] != text:
            self._history.append(text)
            self._history_index = len(self._history) - 1

        self._has_sended = True
        self.text = ""
        return text

    def restore_history_up(self) -> bool:
        """Restore previous history item. Returns True if successful."""
        if self._has_sended:
            return False

        if self._history_index > 0:
            self._history_index -= 1
            self.text = self._history[self._history_index]
            return True
        return False

    def restore_history_down(self) -> bool:
        """Restore next history item. Returns True if successful."""
        if self._history_index >= len(self._history) - 1:
            self._history_index = len(self._history) - 1
            self.text = self._history[self._history_index] if self._history else ""
            return True

        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            self.text = self._history[self._history_index]
            return True

        return False

    def add_to_history(self, text: str):
        """Manually add text to history."""
        if text and (not self._history or self._history[-1] != text):
            self._history.append(text)
