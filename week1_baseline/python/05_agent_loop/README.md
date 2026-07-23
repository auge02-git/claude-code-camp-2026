# 05 · Agent Loop (Python-Port)

Python-3-Port von `ruby/05_agent_loop`: In diesem Schritt bekommt Boukensha die erste
vollstaendige agentische Schleife.

## Ziel von Schritt 05

`Agent` verbindet jetzt:

- `PromptBuilder` (Payload bauen)
- `Client` (API-Call)
- `Registry` (Tool-Dispatch)
- `Context` (Nachrichtenhistorie)

Der Agent kann mehrfach mit dem Modell interagieren, Tool-Calls ausfuehren und danach
mit den Tool-Ergebnissen weiterdenken.

## Neue Komponenten

- `boukensha/agent.py`
- `LoopError` in `boukensha/errors.py` (wie Ruby vorhanden)
- Erweiterungen in:
  - `prompt_builder.py` (`parse_response`, `tools`-Override)
  - `client.py` (`tools`-Override in `call`)
  - `tasks/base.py` (`max_iterations`, `max_output_tokens`)
  - Backends (`parse_response`, assistant-content Rekonstruktion)

## Agent-Ablauf

`Agent.run(user_input)`:

1. User-Nachricht in `Context` schreiben
2. API aufrufen
3. Antwort normalisieren (`parse_response`)
4. Bei `tool_use`:
   - Assistant-Block in Context speichern
   - Tools dispatchen
   - Tool-Ergebnisse als `tool_result` speichern
   - naechste Iteration
5. Bei `end_turn`: Text extrahieren und zurueckgeben

### Iterationslimit und Wind-Down

- `max_iterations` wird aus Task-Settings gelesen (Default: `25`)
- Wenn Limit erreicht ist:
  - ein finaler Wrap-Up-Call mit `tools: []`
  - kurze Abschlussantwort statt abruptem Abbruch
  - Fallback-Text bei API-Fehler

## Setup

```zsh
cd week1_baseline/python/05_agent_loop
uv sync
```

## Tests

```zsh
cd week1_baseline
uv run python -m unittest discover -s python/05_agent_loop/tests -v
```

Enthaelt:

- `tests/test_agent.py` (Tool-Flow, Wrap-Up, Fallback)
- `tests/test_tasks.py` (Task-Settings Resolver)
- `tests/test_run_step5.py` (CLI-Smoke-Test mit gemocktem Agent)

## Ausfuehrung

```zsh
cd week1_baseline/python/05_agent_loop
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

## Provider-Hinweis

- `lmstudio` funktioniert lokal ohne API-Key
- `anthropic`, `openai`, `gemini`, `ollama_cloud` benoetigen passende API-Keys
- `ollama` benoetigt lokalen Ollama-Server

## Relevante Dateien

- `python/05_agent_loop/boukensha/agent.py`
- `python/05_agent_loop/boukensha/client.py`
- `python/05_agent_loop/boukensha/prompt_builder.py`
- `python/05_agent_loop/boukensha/tasks/base.py`
- `python/05_agent_loop/boukensha/cli.py`
- `python/05_agent_loop/tests/test_agent.py`
