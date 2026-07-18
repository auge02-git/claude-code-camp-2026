"""Text-UI / Einstieg (Diagramm-Knoten ``tui.rb`` + ``> bounkensha``).

Aufrufe:
- ``boukensha``                → interaktive REPL
- ``boukensha --dsl <datei>``  → skriptbaren Ablauf ausführen und danach weitere
  Prompts in der REPL eingeben (siehe run_dsl)
- ``boukensha --no-connect``   → nicht automatisch zum MUD verbinden (Testlauf)
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from .agent import Agent
from .config import Config
from .logger import latest_mud_session_log
from .mud import MudManager

# Terminal-Log-Verzeichnis: week0_explore/logs/ (gleicher Ordner wie mud-session-Logs).
# parents[0]=boukensha/, parents[1]=week0_explore/boukensha/, parents[2]=week0_explore/
_LOGS_DIR = Path(__file__).resolve().parents[2] / "logs"


def _terminal_log_path() -> Path:
    """Erzeugt einen datierten Pfad für das Terminal-Log.

    Format: ``mud-journeys-YYYY-MM-DD.log``.  Existiert die Datei bereits,
    wird eine laufende Versionsnummer angehängt (_v2, _v3, …).
    """
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)
    datum = datetime.now().strftime("%Y-%m-%d")
    basis = _LOGS_DIR / f"mud-journeys-{datum}.log"
    if not basis.exists():
        return basis
    version = 2
    while True:
        kandidat = _LOGS_DIR / f"mud-journeys-{datum}_v{version}.log"
        if not kandidat.exists():
            return kandidat
        version += 1

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

        log_pfad = _terminal_log_path()
        print(f"Terminal-Log: {log_pfad}")
        with log_pfad.open("w", encoding="utf-8") as log_datei:
            # Kopfzeile mit Metadaten
            log_datei.write(f"# Boukensha Terminal-Log\n")
            log_datei.write(f"# Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_datei.write(f"# Modell: {config.model}\n")
            if args.dsl:
                log_datei.write(f"# DSL: {args.dsl}\n")
            log_datei.write("#\n\n")

            from .repl import repl

            if args.dsl:
                from .run_dsl import run_dsl_file

                run_dsl_file(agent, args.dsl, log_datei=log_datei)

            repl(agent, log_datei=log_datei)
    except KeyboardInterrupt:
        print("\nAbgebrochen.")
        return 130
    except Exception as fehler:  # kein roher Traceback nach außen
        print(f"\n❌ Fehler: {type(fehler).__name__}: {fehler}", file=sys.stderr)
        return 1
    finally:
        mud.close()
    return 0
