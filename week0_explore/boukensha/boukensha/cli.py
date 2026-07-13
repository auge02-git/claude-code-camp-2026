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
    parser.add_argument(
        "--local-llm",
        action="store_true",
        help="nutzt einen lokalen Anthropic-kompatiblen LLM-Server (http://127.0.0.1:1234)",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=12,
        help="max. Werkzeug-Iterationen pro Ziel (Standard 12; höher für Navigation/Suche)",
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    config = Config.load()
    if args.local_llm:
        config.llm_base_url = "http://127.0.0.1:1234"

    mud = MudManager(host=config.mud_host, port=config.mud_port)

    try:
        if not args.no_connect:
            print("Verbinde zum MUD …")
            print(mud.connect())
            print(mud.login())  # ohne Argumente → credentials.json (mud-mcp)
        else:
            print("Starte ohne MUD-Verbindung (--no-connect).")
            print("Hinweis: MUD-Werkzeuge liefern in diesem Modus nur eine Klartext-Fehlermeldung.")

        if config.llm_base_url:
            print(f"LLM-Endpoint: {config.llm_base_url}")

        agent = Agent(config=config, mud=mud, max_steps=args.max_steps)

        if args.dsl:
            from .run_dsl import run_dsl_file

            run_dsl_file(agent, args.dsl)
        else:
            from .repl import repl

            repl(agent)
    except KeyboardInterrupt:
        print("\nAbgebrochen.")
        return 130
    except Exception as fehler:  # kein roher Traceback nach außen
        print(f"\n❌ Fehler: {type(fehler).__name__}: {fehler}", file=sys.stderr)
        return 1
    finally:
        mud.close()
    return 0
