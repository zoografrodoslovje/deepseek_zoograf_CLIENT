"""
HERO UI POR — Light Theme
Clean, bright terminal UI with hero-style bold accents.
"""
from textual.theme import Theme

HERO_UI_POR_LIGHT = Theme(
    name="hero-ui-por-light",
    primary="#2563EB",
    secondary="#7C3AED",
    accent="#F59E0B",
    warning="#F59E0B",
    error="#EF4444",
    success="#10B981",
    foreground="#1E293B",
    background="#FAFAF8",
    surface="#FFFFFF",
    panel="#FFFFFF",
    boost="#E2F0FF",
    dark=False,
    variables={
        "block-cursor-text-style": "none",
        "block-cursor-foreground": "#FFFFFF",
        "block-cursor-background": "#2563EB",
        "footer-background": "#F1F5F9",
        "footer-foreground": "#64748B",
        "header-background": "#2563EB",
        "header-foreground": "#FFFFFF",
    },
)

# CSS for the entire app
APP_CSS = """
Screen {
    background: #FAFAF8;
}

ChatView {
    background: #FFFFFF;
    border: none;
    padding: 0 1;
}

ChatView:focus-within {
    border: none;
}

RichLog {
    background: #FFFFFF;
    padding: 0 1;
}

InputArea {
    background: #FFFFFF;
    border-top: solid #E2E8F0;
    height: 8;
    padding: 1 1;
}

InputArea TextArea {
    background: #FFFFFF;
    border: tall #CBD5E1;
    padding: 1 2;
    color: #1E293B;
}

InputArea TextArea:focus {
    border: tall #2563EB;
}

StatusBar {
    background: #F1F5F9;
    color: #64748B;
    border-top: solid #E2E8F0;
    height: 1;
    padding: 0 2;
}

#chat-container {
    background: #FFFFFF;
    border: none;
}

#input-container {
    background: #FFFFFF;
    border-top: solid #E2E8F0;
    height: auto;
    min-height: 6;
    padding: 1;
}

.message-row {
    margin: 1 0;
    padding: 1 2;
}

.message-user {
    background: #EFF6FF;
    color: #1E293B;
    border-left: solid #2563EB;
    padding: 1 2;
    margin: 1 0;
}

.message-assistant {
    background: #FFFFFF;
    color: #1E293B;
    padding: 1 2;
    margin: 1 0;
}

.message-tool {
    color: #64748B;
    padding: 0 2;
    margin: 0 0;
}

.tool-bar {
    background: #F8FAFC;
    color: #475569;
    height: 3;
    padding: 0 1;
}

.tool-button {
    background: #2563EB;
    color: #FFFFFF;
    padding: 0 2;
    height: 1;
}

.tool-button:hover {
    background: #1D4ED8;
}

.status-model {
    color: #2563EB;
}

.status-tokens {
    color: #64748B;
}

.status-api {
    color: #10B981;
}

.status-api.disconnected {
    color: #EF4444;
}
"""
