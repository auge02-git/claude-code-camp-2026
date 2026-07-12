"""Text-UI / Einstieg (Diagramm-Knoten ``tui.rb`` + ``> bounkensha``).

Aufrufe:
- ``boukensha``                → interaktive REPL
- ``boukensha --dsl <datei>``  → skriptbaren Ablauf ausführen (siehe run_dsl)
- ``boukensha --no-connect``   → nicht automatisch zum MUD verbinden (Testlauf)
"""

from __future__ import annotations

import argparse
import sys

from .agent import Agent
from .config import Config
from .mud import MudManager


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="boukensha",
        description="Boukensha — Abenteurer-Agent für den tbaMUD (Python-Baseline).",
    )
    parser.add_argument("--dsl", metavar="DATEI", help="skriptbaren Ablauf ausführen")
    parser.add_argument("--no-connect", action="store_true", help="nicht zum MUD verbinden")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    config = Config.load()
    mud = MudManager(host=config.mud_host, port=config.mud_port)

    if not args.no_connect:
        print("Verbinde zum MUD …")
        print(mud.connect())
        print(mud.login())  # ohne Argumente → credentials.json (mud-mcp)

    agent = Agent(config=config, mud=mud)

    try:
        if args.dsl:
            from .run_dsl import run_dsl_file

            run_dsl_file(agent, args.dsl)
        else:
            from .repl import repl

            repl(agent)
    finally:
        mud.close()
    return 0
