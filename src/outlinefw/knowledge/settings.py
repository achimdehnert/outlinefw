"""
outlinefw.knowledge.settings — Configuration for Outline Wiki integration.

Uses pydantic-settings with OUTLINE_ env prefix.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings


class KnowledgeSettings(BaseSettings):
    """Outline Wiki connection settings.

    Environment variables (prefix OUTLINE_):
        OUTLINE_URL: Base URL of Outline instance
        OUTLINE_API_TOKEN: API bearer token
        OUTLINE_DEFAULT_LIMIT: Max search results (default 10)
        OUTLINE_TIMEOUT: HTTP timeout in seconds (default 30)
    """

    url: str = "https://knowledge.iil.pet"
    api_token: str = ""
    default_limit: int = 10
    timeout: int = 30

    model_config = {"env_prefix": "OUTLINE_"}
