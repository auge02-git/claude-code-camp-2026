# Boukensha-Agent — Architektur-Blaupause (Python-Baseline)

Quelle der Wahrheit: **`docs/plans/Claude Code Camp Agent Architecture - Baseline.json`**
(Lucidchart-Export). Diese Datei setzt die im Diagramm gezeigte Architektur als **neue,
additive Python-Erweiterung** um — Baseline: Implementierung in **Python** (uv),
Dokumentation/Kommentare/TUI-Texte auf **Deutsch**. Eigennamen (`Boukensha`, `MudManager`)
und Python-idiomatische (englische) Bezeichner bleiben erhalten.

> Boukensha (冒険者) = „Abenteurer" — der Agent, der den MUD selbstständig spielt.

## Leitplanken (zwingend)
- **`.boukensha/` wird NICHT angefasst** — komplett unverändert.
- **Bestehende `.rb`-Dateien werden NICHT nach Python übersetzt** und NICHT verändert
  (insb. das Ruby-Gem `week0_explore/mud_manager/`). Sie bleiben so wie sie sind.
- Python-Code entsteht **nur als zusätzliche, neue Erweiterung** (die im Diagramm
  gezeigten `agent.rb`/`repl.rb`/`tui.rb` … existieren noch nicht als Dateien → sie
  werden als **neue** Python-Module angelegt, nicht als Übersetzung).
- Vorhandener **Python**-Code (`mud-mcp/mud_mcp/session.py`) wird **wiederverwendet,
  nicht verändert**.
- Neuer Code liegt in **`week0_explore/boukensha/`** (nicht in `.boukensha/`).

## Knoten → Python-Modul (aus dem JSON)

| Baseline-Knoten (Ruby) | Python-Modul | Zweck |
|---|---|---|
| `> bounkensha` (CLI) | `boukensha.cli:main` (pyproject `[project.scripts]`) | Einstiegsbefehl |
| `tui.rb` | `boukensha/cli.py` | Text-UI (rich), deutschsprachig |
| `repl.rb` | `boukensha/repl.py` | interaktive Schleife |
| `run_dsl.rb` | `boukensha/run_dsl.py` | skriptbare „Journeys" |
| `Bounkensha.run()` | `boukensha/__init__.py:run` + `boukensha/app.py` | Bootstrap/Verdrahtung |
| `config.rb` | `boukensha/config.py` | settings.yml + BOUKENSHA_DIR/PATH + Credentials |
| `logger.rb` | `boukensha/logger.py` | JSONL nach `logs/<session_id>/<datum>.jsonl` |
| `agent.rb` | `boukensha/agent.py` | Agentic Loop |
| `Bounkensha.Context` | `boukensha/context.py` | Gedächtnis/Spielzustand |
| `registry.rb` | `boukensha/registry.py` | Werkzeug-Registry |
| `tool.rb` / „Tool Use" | `boukensha/tools/` | Werkzeuge (Basisklasse + MUD-Werkzeuge) |
| `backends/` | `boukensha/backends/` | LLM-Anbindung (Claude API) |
| `MudManager` | `boukensha/mud.py` | **wiederverwendet** `mud_mcp.session.MudSession` (Telnet) |
| `log_viz` (sinatra) | `log_viz/server.py` (FastAPI, Python-Baseline) | JSONL-Logs menschenlesbar |
| `~/.boukensha` | Laufzeit-Home (creds, settings.yml, prompts/system.md, logs/) | Agent-Home |
| `preview` | `week0_explore/preview/web` (existiert) | Weltdaten-Viewer |
| Docker / infrastructure/lib | `week0_explore/infrastructure` (existiert) | MUD-Server + Weltseed |

## Datenfluss (exakte Kanten aus dem JSON)

```
> bounkensha → tui.py → repl.py → agent.py
                                     │
                 ┌───────────────────┴─────────── Agentic Loop ───────────────────┐
                 │  Your Prompt → Observe → Take Action → Reflect →(zurück)→ Observe │
                 │                              │            └────────→ Output        │
                 │                       Tool Use ⇄ Take Action                        │
                 │            (Context, registry, backends stützen die Schleife)       │
                 └──────────────────────────────┬──────────────────────────────────┘
                                          Tool Use / Agent
                                                 │
                                            MudManager  ──telnet localhost 4000──▶ Docker (circlemud)
config.py ─┐
logger.py ─┼─▶ ~/.boukensha ──▶ log_viz
run_dsl.py ─▶ Bounkensha.run()
```

Kern-Invarianten aus den JSON-Kanten:
- **Rückkopplung** `Reflect → Observe` (Schleife) **und** `Reflect → Output` (Abschluss).
- `Take Action → Tool Use → MudManager` und `Tool Use → Take Action` (Werkzeug-Ergebnis
  fließt zurück in die Aktion).
- Sowohl der **Agent** als auch **Tool Use** sprechen den **MudManager** an.
- `config.py` **und** `logger.py` schreiben/lesen unter `~/.boukensha`.

## Wiederverwendung (nicht neu bauen, nichts verändern)
- **MudManager = `mud_mcp.session.MudSession`** (vorhandener Python-Code inkl. IAC-Stripping,
  Login-Dance, `credentials.json`). `boukensha/mud.py` ist nur ein **dünner Wrapper**, der
  diese Klasse **importiert** — die Datei `session.py` selbst wird **nicht** verändert.
- Das Ruby-Gem `mud_manager/` bleibt **unverändert** und wird **nicht** ersetzt/übersetzt
  (es kann eigenständig weiter genutzt werden). Der Python-Agent ist eine **parallele,
  additive** Variante.
- `preview/web` und `infrastructure/` bleiben unverändert.

## Baseline-Regeln (nur für NEUEN Code)
- Neue Module in **Python** (uv); `log_viz` als **FastAPI** (neu, kein Ruby-Ersatz).
- Deutsche Docstrings/Kommentare/TUI. **LLM-Default: Claude Haiku 4.5**
  (`claude-haiku-4-5-20251001`) in `settings.yml` — nicht das „neueste/Default"-Modell.
  **Alternative: Sonnet 4.6** (in `settings.yml` umschaltbar). Exakte Modell-ID vor der
  Verdrahtung bestätigen (mir bekannt sind Haiku 4.5, Sonnet 5, Opus 4.8).
- Keine Änderung an bestehenden `.rb`-Dateien und an `.boukensha/`.
