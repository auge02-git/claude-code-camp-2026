"""Konkrete MUD-Werkzeuge.

Jedes Werkzeug sendet genau ein Kommando über den :class:`MudManager`. Die im
MUD-Log dokumentierten **Sicherheitsregeln** sind in den Beschreibungen kodiert,
damit das Modell sie befolgt (z. B. keine Wachen angreifen, bei „has arrived"
fliehen). Siehe ``docs/plans/vorgaben.md`` Abschnitt 5.
"""

from __future__ import annotations

from ..mud import MudManager
from .base import Tool


class LookTool(Tool):
    name = "look"
    description = "Schaut sich im aktuellen Raum um (Kommando `look`). Zeigt Ausgänge, Mobs, Gegenstände."
    input_schema = {"type": "object", "properties": {}}

    def run(self, mud: MudManager, **kwargs) -> str:
        return mud.send("look")


class MoveTool(Tool):
    name = "move"
    description = (
        "Bewegt den Charakter in eine Richtung. `direction` ist eine von "
        "north/south/east/west/up/down (oder n/s/e/w/u/d)."
    )
    input_schema = {
        "type": "object",
        "properties": {"direction": {"type": "string"}},
        "required": ["direction"],
    }

    def run(self, mud: MudManager, direction: str = "", **kwargs) -> str:
        return mud.send(direction)


class KillTool(Tool):
    name = "kill"
    description = (
        "Greift ein Ziel an (Kommando `kill <ziel>`). SICHERHEIT: nur EINZELNE, "
        "schwache Mobs (z. B. `fido`) und NUR wenn KEINE Wache (cityguard/Peacekeeper/"
        "knight/sorcerer) im Raum ist. Niemals Wachen angreifen."
    )
    input_schema = {
        "type": "object",
        "properties": {"target": {"type": "string"}},
        "required": ["target"],
    }

    def run(self, mud: MudManager, target: str = "", **kwargs) -> str:
        return mud.send(f"kill {target}", quiet_seconds=2.0, timeout=10.0)


class FleeTool(Tool):
    name = "flee"
    description = (
        "Flieht aus dem Kampf (`flee`). Bei „cityguard/Peacekeeper ... has arrived" "
        "während eines Kampfs SOFORT einsetzen (Latenz einplanen, nicht erst bei "
        "niedrigen HP)."
    )
    input_schema = {"type": "object", "properties": {}}

    def run(self, mud: MudManager, **kwargs) -> str:
        return mud.send("flee")


class LootTool(Tool):
    name = "loot_corpse"
    description = "Plündert die Leiche (`get all corpse`). SOFORT nach einem Kill, sonst frisst ein anderer Fido sie."
    input_schema = {"type": "object", "properties": {}}

    def run(self, mud: MudManager, **kwargs) -> str:
        return mud.send("get all corpse")


class EatTool(Tool):
    name = "eat"
    description = "Isst etwas aus dem Inventar (`eat <item>`, Standard: `meat`) gegen Hunger."
    input_schema = {
        "type": "object",
        "properties": {"item": {"type": "string", "default": "meat"}},
    }

    def run(self, mud: MudManager, item: str = "meat", **kwargs) -> str:
        return mud.send(f"eat {item}")


class DrinkTool(Tool):
    name = "drink"
    description = "Trinkt aus einer Quelle (`drink <quelle>`, z. B. `fountain` am Temple Square) gegen Durst."
    input_schema = {
        "type": "object",
        "properties": {"source": {"type": "string", "default": "fountain"}},
    }

    def run(self, mud: MudManager, source: str = "fountain", **kwargs) -> str:
        return mud.send(f"drink {source}")


class ScoreTool(Tool):
    name = "score"
    description = "Zeigt Charakterwerte (`score`): Level, Exp, Gold, HP."
    input_schema = {"type": "object", "properties": {}}

    def run(self, mud: MudManager, **kwargs) -> str:
        return mud.send("score", quiet_seconds=1.5, timeout=6.0)


class ReadTool(Tool):
    name = "read_pending"
    description = "Liest anstehende Ausgabe (Kampfrunden, Ereignisse) ohne Kommando — gegen Puffer-Latenz."
    input_schema = {"type": "object", "properties": {}}

    def run(self, mud: MudManager, **kwargs) -> str:
        return mud.read()


def build_default_tools() -> list[Tool]:
    """Die Standard-Werkzeuge für das MUD-Spielen."""
    return [
        LookTool(),
        MoveTool(),
        KillTool(),
        FleeTool(),
        LootTool(),
        EatTool(),
        DrinkTool(),
        ScoreTool(),
        ReadTool(),
    ]
