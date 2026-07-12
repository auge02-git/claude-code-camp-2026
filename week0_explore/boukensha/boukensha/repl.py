"""Interaktive Schleife (Diagramm-Knoten ``repl.rb``).

Liest Anweisungen des Nutzers, gibt sie an den Agenten (``Your Prompt``) und
zeigt dessen Ausgabe. Deutschsprachig. ``rich`` ist optional (Fallback: print).
"""

from __future__ import annotations

from .agent import Agent

try:
    from rich.console import Console

    _console = Console()

    def _out(text: str) -> None:
        _console.print(text)
except ImportError:  # pragma: no cover
    def _out(text: str) -> None:
        print(text)


def repl(agent: Agent) -> None:
    """Startet die interaktive Eingabeschleife (Ende mit ``exit``/``quit``)."""
    _out("[bold]Boukensha[/bold] bereit. Anweisung eingeben (oder 'exit').")
    while True:
        try:
            prompt = input("\nboukensha> ").strip()
        except (EOFError, KeyboardInterrupt):
            _out("\nTschüss.")
            return
        if prompt.lower() in {"exit", "quit", "ende"}:
            _out("Tschüss.")
            return
        if not prompt:
            continue
        ausgabe = agent.step(prompt)
        _out(ausgabe)
