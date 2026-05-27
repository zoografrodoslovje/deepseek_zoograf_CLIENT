"""Status Bar Widget - Shows token count, model name, and connection status"""

from textual.widgets import Static
from textual.containers import Container


class StatusBar(Container):
    """Custom status bar widget."""

    CSS = """
    #status-bar {
        height: 1;
        background: $bg-darker;
        color: $text-secondary;
        padding: 0 2;
        content-align: left middle;
    }

    .status-item {
        margin-right: 2;
    }

    .token-count {
        color: $accent-info;
    }

    .model-name {
        color: $brand-secondary;
    }

    .connection-status {
        color: $accent-success;
    }

    .connection-error {
        color: $accent-error;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tokens_used = 0
        self._max_tokens = 64000
        self._current_model = "deepseek-chat"
        self._is_connected = True

    def compose(self):
        yield Static(
            f"[dim]Model:[/dim] [span class='model-name']{self._current_model}[/span]",
            id="model-display",
            classes="status-item",
            markup=True,
        )
        yield Static(
            f"[dim]Tokens:[/dim] [span class='token-count']{self._tokens_used}/{self._max_tokens}[/span]",
            id="token-display",
            classes="status-item",
            markup=True,
        )
        yield Static(
            f"[span class='connection-status']● Connected[/span]",
            id="connection-display",
            classes="status-item",
            markup=True,
        )

    def update_tokens(self, tokens_used: int, max_tokens: int = 64000):
        """Update token usage display."""
        self._tokens_used = tokens_used
        self._max_tokens = max_tokens
        self.query_one("#token-display", Static).update(
            f"[dim]Tokens:[/dim] [span class='token-count']{tokens_used}/{max_tokens}[/span]"
        )

    def update_model(self, model_name: str):
        """Update current model display."""
        self._current_model = model_name
        self.query_one("#model-display", Static).update(
            f"[dim]Model:[/dim] [span class='model-name']{model_name}[/span]"
        )

    def update_connection(self, is_connected: bool):
        """Update connection status display."""
        self._is_connected = is_connected
        status_text = "Connected" if is_connected else "Disconnected"
        status_class = "connection-status" if is_connected else "connection-error"

        self.query_one("#connection-display", Static).update(
            f"[span class='{status_class}']● {status_text}[/span]"
        )
