"""Claude-Backend (Anthropic Messages-API).

Modell laut Vorgaben: **Haiku 4.5** (Default), Alternative **Sonnet 4.6** —
umschaltbar über ``settings.yml`` (siehe :mod:`boukensha.config`).

Der ``ANTHROPIC_API_KEY`` wird aus der Umgebung gelesen. Der Import des
``anthropic``-SDK erfolgt verzögert, damit das Paket auch ohne installiertes SDK
importierbar bleibt (Gerüst-tolerant).

## Prompt-Caching (Token-Ersparnis)
In der Agentic Loop werden **Werkzeug-Definitionen** und **System-Prompt** bei
JEDEM Schritt erneut gesendet, dazu wächst der Nachrichtenverlauf. Mit
``cache_control: {"type": "ephemeral"}`` markieren wir Cache-Breakpoints, sodass
dieser statische/bereits gesendete Präfix serverseitig zwischengespeichert und
nur einmal (statt bei jedem Schritt) voll berechnet wird. Wichtig: ``cache_control``
gehört an einzelne **Content-Blöcke** (Tools/System/Messages), NICHT als
Top-Level-Parameter von ``messages.create`` — Letzteres existiert in der API nicht.

Hinweis: Caching greift erst ab einer Mindest-Präfixlänge (Sonnet ~1024,
Haiku ~2048 Tokens). Darunter ignoriert die API ``cache_control`` folgenlos.
"""

from __future__ import annotations

import os

from ..config import DEFAULT_MODEL

# Standard-Cache-Marker (kurzlebig, ~5 Min TTL serverseitig).
_CACHE = {"type": "ephemeral"}


def _system_with_cache(system: str) -> list[dict]:
    """System-Prompt als Content-Block mit Cache-Breakpoint."""
    return [{"type": "text", "text": system, "cache_control": _CACHE}]


def _tools_with_cache(tools: list[dict]) -> list[dict]:
    """Kopie der Werkzeuge; setzt den Cache-Breakpoint auf das LETZTE Werkzeug.

    Ein Breakpoint am Ende der Werkzeugliste cacht den gesamten (statischen)
    Werkzeug-Block. Die Eingabe wird nicht mutiert.
    """
    if not tools:
        return tools
    kopie = [dict(t) for t in tools]
    kopie[-1] = {**kopie[-1], "cache_control": _CACHE}
    return kopie


def _messages_with_cache(messages: list[dict]) -> list[dict]:
    """Setzt einen Cache-Breakpoint auf die LETZTE Nachricht (inkrementelles Caching).

    In der Agentic Loop ist die jeweils letzte Nachricht stets eine User-Nachricht
    (Prompt-Text oder ``tool_result``-Liste). Ihr Inhalt wird — ohne Mutation der
    Eingabe — so umgeformt, dass ihr letzter Content-Block den Breakpoint trägt.
    So wird der wachsende Verlauf schrittweise mitgecacht (die API prüft die
    letzten Blöcke automatisch auf Treffer).
    """
    if not messages:
        return messages
    out = list(messages)
    letzte = dict(out[-1])
    inhalt = letzte.get("content")

    if isinstance(inhalt, str):
        # Reiner Text -> ein Textblock mit Breakpoint.
        letzte["content"] = [{"type": "text", "text": inhalt, "cache_control": _CACHE}]
    elif isinstance(inhalt, list) and inhalt and all(isinstance(b, dict) for b in inhalt):
        # Liste von Blöcken (z. B. tool_result) -> Breakpoint auf den letzten Block.
        neu = [dict(b) for b in inhalt]
        neu[-1] = {**neu[-1], "cache_control": _CACHE}
        letzte["content"] = neu
    else:
        # SDK-Objekte o. Ä.: nicht anfassen (bleibt uncached, kein Fehler).
        return messages

    out[-1] = letzte
    return out


class ClaudeBackend:
    """Dünne Hülle um ``anthropic.Anthropic().messages.create`` mit Prompt-Caching."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        max_tokens: int = 1024,
        use_cache: bool = True,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self.use_cache = use_cache
        self.base_url = base_url
        self.api_key = api_key    # expliziter Key (Gateway-Pflicht); None → SDK-Default
        self._client = None  # verzögert initialisiert

    def _client_lazy(self):
        if self._client is None:
            import anthropic  # verzögerter Import

            # Priorität: expliziter api_key → ANTHROPIC_API_KEY → Dummy (nur bei base_url).
            kwargs: dict = {}
            if self.api_key:
                kwargs["api_key"] = self.api_key
            elif self.base_url:
                kwargs["api_key"] = os.environ.get("ANTHROPIC_API_KEY", "local-dev-key")
            if self.base_url:
                kwargs["base_url"] = self.base_url.rstrip("/")
            self._client = anthropic.Anthropic(**kwargs)
        return self._client

    def complete(self, system: str, messages: list[dict], tools: list[dict]):
        """Ein Aufruf der Messages-API (mit Prompt-Caching, falls aktiviert).

        Gibt die rohe Antwort zurück (kann Text- und ``tool_use``-Blöcke enthalten).
        Die Agentic Loop wertet ``stop_reason``/``content`` aus (siehe
        :mod:`boukensha.agent`).
        """
        client = self._client_lazy()
        system_text = system or "Du bist Boukensha, ein Abenteurer, der einen MUD spielt."

        if self.use_cache:
            system_param = _system_with_cache(system_text)
            tools_param = _tools_with_cache(tools)
            messages_param = _messages_with_cache(messages)
        else:
            system_param = system_text
            tools_param = tools
            messages_param = messages

        return client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_param,
            tools=tools_param,
            messages=messages_param,
        )
