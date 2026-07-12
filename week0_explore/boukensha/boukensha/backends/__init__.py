"""LLM-Backends (Diagramm-Knoten ``backends/``).

Kapselt den Zugriff auf das Sprachmodell. Standard: Claude (Anthropic).
"""

from __future__ import annotations

from .anthropic import ClaudeBackend

__all__ = ["ClaudeBackend"]
