"""Wrappers minimalistas para provedores LLM, com fallback mock para desenvolvimento offline."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable, Protocol

from .env import get_env


@dataclass
class LLMResponse:
    text: str
    model: str
    provider: str
    usage: dict[str, int] | None = None


class LLMClient(Protocol):
    provider: str

    def complete(self, prompt: str, *, system: str | None = None, model: str | None = None) -> LLMResponse: ...


class MockLLMClient:
    """Cliente determinístico usado quando não há API key. Útil para smoke tests."""

    provider = "mock"

    def complete(self, prompt: str, *, system: str | None = None, model: str | None = None) -> LLMResponse:
        digest = hashlib.sha256((system or "") + prompt).hexdigest()[:8] if False else hashlib.sha256(
            ((system or "") + prompt).encode("utf-8")
        ).hexdigest()[:8]
        body = (
            f"[mock-llm:{digest}] Resposta simulada para prompt de {len(prompt)} chars. "
            "Configure OPENAI_API_KEY ou GEMINI_API_KEY para usar um provedor real."
        )
        return LLMResponse(text=body, model=model or "mock-1", provider=self.provider, usage={"prompt": len(prompt), "completion": len(body)})


class OpenAIClient:
    provider = "openai"

    def __init__(self, api_key: str, default_model: str = "gpt-4o-mini") -> None:
        from openai import OpenAI  # import lazy

        self._client = OpenAI(api_key=api_key)
        self._default_model = default_model

    def complete(self, prompt: str, *, system: str | None = None, model: str | None = None) -> LLMResponse:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        chosen = model or self._default_model
        resp = self._client.chat.completions.create(model=chosen, messages=messages)
        choice = resp.choices[0].message.content or ""
        usage = {
            "prompt": getattr(resp.usage, "prompt_tokens", 0),
            "completion": getattr(resp.usage, "completion_tokens", 0),
        }
        return LLMResponse(text=choice, model=chosen, provider=self.provider, usage=usage)


class GeminiClient:
    provider = "gemini"

    def __init__(self, api_key: str, default_model: str = "gemini-1.5-flash") -> None:
        import google.generativeai as genai  # import lazy

        genai.configure(api_key=api_key)
        self._genai = genai
        self._default_model = default_model

    def complete(self, prompt: str, *, system: str | None = None, model: str | None = None) -> LLMResponse:
        chosen = model or self._default_model
        m = self._genai.GenerativeModel(chosen, system_instruction=system) if system else self._genai.GenerativeModel(chosen)
        resp = m.generate_content(prompt)
        return LLMResponse(text=resp.text or "", model=chosen, provider=self.provider)


class AnthropicClient:
    provider = "anthropic"

    def __init__(self, api_key: str, default_model: str = "claude-sonnet-4-6") -> None:
        from anthropic import Anthropic  # import lazy

        self._client = Anthropic(api_key=api_key)
        self._default_model = default_model

    def complete(self, prompt: str, *, system: str | None = None, model: str | None = None) -> LLMResponse:
        chosen = model or self._default_model
        kwargs = {"model": chosen, "max_tokens": 1024, "messages": [{"role": "user", "content": prompt}]}
        if system:
            kwargs["system"] = system
        resp = self._client.messages.create(**kwargs)
        text = "".join(block.text for block in resp.content if getattr(block, "type", "") == "text")
        usage = {"prompt": resp.usage.input_tokens, "completion": resp.usage.output_tokens}
        return LLMResponse(text=text, model=chosen, provider=self.provider, usage=usage)


def get_default_client(prefer: Iterable[str] = ("openai", "gemini", "anthropic")) -> LLMClient:
    """Retorna o primeiro provedor com API key disponível, ou um MockLLMClient."""
    for provider in prefer:
        if provider == "openai":
            key = get_env("OPENAI_API_KEY")
            if key:
                try:
                    return OpenAIClient(key)
                except Exception:
                    continue
        elif provider == "gemini":
            key = get_env("GEMINI_API_KEY") or get_env("GOOGLE_API_KEY")
            if key:
                try:
                    return GeminiClient(key)
                except Exception:
                    continue
        elif provider == "anthropic":
            key = get_env("ANTHROPIC_API_KEY")
            if key:
                try:
                    return AnthropicClient(key)
                except Exception:
                    continue
    return MockLLMClient()
