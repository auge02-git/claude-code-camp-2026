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

Das Backend nutzt den offiziellen `anthropic`-Client mit dem **API-Key** aus der
Umgebung:

```sh
export ANTHROPIC_API_KEY=sk-ant-…
```

> ⚠️ **Hinweis:** Der `anthropic`-Client löst Credentials selbst auf (u. a. ein
> `ant auth login`-OAuth-Profil, falls vorhanden). Ein solches Profil bucht aber
> auf das **API-Guthaben der Console-Org** — **nicht** auf ein claude.ai-**Abo**
> (Pro/Max). Ohne Guthaben antwortet die API mit `400 – "credit balance is too low"`.
> Der Agent stürzt dabei **nicht** ab, sondern meldet es klar
> (`agent.py:_fehlermeldung`). Für einen produktiven Lauf einen `ANTHROPIC_API_KEY`
> mit Guthaben verwenden.

### Optional: lokaler LLM-Server

Wenn ein **Anthropic-kompatibler** lokaler Endpoint verfügbar ist (z. B.
`http://127.0.0.1:1234`), kann Boukensha wahlweise dagegen laufen.
Das Modell wird dabei ohne Override automatisch auf **`qwen/qwen-3-5-9b`** gesetzt
(Default für `--local-llm`). Du kannst aber jedes lokale Modell explizit setzen,
z. B. **`google/gemma-4-12b-qat`**.

```sh
# Variante A: pro Aufruf
uv run boukensha --local-llm --no-connect

# Variante A2: lokales Modell explizit setzen
uv run boukensha --local-llm --model google/gemma-4-12b-qat --no-connect

# Variante A3: Gateway mit eigenem API-Key (z. B. LiteLLM Virtual Key)
uv run boukensha --local-llm --api-key sk-my-gateway-key --no-connect

# Variante B: dauerhaft über Umgebung
export BOUKENSHA_LLM_BASE_URL=http://127.0.0.1:1234
export BOUKENSHA_LLM_MODEL=qwen/qwen-3-5-9b
export BOUKENSHA_API_KEY=sk-my-gateway-key
uv run boukensha --no-connect

# Variante C: globaler Modell-Override (auch ohne --local-llm)
export ANTHROPIC_LLM_MODEL=google/gemma-4-12b-qat
uv run boukensha --no-connect
```

Hinweise:
- Das Backend setzt bei fehlendem `ANTHROPIC_API_KEY` automatisch einen Dummy-Key (`local-dev-key`).
- Mit `--local-llm` werden Endpoint + lokales Default-Modell gesetzt; `--model` überschreibt das Modell.
- `--api-key` / `BOUKENSHA_API_KEY` setzt einen expliziten Key, der Vorrang vor `ANTHROPIC_API_KEY` und dem Dummy-Key hat. Der Key wird beim Start maskiert angezeigt (`sk-xx****`).
- `ANTHROPIC_LLM_MODEL` überschreibt das Modell global (falls `--model` nicht gesetzt ist).

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

Überschreibbar via Umgebungsvariable `BOUKENSHA_DIR`.

## Logs ansehen

```sh
uv sync --extra logviz
uv run uvicorn log_viz.server:app --reload   # http://127.0.0.1:8000
```
