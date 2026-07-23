# 01 · Struct Skeleton (Python-Port)

Python-3-Port von [`ruby/01_struct_skeleton`](../../ruby/01_struct_skeleton/README.md). Definiert
die drei Kernstrukturen fuer die Agent-Task-Verwaltung — die Datencontainer, mit denen Nachrichten,
Werkzeuge und Kontext durch das System fliessen.

Ziel:
- `boukensha.tool.Tool` — Werkzeug, das ein Agent aufrufen kann
- `boukensha.message.Message` — Gesprächseinheit
- `boukensha.context.Context` — Zentraler Container fuer API-Call-Daten

Ruby nutzt leichte `Struct`s. Python's Entsprechung ist `@dataclass` fuer `Tool` und `Message`.
`Context` hat Verhalten (mutable Sammlungen, Methoden), bleibt also eine regulaere Klasse.

## Datenstrukturen

### `Tool`
Ein Werkzeug, das der Agent aufrufen kann.

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `name` | str | Name der Aktion (z.B. "move", "attack") |
| `description` | str | Agent-verständliche Beschreibung |
| `parameters` | dict | JSON-Schema Format für Parameter |
| `block` | callable | Ausführbarer Code beim Tool-Aufruf |

### `Message`
Eine Nachricht in der Konversation zwischen User und Agent.

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `role` | str | "user", "assistant", oder "tool_result" |
| `content` | str | Gesprächstext |
| `tool_use_id` | str | (optional) Verknüpfung zu Tool-Aufruf |

### `Context`
Zentraler Container für alle API-Call-Daten.

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `task` | type | Task-Klasse (z.B. Player) |
| `system` | str | System-Prompt für Agent |
| `messages` | list[Message] | Gesprächshistorie |
| `tools` | dict[str, Tool] | Registrierte Tools |

## Code-Struktur

| Datei | Zweck |
|------|---------|
| `boukensha/config.py` | `Config`-Klasse (kopiert von Schritt 00, ohne `PROMPTS_DIR`) |
| `boukensha/tasks/base.py` | Abstrakte `Base`-Task-Klasse (unverändert von Schritt 00) |
| `boukensha/tasks/player.py` | Konkrete `Player`-Task-Klasse (unverändert von Schritt 00) |
| `boukensha/tool.py` | `Tool` @dataclass — Port von `lib/boukensha/tool.rb` |
| `boukensha/message.py` | `Message` @dataclass — Port von `lib/boukensha/message.rb` |
| `boukensha/context.py` | `Context` Klasse — Port von `lib/boukensha/context.rb` |
| `boukensha/cli.py` | CLI-Funktionen `run_step0()` und `run_step1()` |
| `boukensha/__main__.py` | Modul-Entry-Point |
| `boukensha/__init__.py` | Paket-Exports |
| `tests/test_struct_skeleton.py` | Unit-Tests fuer alle Strukturen |
| `pyproject.toml` | Projektmetadaten und Abhaengigkeiten |

Keine `prompts/`-Verzeichnis in diesem Schritt — siehe "Unterschiede zu Schritt 0" weiter unten.

## Unterschiede zu Schritt 0

- **`Config.PROMPTS_DIR` entfernt** — Ruby laesst die Konstante in diesem Schritt weg
  und liefert kein `prompts/system.md`. Das Python-Port macht dasselbe.
- **`tasks/base.py` und `tasks/player.py` unverändert** — byte-identisch zu Schritt 00
- **`Context` hat kein `token_budget`-Feld** — trotz Dokumentation nicht implementiert
  (doc/code-Drift im Ruby-Original)

## Python-spezifische Anpassungen

Uebernimmt alle Konventionen aus Schritt 00:
- Symbol/String-Dual-Key-Lookups fallen auf String-Keys zusammen
- `Path`-basierte Pfade statt Strings
- `task_name()` als @classmethod
- Vollstaendige Type-Hints
- Keine `abc.ABC`

Neu in diesem Schritt:

- **`Tool` und `Message` → `@dataclass`** (veraenderbar, nicht gefroren — wie Ruby Struct)
  - `Tool.__repr__`: Beschreibung gekuerzt auf 41 Zeichen
  - `Message.__repr__`: Inhalt gekuerzt auf 61 Zeichen, plus `[tool_use_id]` wenn gesetzt
- **`Tool.block`** ist `Callable[..., Any]` — wird nicht aufgerufen, kommt in Schritt 02
- **`Context`** bleibt regulaere Klasse mit `messages` und `tools` als mutable Sammlungen
- **`role` ist plain str** — `"user"`, `"assistant"`, `"tool_result"`


## Shared venv, kein Per-Schritt-Install

Wie in Schritt 00: Jeder Python-Schritt hat sein eigenes `boukensha`-Paket.
Nur einer kann je venv installiert sein — daher nutzen wir `uv run` statt `pip install`.
Jeder Schritt laedt seinen eigenen Code via `sys.path`-Einfuegung.

## Setup

```zsh
cd week1_baseline/python/01_struct_skeleton
uv sync
```

## Ausfuehrung

Schritt 1 (Struct Skeleton) ausfuehren:

```zsh
cd week1_baseline/python/01_struct_skeleton
uv run python -m boukensha
```

Oder direkt als Funktion:

```zsh
uv run python -c "from boukensha.cli import run_step1; raise SystemExit(run_step1())"
```

Um zuerst die Konfiguration (Schritt 0) anzusehen:

```zsh
uv run python -c "from boukensha.cli import run_step0; raise SystemExit(run_step0())"
```

## Tests ausfuehren

```zsh
uv run python -m unittest tests/test_struct_skeleton.py -v
```

Erwartet 11 Tests:
- Tool-Erstellung und Eigenschaften
- Message-Erstellung mit/ohne tool_use_id
- Text-Kuerzung in __repr__
- Context-Initialisierung
- Tool-Registrierung
- Message-Hinzufuegen
- Context __repr__

## Erwartete Ausgabe

```
=== Boukensha Schritt 1: Struct Skeleton ===

Config:   #<Boukensha.Config dir=/Users/.../.../.boukensha tasks=player>
Context:  #<Context task=player turns=2 tools=1>
Tool:     #<Tool name=move description=Move the player in a direction (north, so params=['direction']>
Messages:
  #<Message role=user content=Explore north and tell me what you find....>
  #<Message role=assistant content=Sure, let me head north and take a look....>
```
