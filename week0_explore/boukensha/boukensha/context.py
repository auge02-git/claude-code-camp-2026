"""Kontext/Gedächtnis (Diagramm-Knoten ``Bounkensha.Context``).

Hält den Gesprächs- und Spielverlauf, den die Agentic Loop über die Schritte
Observe → Take Action → Reflect hinweg teilt. Bewusst schlank: eine Nachrichten-
Historie im Anthropic-Messages-Format plus etwas Spielzustand.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Context:
    """Geteilter Zustand der Agentic Loop."""

    system_prompt: str = ""
    # Nachrichtenverlauf im Format [{"role": "user"|"assistant", "content": ...}]
    messages: list[dict] = field(default_factory=list)
    # Letzte rohe MUD-Ausgabe (Ergebnis von "Observe").
    letzte_beobachtung: str = ""
    # Freies Feld für abgeleiteten Spielzustand (Raum, HP, …).
    zustand: dict = field(default_factory=dict)

    def add_user(self, text: str) -> None:
        """Fügt eine Nutzer-/Beobachtungsnachricht hinzu."""
        self.messages.append({"role": "user", "content": text})

    def add_assistant(self, content) -> None:
        """Fügt die Antwort des Modells hinzu (Text oder Content-Blöcke)."""
        self.messages.append({"role": "assistant", "content": content})
