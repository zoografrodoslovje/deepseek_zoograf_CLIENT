"""Main Textual App — HERO UI POR DeepSeek CLI Tool."""
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Header, Footer, Static
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from rich.text import Text
from rich.markdown import Markdown
from rich.panel import Panel
import asyncio
import json
import sys
import os

# Add parent to path
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.ui.chat_view import ChatView
from src.ui.input_area import InputArea
from src.ui.status_bar import StatusBar
from src.ui.theme import HERO_UI_POR_LIGHT, APP_CSS
from src.core.config import Config
from src.core.client import DeepSeekClient
from src.core.context import ContextManager
from src.core.session import SessionManager
from src.tools.registry import get_tool_definitions, get_tool_handlers
from src.tools.shell import CommandRequiresConfirmation, execute_command_approved
from src.utils.logger import setup_logger


class HeroConfirmDialog(Static):
    """Simple confirmation dialog for shell commands."""
    def __init__(self, command: str, description: str):
        super().__init__()
        self.command = command
        self.description = description
        self.confirmed = False

    def on_mount(self):
        self.styles.background = "#FFFFFF"
        self.styles.border = ("solid", "#2563EB")
        self.styles.margin = (1, 2)
        self.styles.padding = (1, 2)
        self.update(
            Panel(
                f"[bold #1E293B]Execute Command?[/]\\n\\n"
                f"[#64748B]{self.description}[/]\\n"
                f"[#1E293B]$ [bold]{self.command}[/]\\n\\n"
                f"[#94A3B8]Press [bold #2563EB]Y[/] to confirm, [bold #EF4444]N[/] to cancel[/]",
                border_style="#2563EB",
            )
        )


class DeepSeekTUI(App):
    """HERO UI POR — DeepSeek Agentic Terminal Client."""

    CSS = APP_CSS
    TITLE = "HERO UI POR"
    SUB_TITLE = "DeepSeek Agentic Terminal Client"
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", priority=True),
        Binding("ctrl+l", "clear", "Clear chat"),
        Binding("ctrl+s", "save_session", "Save session"),
        Binding("ctrl+n", "new_session", "New session"),
        Binding("ctrl+m", "toggle_model", "Switch model"),
        Binding("f5", "toggle_tools", "Toggle tools"),
    ]

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.client = DeepSeekClient(self.config)
        self.context = ContextManager(max_tokens=self.config.max_tokens)
        self.session = SessionManager()
        self.logger = setup_logger(level=self.config.log_level)

        # Tools
        tool_defs = get_tool_definitions()
        tool_handlers = get_tool_handlers()
        self.client.register_tools(tool_defs, tool_handlers)

        # UI widgets
        self.chat_view = ChatView()
        self.input_area = InputArea()
        self.status_bar = StatusBar()

        self._streaming = False
        self._pending_confirmation = None
        self._tools_enabled = True
        self._session_new = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="chat-container"):
            yield self.chat_view
        with Container(id="input-container"):
            yield self.input_area
        yield self.status_bar

    def on_mount(self):
        self.register_theme(HERO_UI_POR_LIGHT)
        self.theme = "hero-ui-por-light"

        self.status_bar.set_model(self.config.default_model)
        self.status_bar.set_connected(self.config.is_configured())

        if not self.config.is_configured():
            self.chat_view.add_message(
                "assistant",
                "⚠️ **DeepSeek API key not configured.**\\n\\n"
                "Create a `.env` file with:\\n"
                "```\\n"
                "DEEPSEEK_API_KEY=sk-your-key-here\\n"
                "```\\n"
                "Or set the `DEEPSEEK_API_KEY` environment variable.",
            )
        else:
            self.chat_view.add_message(
                "assistant",
                "## 🚀 Welcome to **HERO UI POR**\\n\\n"
                "DeepSeek Agentic Terminal Client\\n\\n"
                "I can help you with:\\n"
                "- 💻 **Code** — Write, debug, refactor\\n"
                "- 📁 **Files** — Read, write, browse your project\\n"
                "- 🔍 **Search** — grep through your codebase\\n"
                "- 🛠️ **Shell** — Run commands (with your approval)\\n\\n"
                "Type your message below and press **Enter** to start!",
            )

        if self._session_new:
            self.session.new_session("DeepSeek CLI Session")
            self._session_new = False

    async def on_input_area_submitted(self, event: InputArea.Submitted):
        """Handle user input submission."""
        if self._streaming:
            return

        text = event.text
        self.chat_view.add_message("user", text)
        self.input_area.text = ""

        messages = self.chat_view.get_api_messages()
        if self.context.needs_truncation(messages):
            messages = self.context.truncate_messages(messages)

        # System prompt
        system_prompt = {
            "role": "system",
            "content": (
                "You are HERO UI POR, an advanced agentic coding assistant powered by DeepSeek. "
                "You have access to tools for reading/writing files, listing directories, "
                "executing shell commands (with user approval), and searching codebases. "
                "ALWAYS use these tools when they would help the user. "
                "Be concise, accurate, and helpful. "
                "When showing code changes, explain what you changed and why."
            ),
        }
        api_messages = [system_prompt] + messages

        self._streaming = True
        self.status_bar.set_connected(True)

        try:
            await self._process_stream(api_messages)
        except Exception as e:
            self.logger.error(f"Stream error: {e}")
            self.chat_view.add_message("assistant", f"❌ Error: {str(e)}")
        finally:
            self._streaming = False

    async def _process_stream(self, messages: list[dict]):
        """Process the streaming response with tool call handling."""
        # Initial streaming pass
        self.chat_view.start_streaming()
        tool_calls = []
        final_content = ""
        usage_info = {}

        # First pass: get the response (could have tool calls)
        async for event in self.client.stream_chat(messages):
            if event["type"] == "content":
                self.chat_view.update_streaming(event["content"])
                final_content += event["content"]

            elif event["type"] == "reasoning":
                self.chat_view.update_streaming(f"*[thinking]* {event['content']}")

            elif event["type"] == "tool_call":
                tool_calls.append(event)

            elif event["type"] == "usage":
                usage_info = event
                self.context.add_usage(
                    event.get("prompt_tokens", 0),
                    event.get("completion_tokens", 0),
                )
                self.status_bar.set_tokens(
                    self.context.total_tokens,
                    self.context.max_tokens,
                )

            elif event["type"] == "error":
                self.chat_view.finish_streaming()
                self.chat_view.add_message("assistant", f"❌ API Error: {event['content']}")
                return

        self.chat_view.finish_streaming()

        # If we have tool calls, process them
        if tool_calls:
            tool_results = []
            for tc in tool_calls:
                tool_name = tc["name"]
                tool_args = tc["arguments"]
                tool_id = tc["id"]

                # For shell commands, show confirmation dialog
                if tool_name == "execute_command":
                    cmd = tool_args.get("command", "")
                    desc = tool_args.get("description", "")
                    panel = Panel(
                        f"[bold #1E293B]🛠️ Execute Command?[/]\\n\\n"
                        f"[#64748B]{desc}[/]\\n"
                        f"[#1E293B]$ [bold]{cmd}[/]\\n\\n"
                        f"[#94A3B8]Auto-approved — command shown for transparency[/]",
                        border_style="#F59E0B",
                    )
                    self.chat_view.add_message("assistant", f"**🛠️ Tool: execute_command**")
                    self.chat_view.add_message("tool", str(panel))

                    # Auto-execute for now (user can quit if worried)
                    result = await execute_command_approved(cmd)
                    tool_results.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": result,
                    })
                    self.chat_view.add_message("tool", f"$ {cmd}\\n\\n{result[:1000]}")
                else:
                    # Other tools run directly
                    handler = get_tool_handlers().get(tool_name)
                    if handler:
                        self.chat_view.add_message("assistant", f"**🛠️ Tool: {tool_name}**")
                        try:
                            if tool_name == "execute_command":
                                result = await execute_command_approved(tool_args["command"])
                            else:
                                result = handler(**tool_args)
                            self.chat_view.add_message("tool", str(result)[:1000])
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_id,
                                "content": str(result),
                            })
                        except CommandRequiresConfirmation as crc:
                            self.chat_view.add_message(
                                "tool",
                                f"⚠️ Command requires confirmation: {crc.command}"
                            )
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_id,
                                "content": "Command cancelled — user needs to confirm",
                            })
                        except Exception as e:
                            self.chat_view.add_message("tool", f"❌ Error: {e}")
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_id,
                                "content": f"Error: {e}",
                            })

            # Send tool results back to API for final response
            if tool_results:
                new_messages = messages + [
                    {"role": "assistant", "content": final_content or None,
                     "tool_calls": [
                         {"id": tc["id"], "type": "function",
                          "function": {"name": tc["name"], "arguments": json.dumps(tc["arguments"])}}
                         for tc in tool_calls
                     ]} if final_content or tool_calls else {"role": "assistant", "content": final_content}
                ] + tool_results

                # If first assistant message has no content, clean it up
                if not final_content and tool_calls:
                    new_messages = [
                        m for m in new_messages
                        if not (m["role"] == "assistant" and not m.get("content") and not m.get("tool_calls"))
                    ]

                self.chat_view.start_streaming()
                async for event in self.client.stream_chat(new_messages):
                    if event["type"] == "content":
                        self.chat_view.update_streaming(event["content"])
                    elif event["type"] == "usage":
                        self.context.add_usage(
                            event.get("prompt_tokens", 0),
                            event.get("completion_tokens", 0),
                        )
                        self.status_bar.set_tokens(
                            self.context.total_tokens,
                            self.context.max_tokens,
                        )
                    elif event["type"] == "error":
                        self.chat_view.finish_streaming()
                        self.chat_view.add_message("assistant", f"❌ API Error: {event['content']}")
                        return
                self.chat_view.finish_streaming()

    def action_clear(self):
        """Clear the chat history."""
        self.chat_view.clear_all()
        self.context.reset()
        self.status_bar.set_tokens(0, self.context.max_tokens)
        self.chat_view.add_message("assistant", "🧹 Chat cleared. Starting fresh!")

    def action_save_session(self):
        """Save the current session."""
        messages = self.chat_view.get_api_messages()
        path = self.session.save_session(messages)
        self.chat_view.add_message(
            "assistant",
            f"💾 Session saved to `{path}`"
        )

    def action_new_session(self):
        """Start a new session."""
        self.chat_view.clear_all()
        self.context.reset()
        self.session.new_session()
        self.status_bar.set_tokens(0, self.context.max_tokens)
        self.chat_view.add_message(
            "assistant",
            "## 🆕 New Session Started\\n\\nReady to help!",
        )

    def action_toggle_model(self):
        """Toggle between chat and reasoner models."""
        if self.client.model == "deepseek-chat":
            self.client.model = "deepseek-reasoner"
        else:
            self.client.model = "deepseek-chat"
        self.status_bar.set_model(self.client.model)
        self.chat_view.add_message(
            "assistant",
            f"🔄 Switched to **{self.client.model}**",
        )

    def action_toggle_tools(self):
        """Toggle tool calling on/off."""
        self._tools_enabled = not self._tools_enabled
        status = "enabled" if self._tools_enabled else "disabled"
        self.chat_view.add_message(
            "assistant",
            f"🔧 Tools {status}",
        )


def run():
    app = DeepSeekTUI()
    app.run()
