"""Utilidades compartilhadas entre os 21 projetos do portfolio."""
from .env import get_env, require_env
from .llm_clients import LLMClient, MockLLMClient, get_default_client
from .security import apply_security

__all__ = [
    "get_env",
    "require_env",
    "LLMClient",
    "MockLLMClient",
    "get_default_client",
    "apply_security",
]
