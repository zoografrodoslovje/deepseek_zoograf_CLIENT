"""Configuration loader — reads .env and provides settings."""
import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Application configuration loaded from .env and environment."""

    def __init__(self, env_path: str | None = None):
        if env_path is None:
            env_path = str(Path(__file__).parent.parent.parent / ".env")
        load_dotenv(env_path)

        self.api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        self.default_model: str = os.getenv("DEFAULT_MODEL", "deepseek-chat")
        self.max_tokens: int = int(os.getenv("MAX_TOKENS", "64000"))
        self.max_output_tokens: int = int(os.getenv("MAX_OUTPUT_TOKENS", "4096"))
        self.temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def is_configured(self) -> bool:
        return bool(self.api_key) and self.api_key != "sk-your-key-here"

    def get_client_kwargs(self) -> dict:
        return {
            "api_key": self.api_key,
            "base_url": self.base_url,
        }
