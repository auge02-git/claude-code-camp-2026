from __future__ import annotations

import boukensha
from .errors import ApiError, LoopError
from .version import VERSION

HELP_TEXT = """\
Commands:
  /quiet   suppress logging output
  /loud    re-enable logging output
  /clear   wipe conversation history (tools stay)
  /exit    leave the REPL
  /quit    alias for /exit
  /help    show this message"""

BUILTIN_COMMANDS = frozenset({"/quiet", "/loud", "/clear", "/help", "/exit", "/quit"})


class Repl:
    PROMPT = "boukensha> "

    def __init__(
        self,
        *,
        agent,
        context,
        logger,
        config_dir=None,
        provider: str | None = None,
        model: str | None = None,
    ) -> None:
        self._agent = agent
        self._context = context
        self._logger = logger
        self._config_dir = config_dir
        self._provider = provider
        self._model = model
        self._turn = 0

    def run(self) -> None:
        print(self._banner())
        while True:
            try:
                line = input(self.PROMPT).strip()
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

    def _banner(self) -> str:
        ver = VERSION
        pad = " " * (9 - len(ver))
        return (
            f"\n"
            f"╔══════════════════════════════════════╗\n"
            f"║  BOUKENSHA MUD Assistant (v{ver}){pad}║\n"
            f"╚══════════════════════════════════════╝\n"
            f"  config:        {self._config_dir or '(default)'}\n"
            f"  provider:      {self._provider or '(default)'}\n"
            f"  model:         {self._model or '(default)'}\n"
            f"\n"
            f"  /quiet or /loud   toggle logging\n"
            f"  /clear            reset conversation history\n"
            f"  /exit or /quit    leave the REPL\n"
        )

    def _handle_command(self, cmd: str) -> None:
        if cmd == "/quiet":
            boukensha.set_quiet(True)
            print("(logging suppressed — type /loud to re-enable)")
        elif cmd == "/loud":
            boukensha.set_quiet(False)
            print("(logging enabled)")
        elif cmd == "/clear":
            self._context.clear_messages()
            self._turn = 0
            print("(conversation history cleared)")
        elif cmd == "/help":
            print(HELP_TEXT)
        elif cmd in ("/exit", "/quit"):
            print("Goodbye.")

    def _run_turn(self, user_input: str) -> None:
        self._turn += 1
        self._logger.turn(self._turn)
        self._agent._iteration = 0
        try:
            result = self._agent.run(user_input)
            print()
            print(result)
        except LoopError as exc:
            print(f"\n[error] {exc}")
        except ApiError as exc:
            print(f"\n[error] API call failed: {exc}")
