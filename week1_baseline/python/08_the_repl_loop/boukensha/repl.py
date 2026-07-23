from __future__ import annotations

import boukensha
from .version import VERSION

BANNER = f"""\
boukensha {VERSION} — REPL-Modus
Tippe /help fuer eine Liste der eingebauten Befehle.
"""

HELP_TEXT = """\
Eingebaute Befehle:
  /quiet   Logging-Ausgabe unterdruecken
  /loud    Logging-Ausgabe wieder aktivieren
  /clear   Konversationsverlauf loeschen (Tools bleiben erhalten)
  /help    Diese Hilfe anzeigen
  /exit    REPL beenden
  /quit    REPL beenden
  Ctrl-D   EOF — REPL beenden
  Ctrl-C   Unterbrechen — sauber beenden
"""

BUILTIN_COMMANDS = frozenset({"/quiet", "/loud", "/clear", "/help", "/exit", "/quit"})


class Repl:
    def __init__(self, *, agent, context, logger) -> None:
        self._agent = agent
        self._context = context
        self._logger = logger
        self._turn = 0

    def run(self) -> None:
        print(BANNER)
        while True:
            try:
                line = input("boukensha> ").strip()
            except EOFError:
                print()
                break
            if not line:
                continue
            if line in BUILTIN_COMMANDS:
                self._handle_command(line)
                if line in ("/exit", "/quit"):
                    break
                continue
            self._run_turn(line)

    def _handle_command(self, cmd: str) -> None:
        if cmd == "/quiet":
            boukensha.set_quiet(True)
            print("Stille aktiviert.")
        elif cmd == "/loud":
            boukensha.set_quiet(False)
            print("Ausgabe wieder aktiviert.")
        elif cmd == "/clear":
            self._context.clear_messages()
            print("Konversationsverlauf geloescht.")
        elif cmd == "/help":
            print(HELP_TEXT)
        elif cmd in ("/exit", "/quit"):
            print("Auf Wiedersehen!")

    def _run_turn(self, user_input: str) -> None:
        self._turn += 1
        self._logger.turn(self._turn)
        self._agent._iteration = 0
        result = self._agent.run(user_input)
        print(result)
