"""Basisklasse für Werkzeuge."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..mud import MudManager


class Tool(ABC):
    """Ein Werkzeug, das die Agentic Loop aufrufen kann.

    Unterklassen setzen ``name``, ``description`` (deutsch) und ``input_schema``
    (JSON-Schema der Argumente) und implementieren :meth:`run`.
    """

    name: str = ""
    description: str = ""
    input_schema: dict = {"type": "object", "properties": {}}

    @abstractmethod
    def run(self, mud: MudManager, **kwargs) -> str:
        """Führt das Werkzeug aus und liefert das (bereinigte) MUD-Ergebnis."""
        raise NotImplementedError

    def anthropic_schema(self) -> dict:
        """Schema im Format der Anthropic-Messages-API (``tools``-Eintrag)."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }
