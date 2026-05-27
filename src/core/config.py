"""Configuration Module - Environment and Settings"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    # API Configuration
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv(
        "DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"
    )
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "deepseek-chat")

    # Context Configuration
    MAX_CONTEXT_TOKENS: int = int(os.getenv("MAX_CONTEXT_TOKENS", "64000"))

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Application Root
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    PROJECT_DIR: Path = ROOT_DIR / "src"

    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """Validate configuration. Returns (is_valid, list_of_errors)."""
        errors = []

        if not cls.DEEPSEEK_API_KEY:
            errors.append("DEEPSEEK_API_KEY is required but not set in .env file")

        return len(errors) == 0, errors

    @classmethod
    def get_model_options(cls) -> list[str]:
        """Return available model options."""
        return ["deepseek-chat", "deepseek-reasoner"]

    @property
    def is_api_key_set(self) -> bool:
        """Check if API key is configured."""
        return bool(self.DEEPSEEK_API_KEY.strip())

    @property
    def supports_reasoning(self) -> bool:
        """Check if reasoning model is supported."""
        return "deepseek-reasoner" in self.get_model_options()
