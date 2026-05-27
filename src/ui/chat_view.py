"""Chat View Widget - Displays conversation history with streaming support"""

from textual.widgets import Static, RichLog
from textual.containers import ScrollableContainer
from textual.message import Message


class ChatWidget(Static):
    """Custom widget for displaying chat conversations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._message_id: int = 0

    class MessageAdded(Message):
        """Posted when a new message is added."""

        def __init__(self, message_id: int, role: str) -> None:
            super().__init__()
            self.message_id = message_id
            self.role = role

    CSS = """
    #chat-container {
        width: 1fr;
        height: 1fr;
        padding: 1;
        background: $bg-dark;
        border: solid $border-default;
    }

    .message {
        margin-bottom: 1;
        padding: 1;
        border-radius: 1;
        width: 1fr;
    }

    .message-user {
        background: $surface-2;
        border-left: solid $accent-user;
    }

    .message-bot {
        background: $surface-3;
        border-left: solid $accent-bot;
    }

    .role-label {
        font-weight: bold;
        margin-bottom: 0.5;
    }
    """

    BINDINGS = []

    def compose(self):
        yield ScrollableContainer(id="chat-container")

    async def add_message(self, role: str, content: str) -> int:
        """Add a new message to the chat.

        Args:
            role: Message role ('user' or 'assistant')
            content: Message content

        Returns:
            Assigned message ID
        """
        self._message_id += 1
        msg_id = self._message_id

        container = self.query_one("#chat-container", ScrollableContainer)

        # Create message div
        user_class = "message-user" if role == "user" else "message-bot"

        role_label = "You" if role == "user" else "DeepSeek"
        label_color = "$text-accent-user" if role == "user" else "$text-accent-bot"

        message_div = Static(
            f"[bold]{role_label}:[/bold]\n[/{label_color}]{content}",
            classes=f"message {user_class}",
            markup=True,
        )

        await container.mount(message_div)

        # Scroll to bottom
        container.scroll_end(smooth=False)

        self.post_message(self.MessageAdded(msg_id, role))

        return msg_id

    async def stream_message(
        self, role: str, initial_content: str = ""
    ) -> list[str]:
        """Start streaming a new message and track its position.

        Args:
            role: Message role
            initial_content: Content to start with

        Returns:
            List reference to append content chunks
        """
        self._message_id += 1
        msg_id = self._message_id

        container = self.query_one("#chat-container", ScrollableContainer)

        user_class = "message-user" if role == "user" else "message-bot"
        role_label = "You" if role == "user" else "DeepSeek"

        current_content = [initial_content]

        message_div = Static(
            f"[bold]{role_label}:[/bold]\n{initial_content}",
            classes=f"message {user_class}",
            markup=True,
        )

        await container.mount(message_div)

        container.scroll_end(smooth=False)

        def update_content(new_chunk: str):
            current_content.append(new_chunk)
            full_text = "".join(current_content)
            message_div.update(f"[bold]{role_label}:[/bold]\n{full_text}")
            container.scroll_end(smooth=False)

        return update_content

    async def clear(self):
        """Clear all messages from the chat."""
        container = self.query_one("#chat-container", ScrollableContainer)
        for child in list(container.children):
            await container.remove(child)
        self._message_id = 0
