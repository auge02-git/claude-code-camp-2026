"""Interaktive Schleife (Diagramm-Knoten ``repl.rb``).

Liest Anweisungen des Nutzers, gibt sie an den Agenten (``Your Prompt``) und
zeigt dessen Ausgabe. Deutschsprachig. ``rich`` ist optional (Fallback: print).
"""

from __future__ import annotations

from typing import IO

from .agent import Agent

try:
    from rich.console import Console

    _console = Console()

    def _out(text: str) -> None:
        _console.print(text)
except ImportError:  # pragma: no cover
    def _out(text: str) -> None:
        print(text)


def repl(agent: Agent, log_datei: IO[str] | None = None) -> None:
    """Startet die interaktive Eingabeschleife (Ende mit ``exit``/``quit``).

    Wenn ``log_datei`` übergeben wird, werden Prompts und Antworten zusätzlich
    zur Terminal-Ausgabe dorthin geschrieben (gleiche Formatierung wie die
    bestehenden ``mud-journeys-*.log`` Dateien).
    """
    _out("[bold]Boukensha[/bold] bereit. Anweisung eingeben (oder 'exit').")
    while True:
        try:
            prompt = input("\nboukensha> ").strip()
        except (EOFError, KeyboardInterrupt):
            _out("\nTschüss.")
            if log_datei:
                log_datei.write("\n» (Sitzung beendet)\n")
            return
        if prompt.lower() in {"exit", "quit", "ende"}:
            _out("Tschüss.")
            if log_datei:
                log_datei.write("\n» (Sitzung beendet)\n")
            return
        if not prompt:
            continue
        ausgabe = agent.step(prompt)
        _out(ausgabe)
        if log_datei:
            log_datei.write(f"» {prompt}\n{ausgabe}\n\n")
            log_datei.flush()
