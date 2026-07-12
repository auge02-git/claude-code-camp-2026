"""Boukensha (冒険者) — der Player-Journey-Agent.

Neue, **additive** Python-Umsetzung der Architektur aus
``docs/plans/Claude Code Camp Agent Architecture - Baseline.json``.

Leitplanken (siehe ``docs/plans/vorgaben.md``):
- Bestehende ``.rb``-Dateien und ``.boukensha/`` werden NICHT verändert.
- Der MudManager wird aus ``mud_mcp.session`` **wiederverwendet** (nur importiert).

Der Einstiegsknoten ``Bounkensha.run()`` aus dem Diagramm entspricht der Funktion
:func:`run` hier.
"""

from __future__ import annotations

__all__ = ["run", "__version__"]

__version__ = "0.1.0"


def run(argv: list[str] | None = None) -> int:
    """Bootstrap + Start (Diagramm-Knoten ``Bounkensha.run()``).

    Verdrahtet Konfiguration, Logger, Kontext, Agent und startet die REPL bzw.
    — bei ``--dsl <datei>`` — einen skriptbaren Ablauf. Delegiert an die CLI.
    """
    from .cli import main

    return main(argv)
