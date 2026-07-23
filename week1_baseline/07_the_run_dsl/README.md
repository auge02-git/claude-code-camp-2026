# 07 · Run DSL (Python-Port)

Schritt 7 kapselt die bisher manuelle Verdrahtung hinter einer einzigen API:
`boukensha.run(...)`.

## Ziel

Statt `Context`, `Registry`, Backend, `PromptBuilder`, `Client`, `Logger` und `Agent`
bei jedem Aufruf selbst zu bauen, beschreibt der Aufrufer nur noch:

- die Aufgabe (`task`)
- optionale Overrides (`system`, `model`, `backend`, `max_output_tokens`)
- ein kleines `setup(dsl)` fuer Tools

## Neue Bausteine

- `boukensha/run_dsl.py`
- top-level `boukensha.run(...)`
- Logger-Erweiterungen:
  - `turn(n)`
  - `subscribe(callback)`

## Python-DSL statt Ruby-Block

Ruby nutzt `instance_eval`. In Python wird die DSL explizit ueber ein Setup-Callable genutzt:

```python
import boukensha


def setup(t):
    @t.tool(
        "read_file",
        description="Read a file",
        parameters={"path": {"type": "string", "description": "File path"}},
    )
    def read_file(path: str) -> str:
        return open(path, encoding="utf-8").read()


result = boukensha.run(
    task="Read README.md and summarise it.",
    setup=setup,
)
```

`RunDSL` exponiert absichtlich nur `tool(...)`.

## Was `boukensha.run(...)` macht

- laedt `Config`
- liest Defaults aus `tasks.player`
- erstellt `Context`, `Registry`, Backend, `PromptBuilder`, `Client`, `Logger`, `Agent`
- fuehrt optional `setup(dsl)` aus
- startet den Agent
- schliesst den Logger sicher wieder

## Logger in Schritt 7

Die Log-Ausgabe bleibt `log_viz`-kompatibel.
Neu hinzugekommen:

- `turn`-Event
- Subscriber-Callbacks via `Logger.subscribe(...)`

Subscriber erhalten das **urspruengliche Event ohne Log-Enveloping**, also ohne `ts` und `session`.

## Setup

```zsh
cd week1_baseline/python/07_the_run_dsl
uv sync
```

## Tests

```zsh
cd week1_baseline
uv run python -m unittest discover -s python/07_the_run_dsl/tests -v
```

## Schritt ausfuehren

```zsh
cd week1_baseline/python/07_the_run_dsl
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

## Relevante Dateien

- `python/07_the_run_dsl/boukensha/run_dsl.py`
- `python/07_the_run_dsl/boukensha/__init__.py`
- `python/07_the_run_dsl/boukensha/logger.py`
- `python/07_the_run_dsl/boukensha/cli.py`
- `python/07_the_run_dsl/tests/test_run_api.py`
- `python/07_the_run_dsl/tests/test_logger_subscribe.py`
- `python/07_the_run_dsl/tests/test_run_step7.py`
