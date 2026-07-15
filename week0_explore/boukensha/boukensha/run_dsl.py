"""Skriptbare Abläufe (Diagramm-Knoten ``run_dsl.rb``).

Ein „Journey"-Skript ist eine einfache Textdatei: eine Anweisung pro Zeile,
Leerzeilen und ``#``-Kommentare werden ignoriert. Jede Zeile wird als
``Your Prompt`` an den Agenten gegeben.

Beispiel (``journeys/trinken_essen.txt``)::

    # Erst Wasser, dann Essen besorgen
    Geh zum Brunnen am Temple Square und trink.
    Töte einen einzelnen Fido und iss das Fleisch.
"""

from __future__ import annotations

from pathlib import Path
from typing import IO

from .agent import Agent


def run_dsl_file(agent: Agent, pfad: str, log_datei: IO[str] | None = None) -> None:
    """Führt jede nicht-leere, nicht-kommentierte Zeile als Agenten-Schritt aus.

    Wenn ``log_datei`` übergeben wird, werden Anweisung und Antwort zusätzlich
    zur Terminal-Ausgabe dorthin geschrieben.
    """
    for zeile in Path(pfad).read_text(encoding="utf-8").splitlines():
        anweisung = zeile.strip()
        if not anweisung or anweisung.startswith("#"):
            continue
        print(f"\n» {anweisung}")
        ausgabe = agent.step(anweisung)
        print(ausgabe)
        if log_datei:
            log_datei.write(f"» {anweisung}\n{ausgabe}\n\n")
            log_datei.flush()
