# Boukensha (冒険者)

Autonomer **Spieler-Agent** für den tbaMUD (Midgaard) — Python-Baseline der
„Claude Code Camp"-Architektur. Boukensha beobachtet die MUD-Ausgabe, wählt über
ein LLM (Claude) ein Werkzeug, führt es über den `MudManager` aus und reflektiert
das Ergebnis (Agentic Loop).

> **Leitplanken:** additive Python-Erweiterung. Die bestehenden Ruby-Dateien
> (`mud_manager/`) und das Repo-Verzeichnis `.boukensha/` bleiben **unverändert**.
> Die Telnet-Session wird aus `mud-mcp/mud_mcp/session.py` **wiederverwendet**
> (importiert, nicht kopiert/geändert).

## Architektur (aus dem Diagramm)

```
Your Prompt → Observe → Take Action → Reflect → (Observe) / → Output
                            │
                            └── Tool Use → MudManager → tbaMUD (telnet :4000)
```

| Modul | Diagramm-Knoten | Aufgabe |
|-------|-----------------|---------|
| `boukensha/agent.py`   | `agent.rb`   | Agentic Loop (Anthropic-Tool-Use) |
| `boukensha/config.py`  | `config.rb`  | `~/.boukensha/settings.yml` + `prompts/system.md` |
| `boukensha/logger.py`  | —            | JSONL-Sitzungslogs |
| `boukensha/context.py` | —            | Nachrichten-/Zustandskontext |
| `boukensha/registry.py`| —            | Werkzeug-Registry (Anthropic-Schemas) |
| `boukensha/mud.py`     | `MudManager` | dünner Wrapper um `mud_mcp.session` |
| `boukensha/tools/`     | `Tool Use`   | MUD-Werkzeuge (look/move/kill/flee/…) |
| `boukensha/backends/`  | —            | Claude-Backend |
| `boukensha/cli.py` `repl.py` `run_dsl.py` | `tui.rb` / `> bounkensha` | Text-UI |
| `log_viz/server.py`    | `log_viz`    | FastAPI-Viewer für die JSONL-Logs |

## Modell

Laut Vorgaben: **primär Haiku 4.5** (`claude-haiku-4-5-20251001`), Alternative
**Sonnet 4.6** (`claude-sonnet-4-6`). Bewusst **nicht** das Default-/neueste Modell.
Konfigurierbar in `~/.boukensha/settings.yml` (`model:`).

## Authentifizierung

Das Backend nutzt den offiziellen `anthropic`-Client. Der **argumentlose**
`anthropic.Anthropic()` löst Zugangsdaten in fester Reihenfolge auf (erste
Übereinstimmung gewinnt):

`ANTHROPIC_API_KEY` → `ANTHROPIC_AUTH_TOKEN` → OAuth-Profil aus `ant auth login`
→ Workload-Identity → Default-Profil auf der Platte.

Drei Wege, den Agenten zu authentifizieren:

| Weg | Wie | Wann |
|-----|-----|------|
| **API-Key** | `export ANTHROPIC_API_KEY=sk-ant-…` | Standard, Abrechnung über die Anthropic Console. |
| **OAuth / claude.ai-Konto** | `ant auth login` (Anthropic CLI) legt ein Profil an, das der `anthropic`-Client automatisch liest — **kein** Env-Var nötig. Alternativ ein `ANTHROPIC_AUTH_TOKEN` setzen. | Nutzung über ein Konto/Abo statt eines statischen API-Keys. |
| **Explizites Token im Code** | `settings.yml: auth_token: <token>` **oder** `export BOUKENSHA_AUTH_TOKEN=<token>` | Wenn das Token nicht über die SDK-Auto-Auflösung kommen soll. |

Der explizite Weg wird an `anthropic.Anthropic(auth_token=…)` durchgereicht
(`config.py:Config.auth_token` → `backends/anthropic.py`). Ist nichts gesetzt,
greift die Auto-Auflösung oben — der Agent läuft also auch mit einem reinen
`ant auth login`-Profil ohne weitere Konfiguration.

> Hinweis: `ant` ist die Anthropic-CLI (`brew install anthropics/tap/ant`).
> Ein per Claude Code erzeugtes OAuth-Token (`claude setup-token`) lässt sich
> als `ANTHROPIC_AUTH_TOKEN` bzw. `BOUKENSHA_AUTH_TOKEN` setzen.
>
> ⚠️ **Wichtig zur Abrechnung:** Ein `ant auth login`-OAuth-Profil authentifiziert
> gegen die **Console-Organisation** und bucht auf deren **API-Guthaben** — **nicht**
> auf ein claude.ai-**Abo** (Pro/Max). Hat die Org kein Guthaben, antwortet die API
> mit `400 – "credit balance is too low"`. Der Agent stürzt dann **nicht** ab, sondern
> meldet das klar (siehe `agent.py:_fehlermeldung`). Für einen produktiven Lauf
> entweder Guthaben in der Console einrichten oder einen `ANTHROPIC_API_KEY` mit
> Guthaben verwenden.

## Inbetriebnahme

```sh
cd week0_explore/boukensha
uv sync                          # Abhängigkeiten (inkl. mud-mcp als Pfad-Dep)
export ANTHROPIC_API_KEY=sk-...  # für den LLM-Aufruf nötig

# 1) Verdrahtungs-Smoke-Test (ohne MUD, ohne LLM):
uv run boukensha --help

# 2) Live gegen den MUD (Server muss laufen: infrastructure/ up auf :4000):
uv run boukensha                 # verbindet + loggt via credentials.json ein → REPL
uv run boukensha --no-connect    # startet ohne MUD-Verbindung
uv run boukensha --dsl plan.txt  # skriptbaren Ablauf ausführen
```

Voraussetzungen für den Live-Betrieb:
- MUD-Server läuft (`cd ../infrastructure && docker compose up -d`), Port 4000.
- Charakter `dummy` existiert (Zugangsdaten in `../mud-mcp/credentials.json`).
- `ANTHROPIC_API_KEY` gesetzt.

## Agent-Home `~/.boukensha`

- `settings.yml` — Modell + MUD-Host/Port.
- `prompts/system.md` — deutscher System-Prompt (Sicherheitsregeln, Weltwissen).
- `logs/<session_id>/<datum>.jsonl` — Sitzungslogs (siehe `log_viz`).

Überschreibbar via Umgebungsvariable `BOUKENSHA_DIR`.

## Logs ansehen

```sh
uv sync --extra logviz
uv run uvicorn log_viz.server:app --reload   # http://127.0.0.1:8000
```
