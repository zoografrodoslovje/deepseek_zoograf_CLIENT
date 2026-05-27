"""Multi-line input widget with history navigation."""
from textual.widgets import TextArea
from textual.widget import Widget
from textual.binding import Binding
from textual import events
from textual.message import Message
from typing import Optional


class InputArea(Widget):
    """Multi-line input with command history and submit on Enter."""

    DEFAULT_CSS = """
    InputArea {
        height: auto;
        min-height: 6;
        max-height: 12;
        background: #FFFFFF;
        border-top: solid #E2E8F0;
        padding: 1;
    }

    InputArea > #chat-input {
        background: #FFFFFF;
        border: tall #CBD5E1;
        padding: 1 2;
        margin: 1 0;
        color: #1E293B;
        min-height: 3;
    }

    InputArea > #chat-input:focus {
        border: tall #2563EB;
    }
    """

    class Submitted(Message):
        def __init__(self, text: str):
            super().__init__()
            self.text = text

    def __init__(self):
        super().__init__()
        self._history: list[str] = []
        self._history_index: int = -1
        self._input: Optional[TextArea] = None

    def compose(self):
        self._input = TextArea(
            id="chat-input",
            text="",
            language=None,
            theme="css",
            soft_wrap=True,
        )
        self._input.border_title = " Message "
        self._input.tooltip = "Type your message. Enter to send, Shift+Enter for newline, ↑/↓ for history"
        yield self._input

    def on_mount(self):
        if self._input:
            self._input.focus()

    def on_text_area_changed(self, event: TextArea.Changed):
        if self._input:
            line_count = self._input.text.count("\n") + 1
            self._input.styles.height = min(max(3, line_count), 10)

    def _submit(self):
        if self._input:
            text = self._input.text.strip()
            if text:
                self._history.append(text)
                self._history_index = len(self._history)
                self.post_message(self.Submitted(text))
                self._input.text = ""

    def _history_up(self):
        if not self._history:
            return
        if self._history_index > 0:
            self._history_index -= 1
            if self._input:
                self._input.text = self._history[self._history_index]
                self._input.cursor = (len(self._input.text.split("\\n")[-1]), len(self._input.text.split("\\n")) - 1)

    def _history_down(self):
        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            if self._input:
                self._input.text = self._history[self._history_index]
                self._input.cursor = (len(self._input.text.split("\\n")[-1]), len(self._input.text.split("\\n")) - 1)
        else:
            self._history_index = len(self._history)
            if self._input:
                self._input.text = ""

    def key_enter(self):
        self._submit()

    def key_up(self):
        self._history_up()

    def key_down(self):
        self._history_down()

    def focus(self):
        if self._input:
            self._input.focus()

    @property
    def text(self) -> str:
        return self._input.text if self._input else ""

    @text.setter
    def text(self, value: str):
        if self._input:
            self._input.text = value
