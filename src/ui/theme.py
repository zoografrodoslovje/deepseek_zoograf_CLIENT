"""UI Theme - Colors, Styles, and CSS Definitions"""


THEME = {
    "colors": {
        # Primary colors
        "brand_primary": "#00d4ff",
        "brand_secondary": "#7aa2f7",
        "accent_success": "#9ece6a",
        "accent_warning": "#e0af68",
        "accent_error": "#f7768e",
        "accent_info": "#7dcfff",
        # Text colors
        "text_primary": "#c0caf5",
        "text_secondary": "#a9b1d6",
        "text_muted": "#565f89",
        "text_accent_user": "#7aa2f7",  # Blue for user messages
        "text_accent_bot": "#9ece6a",   # Green for bot messages
        "text_error": "#f7768e",
        # Background colors
        "bg_dark": "#1a1b26",
        "bg_darker": "#16161e",
        "bg_light": "#24283b",
        "bg_message_user": "#1f2335",
        "bg_message_bot": "#1f2335",
        # Border colors
        "border_default": "#414868",
        "border_focus": "#7aa2f7",
    },
    "styles": {
        "chat_container": {
            "height": "1fr",
            "padding": "1",
            "background_color": "$bg_dark",
        },
        "message": {
            "margin_bottom": "1",
            "padding": "1",
            "border": "solid $border_default",
            "border_radius": "1",
        },
        "input_row": {
            "height": "3",
            "width": "1fr",
        },
        "user_input": {
            "width": "1fr",
            "padding": "1",
            "background_color": "$bg_light",
            "color": "$text_primary",
        },
        "status_bar": {
            "height": "1",
            "background_color": "$bg_darker",
            "color": "$text_secondary",
        },
    },
    "animations": {
        "blink_speed": "1s",
        "fade_duration": "0.2s",
    },
}

# Textual CSS themes
CSS_DARK = """
Default:
    background: $background;
    color: $foreground;

#header:
    height: 1;
    background: $primary 30%;
    content-align: center middle;

#chat-container:
    width: 1fr;
    height: 1fr;
    padding: 1;
    background: $bg_dark;

.message-user:
    background: $bg_message_user;
    border-left: solid $text_accent_user;
    margin-bottom: 1;
    padding: 1;

.message-bot:
    background: $bg_message_bot;
    border-left: solid $text_accent_bot;
    margin-bottom: 1;
    padding: 1;

#input-area:
    height: 3;
    width: 1fr;
    background: $bg_light;
    padding: 1;

#input-field:
    width: 1fr;
    color: $text_primary;

#status-bar:
    height: 1;
    background: $bg_darker;
    color: $text_secondary;

/* Code blocks */
code-block:
    background: $bg_darker;
    padding: 1;
    border-radius: $border-default;

/* Scrollbar styling */
Scrollbars:
    background: $bg_light;
    opacity: 0.3;

/* Focus states */
Input:focus:
    border-style: solid $brand_primary;

Button:focus:
    background: $brand_primary;
"""

__all__ = ["THEME", "CSS_DARK"]
