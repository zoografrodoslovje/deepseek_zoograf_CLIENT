"""Main Application - Orchestrates UI, Core Logic, and Tools"""

import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.binding import Binding
from pathlib import Path

from core.client import DeepSeekClient
from core.context import ContextManager
from core.session import SessionManager
from core.config import Config
from tools.registry import get_all_tools, execute_tool
from .chat_view import ChatWidget
from .input_area import InputArea
from .status_bar import StatusBar


class DeepSeekApp(App):
    """Main Textual application for DeepSeek CLI Tool."""

    CSS_PATH = "theme.css"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "interrupt", "Interrupt"),
        Binding("d", "clear_session", "Clear Chat"),
        Binding("s", "save_session", "Save Session"),
        Binding("o", "load_session", "Load Session"),
        Binding("?", "help", "Help"),
    ]

    def __init__(self):
        super().__init__()
        self._client: DeepSeekClient | None = None
        self._context_manager: ContextManager | None = None
        self._session_manager: SessionManager | None = None
        self._is_streaming: bool = False
        self._update_func = None

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header(show_clock=True)
        yield ChatWidget(id="chat-widget")
        yield StatusBar(id="status-bar")
        yield InputArea(id="input-area")
        yield Footer()

    async def on_mount(self):
        """Initialize components when app mounts."""
        # Initialize components
        self._client = DeepSeekClient()
        self._context_manager = ContextManager(self._client)
        self._session_manager = SessionManager()

        # Set up system prompt
        await self._context_manager.add_system_message(
            "You are a helpful coding assistant integrated into an agentic terminal environment. "
            "You have access to file reading, writing, directory listing, shell command execution, "
            "and codebase search tools. Respond helpfully and concisely."
        )

        # Update status bar
        self.query_one("#status-bar", StatusBar).update_connection(True)
        self.query_one("#status-bar", StatusBar).update_model(
            self._client.current_model
        )

        # Add welcome message
        chat_widget = self.query_one("#chat-widget", ChatWidget)
        await chat_widget.add_message(
            "assistant",
            "Welcome to DeepSeek CLI! Type your message or use `?` for help.\n\n"
            "**Available Commands:**\n"
            "- `Ctrl+C`: Interrupt current operation\n"
            "- `D`: Clear conversation\n"
            "- `S`: Save session\n"
            "- `O`: Load session\n"
            "- `Q`: Quit application",
        )

    async def action_quit(self):
        """Handle quit action."""
        await self.exit()

    async def action_interrupt(self):
        """Handle interrupt (for breaking long operations)."""
        if self._is_streaming:
            # Cancel any pending tasks
            self._is_streaming = False
            print("\n[Interrupted]")

    async def action_clear_session(self):
        """Clear conversation history."""
        chat_widget = self.query_one("#chat-widget", ChatWidget)
        await chat_widget.clear()
        if self._context_manager:
            await self._context_manager.clear()

        # Add confirmation
        await chat_widget.add_message("assistant", "Conversation cleared.")

    async def action_save_session(self):
        """Save current session."""
        if not self._context_manager or not self._session_manager:
            return

        messages = self._context_manager.messages
        session_id = await self._session_manager.create_session()
        await self._session_manager.save_session(session_id, messages)

        chat_widget = self.query_one("#chat-widget", ChatWidget)
        await chat_widget.add_message(
            "assistant", f"Session saved with ID: {session_id}"
        )

    async def action_load_session(self):
        """Load previous session."""
        if not self._session_manager:
            return

        sessions = await self._session_manager.list_sessions()

        if not sessions:
            chat_widget = self.query_one("#chat-widget", ChatWidget)
            await chat_widget.add_message(
                "assistant", "No saved sessions found."
            )
            return

        # Show available sessions (in practice, would use a picker)
        session_list = "\n".join(f"- {s['id']}: {s['name']} ({s['message_count']} msgs)" for s in sessions[:5])
        chat_widget = self.query_one("#chat-widget", ChatWidget)
        await chat_widget.add_message(
            "assistant",
            f"Available sessions:\n{session_list}\n\nUse the ID to load (manual selection for now)."
        )

    async def on_input_submitted(self, event: InputArea.Submit) -> None:
        """Handle input submission."""
        await self._handle_message(event)

    async def _handle_message(self, event=None) -> None:
        """Process user message and generate response."""
        if self._is_streaming:
            return

        input_area = self.query_one("#input-area", InputArea)
        chat_widget = self.query_one("#chat-widget", ChatWidget)
        status_bar = self.query_one("#status-bar", StatusBar)

        # Get message text
        text = input_area.get_text_and_reset()
        if not text:
            return

        # Add user message to display
        await chat_widget.add_message("user", text)

        # Add to context
        await self._context_manager.add_message("user", text)

        # Prepare messages for API
        messages = await self._context_manager.get_messages_for_api()

        # Enable streaming mode
        self._is_streaming = True
        input_area.disabled = True
        status_bar.update_connection(False)

        try:
            # Check if AI wants to use tools
            tools = get_all_tools()

            stream_generator = self._client.chat_stream(messages, tools=tools)

            # Start receiving tokens
            full_response = ""

            async for chunk_type, chunk_data in stream_generator:
                if not self._is_streaming:
                    break

                if chunk_type == "tool_call":
                    # Handle tool call
                    tool_name = chunk_data["name"]
                    args_str = chunk_data["arguments"] or "{}"

                    try:
                        import json

                        args = json.loads(args_str)
                    except Exception:
                        args = {}

                    # Execute tool
                    result = execute_tool(tool_name, args)

                    # Add tool result to messages
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": chunk_data["id"],
                            "content": result,
                        }
                    )

                    # Continue streaming
                    continue

                elif chunk_type == "reasoning":
                    # Display reasoning content (R1 models)
                    pass  # Can render in gray in future

                elif chunk_type == "content":
                    full_response += chunk_data
                    chat_widget.stream_content(full_response)

            # Add assistant response to context
            await self._context_manager.add_message("assistant", full_response)

        except Exception as e:
            await chat_widget.add_message(
                "assistant", f"**Error**: {str(e)}"
            )

        finally:
            self._is_streaming = False
            input_area.disabled = False
            status_bar.update_connection(True)
            input_area.focus()

    def update_tokens_used(self, count: int):
        """Update token count display."""
        config = Config
        status_bar = self.query_one("#status-bar", StatusBar)
        status_bar.update_tokens(count, config.MAX_CONTEXT_TOKENS)


# Re-export for cleaner imports
__all__ = ["DeepSeekApp"]
