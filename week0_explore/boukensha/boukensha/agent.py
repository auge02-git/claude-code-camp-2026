"""Agentic Loop (Diagramm-Knoten ``agent.rb``).

Setzt die Schleife aus dem Architektur-JSON um:

    Your Prompt → Observe → Take Action → Reflect → (zurück zu Observe) / → Output
    Take Action ⇄ Tool Use → MudManager

Konkret als Anthropic-Tool-Use-Schleife:
- **Observe:** aktuelle MUD-Ausgabe als Beobachtung in den Kontext.
- **Take Action:** Modell wählt ein Werkzeug (``tool_use``).
- **Tool Use:** Werkzeug wird über die Registry ausgeführt (→ MudManager); das
  Ergebnis fließt als ``tool_result`` zurück (Kante „Tool Use → Take Action").
- **Reflect/Output:** endet das Modell ohne Werkzeugaufruf, ist das die Ausgabe.
"""

from __future__ import annotations

from .backends import ClaudeBackend
from .config import Config
from .context import Context
from .logger import SessionLogger
from .mud import MudManager
from .registry import ToolRegistry
from .tools import build_default_tools


class Agent:
    """Verdrahtet Kontext, Registry, Backend und MudManager zur Agentic Loop."""

    def __init__(
        self,
        config: Config,
        mud: MudManager,
        backend: ClaudeBackend | None = None,
        logger: SessionLogger | None = None,
        max_steps: int = 12,
    ) -> None:
        self.config = config
        self.mud = mud
        self.backend = backend or ClaudeBackend(model=config.model)
        self.logger = logger or SessionLogger()
        self.context = Context(system_prompt=config.system_prompt)
        self.registry = ToolRegistry()
        for tool in build_default_tools():
            self.registry.register(tool)
        self.max_steps = max_steps

    def observe(self) -> str:
        """Liest die aktuelle MUD-Ausgabe (Kante „→ Observe")."""
        beobachtung = self.mud.read()
        self.context.letzte_beobachtung = beobachtung
        self.logger.log("observe", text=beobachtung)
        return beobachtung

    def step(self, prompt: str) -> str:
        """Ein „Your Prompt → … → Output"-Durchlauf.

        Führt die Tool-Use-Schleife aus, bis das Modell ohne Werkzeugaufruf
        antwortet (Reflect → Output) oder ``max_steps`` erreicht ist.
        """
        self.context.add_user(prompt)
        self.logger.log("prompt", text=prompt)
        tools = self.registry.anthropic_schemas()

        for _ in range(self.max_steps):
            try:
                antwort = self.backend.complete(
                    system=self.context.system_prompt,
                    messages=self.context.messages,
                    tools=tools,
                )
            except Exception as fehler:
                # Kein harter Absturz mehr: API-/Auth-/Billing-Fehler sauber melden.
                text = _fehlermeldung(fehler)
                self.logger.log(
                    "error", fehler=type(fehler).__name__, text=str(fehler)[:500]
                )
                self.logger.log("output", text=text)
                return text
            self._log_usage(antwort)
            self.context.add_assistant(antwort.content)

            if getattr(antwort, "stop_reason", None) != "tool_use":
                text = _text_of(antwort)
                self.logger.log("output", text=text)
                return text

            # Take Action → Tool Use: alle angeforderten Werkzeuge ausführen.
            tool_results = []
            for block in antwort.content:
                if getattr(block, "type", None) != "tool_use":
                    continue
                tool = self.registry.get(block.name)
                self.logger.log("action", tool=block.name, input=dict(block.input))
                if tool is None:
                    ergebnis = f"Unbekanntes Werkzeug: {block.name}"
                else:
                    ergebnis = tool.run(self.mud, **dict(block.input))
                self.logger.log("tool", tool=block.name, result=ergebnis)
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": ergebnis}
                )
            # Ergebnis zurück in die Aktion (Kante „Tool Use → Take Action").
            self.context.add_user(tool_results)

        self.logger.log("output", text="(max_steps erreicht)")
        return "(Abbruch: max_steps erreicht)"

    def _log_usage(self, antwort) -> None:
        """Protokolliert Token-Nutzung inkl. Cache-Treffer (Prompt-Caching)."""
        usage = getattr(antwort, "usage", None)
        if usage is None:
            return
        self.logger.log(
            "usage",
            input=getattr(usage, "input_tokens", None),
            output=getattr(usage, "output_tokens", None),
            cache_write=getattr(usage, "cache_creation_input_tokens", None),
            cache_read=getattr(usage, "cache_read_input_tokens", None),
        )


def _text_of(antwort) -> str:
    """Sammelt die Textblöcke einer Antwort."""
    teile = [b.text for b in antwort.content if getattr(b, "type", None) == "text"]
    return "\n".join(teile).strip()


def _fehlermeldung(fehler: Exception) -> str:
    """Übersetzt einen Backend-/API-Fehler in einen klaren deutschen Hinweis.

    Fängt insbesondere die häufigsten Auth-/Abrechnungsfälle ab, damit der Agent
    nicht mit einem rohen Traceback abstürzt.
    """
    text = str(fehler)
    low = text.lower()
    status = getattr(fehler, "status_code", None)

    if "credit balance is too low" in low or "plans & billing" in low:
        return (
            "❌ Abbruch: Das verwendete Konto hat kein API-Guthaben.\n"
            "   Console-Organisation — NICHT auf ein claude.ai-Abo (Pro/Max). Optionen:\n"
            "   • In der Anthropic Console Guthaben/Billing für diese Org einrichten, oder\n"
            "   • einen API-Key mit Guthaben setzen: `export ANTHROPIC_API_KEY=sk-ant-…`\n"
            f"   (API-Meldung: {text[:160]})"
        )
    if status in (401, 403) or "authentication_error" in low or "permission" in low:
        return (
            "❌ Abbruch: Authentifizierung fehlgeschlagen.\n"
            "   Prüfe den `ANTHROPIC_API_KEY` (mit Guthaben) in der Umgebung.\n"
            f"   (API-Meldung: {text[:160]})"
        )
    if status == 429 or "rate_limit" in low or "overloaded" in low:
        return (
            "❌ Abbruch: Rate-Limit/Überlastung. Später erneut versuchen.\n"
            f"   (API-Meldung: {text[:160]})"
        )
    return f"❌ Abbruch: Modellaufruf fehlgeschlagen ({type(fehler).__name__}): {text[:200]}"
