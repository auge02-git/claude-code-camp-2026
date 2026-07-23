# 06 · The Logger (Python-Port)

In Schritt 6 wird die Agent-Ausfuehrung strukturiert geloggt.
**Abweichung zu Ruby/Python-Referenz:** Das Log-Format ist explizit auf
`week1_baseline/log_viz/server.py` abgestimmt.

## Ziel

- Jeder wichtige Agent-Schritt erzeugt ein JSONL-Event.
- Die Events sind direkt in `log_viz` lesbar.
- Der Agent bleibt funktionsgleich zu Schritt 5 (Tool-Loop), aber mit observability.

## log_viz-kompatibles Format

`log_viz/server.py` erwartet JSONL-Zeilen mit mindestens:

- `ts`
- `session`
- `typ`

Deshalb schreibt `Logger` Events im Format:

```json
{"ts":"...","session":"...","typ":"iteration","n":1,"max":25}
```

## Ablageort

Logs liegen unter:

```text
~/.boukensha/logs/<session_id>/events.jsonl
```

bzw. bei gesetztem `BOUKENSHA_DIR`:

```text
$BOUKENSHA_DIR/logs/<session_id>/events.jsonl
```

## Logger-Events

- `session_start`
- `iteration`
- `prompt`
- `raw`
- `tool_call`
- `tool_result`
- `limit_reached`
- `response`
- `turn_end`

## Integration in den Agent

`Agent` nutzt `Logger` fuer:

- Iterations-/Prompt-Tracking
- Tool-Aufruf + Tool-Ergebnis (inkl. Fehlerfall)
- Response + Turn-Ende
- Wind-down bei Iterationslimit

Bei Tool-Fehlern bricht die Schleife nicht hart ab; stattdessen wird ein Fehler-Resultat
als `tool_result` geloggt und in den Kontext geschrieben.

## Setup

```zsh
cd week1_baseline/python/06_the_logger
uv sync
```

## Tests

```zsh
cd week1_baseline
uv run python -m unittest discover -s python/06_the_logger/tests -v
```

## Schritt ausfuehren

```zsh
cd week1_baseline/python/06_the_logger
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

Danach optional `log_viz` starten:

```zsh
cd week1_baseline
uvicorn log_viz.server:app --reload
```

## Relevante Dateien

- `python/06_the_logger/boukensha/logger.py`
- `python/06_the_logger/boukensha/agent.py`
- `python/06_the_logger/boukensha/cli.py`
- `python/06_the_logger/tests/test_logger.py`
- `python/06_the_logger/tests/test_agent_logger.py`
- `python/06_the_logger/tests/test_run_step6.py`
