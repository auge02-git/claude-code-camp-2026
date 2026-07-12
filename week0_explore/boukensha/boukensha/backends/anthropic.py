"""Claude-Backend (Anthropic Messages-API).

Modell laut Vorgaben: **Haiku 4.5** (Default), Alternative **Sonnet 4.6** —
umschaltbar über ``settings.yml`` (siehe :mod:`boukensha.config`).

Der ``ANTHROPIC_API_KEY`` wird aus der Umgebung gelesen (oder aus dem Agent-Home
``~/.boukensha/credentials``, das der Aufrufer setzen kann). Der Import des
``anthropic``-SDK erfolgt verzögert, damit das Paket auch ohne installiertes SDK
importierbar bleibt (Gerüst-tolerant).
"""

from __future__ import annotations

from ..config import DEFAULT_MODEL


class ClaudeBackend:
    """Dünne Hülle um ``anthropic.Anthropic().messages.create``."""

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 1024) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self._client = None  # verzögert initialisiert

    def _client_lazy(self):
        if self._client is None:
            import anthropic  # verzögerter Import

            self._client = anthropic.Anthropic()
        return self._client

    def complete(self, system: str, messages: list[dict], tools: list[dict]):
        """Ein Aufruf der Messages-API.

        Gibt die rohe Antwort zurück (kann Text- und ``tool_use``-Blöcke enthalten).
        Die Agentic Loop wertet ``stop_reason``/``content`` aus (siehe
        :mod:`boukensha.agent`).
        """
        client = self._client_lazy()
        return client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system or "Du bist Boukensha, ein Abenteurer, der einen MUD spielt.",
            tools=tools,
            messages=messages,
        )
