"""Werkzeug-Registry (Diagramm-Knoten ``registry.rb``).

Sammelt die verfügbaren Werkzeuge und liefert ihre Schemata im Anthropic-
Tool-Format an das Backend. Die Agentic Loop (``Take Action`` → ``Tool Use``)
schlägt Werkzeuge hier per Name nach.
"""

from __future__ import annotations

from .tools.base import Tool


class ToolRegistry:
    """Namens-Register für :class:`~boukensha.tools.base.Tool`."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def anthropic_schemas(self) -> list[dict]:
        """Alle Werkzeuge als ``tools``-Liste für die Messages-API."""
        return [t.anthropic_schema() for t in self._tools.values()]

    def __len__(self) -> int:
        return len(self._tools)
