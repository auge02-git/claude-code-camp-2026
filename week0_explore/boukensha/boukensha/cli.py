"""Text-UI / Einstieg (Diagramm-Knoten ``tui.rb`` + ``> bounkensha``).

Aufrufe:
- ``boukensha``                → interaktive REPL
- ``boukensha --dsl <datei>``  → skriptbaren Ablauf ausführen (siehe run_dsl)
- ``boukensha --no-connect``   → nicht automatisch zum MUD verbinden (Testlauf)
"""

from __future__ import annotations

import argparse
import os
import sys

from .agent import Agent
from .config import Config
from .logger import latest_mud_session_log
from .mud import MudManager

LOCAL_LLM_DEFAULT_URL = "http://127.0.0.1:1234"
LOCAL_LLM_DEFAULT_MODEL = "qwen/qwen-3-5-9b"


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
        help="nutzt einen lokalen Anthropic-kompatiblen LLM-Server",
    )
    parser.add_argument(
        "--llm-base-url",
        metavar="URL",
        help="LLM-Endpoint (z. B. http://127.0.0.1:1234), überschreibt Config/Env",
    )
    parser.add_argument(
        "--api-key",
        metavar="KEY",
        help="API-Key für LLM-Gateway (z. B. LiteLLM Virtual Key); überschreibt ANTHROPIC_API_KEY",
    )
    parser.add_argument(
        "--model",
        metavar="NAME",
        help="Modellname für den LLM-Aufruf (z. B. google/gemma-4-12b-qat)",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=5,
        help="max. Werkzeug-Iterationen pro Ziel (Standard 5; höher für Navigation/Suche)",
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    letztes_log = latest_mud_session_log()
    if letztes_log is not None:
        # Maschinenlesbar fuer Wrapper-Skripte und direkt sichtbar in der Shell.
        print(f"BOUKENSHA_LAST_LOG={letztes_log}")
        print(f"Letztes MUD-Log: {letztes_log}")
    else:
        print("BOUKENSHA_LAST_LOG=")
        print("Letztes MUD-Log: (keins gefunden)")

    config = Config.load()
    if args.llm_base_url:
        config.llm_base_url = args.llm_base_url
    if args.api_key:
        config.llm_api_key = args.api_key
    if args.model:
        config.model = args.model

    if args.local_llm:
        config.llm_base_url = config.llm_base_url or LOCAL_LLM_DEFAULT_URL
        # Im Local-LLM-Modus gilt ohne explizites --model der lokale Default.
        if not args.model:
            config.model = os.environ.get("BOUKENSHA_LLM_MODEL") or os.environ.get(
                "ANTHROPIC_LLM_MODEL"
            ) or LOCAL_LLM_DEFAULT_MODEL

    # Prüfe, ob ein gültiger LLM-Endpoint verfügbar ist
    has_api_key = bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())
    has_local_endpoint = bool(config.llm_base_url)
    if not has_api_key and not has_local_endpoint:
        print(
            "❌ Fehler: Kein LLM-Endpoint konfiguriert.\n"
            "   Optionen:\n"
            "   A) API-Key setzen: export ANTHROPIC_API_KEY=sk-ant-…\n"
            "   B) Lokalen Server nutzen: boukensha --local-llm (benötigt http://127.0.0.1:1234)\n"
            "   C) Endpoint über Env: export BOUKENSHA_LLM_BASE_URL=http://your.server:port",
            file=sys.stderr,
        )
        return 1

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
            print(f"LLM-Modell: {config.model}")
            if config.llm_api_key:
                masked = config.llm_api_key[:6] + "****" if len(config.llm_api_key) > 6 else "****"
                print(f"LLM-API-Key: {masked}")

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
