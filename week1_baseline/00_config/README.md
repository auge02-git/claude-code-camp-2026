# 00 · Konfiguration (Python-Port)

Python-3-Port von [`ruby/00_config`](../../ruby/00_config/README.md). Ziel ist eine moeglichst
nahe Entsprechung zur Ruby-Implementierung: gleiches `.boukensha/`-Vertragsmodell,
vergleichbares Schema, gleiche Aufgabenaufteilung.

Die Konfiguration wird zentral aus `.boukensha/settings.yml` (oder alternativ
`.boukensha/settings.yaml`) geladen und ueber `boukensha.config.Config` bereitgestellt.
Konfigurierbare Werte kommen aus Dateien, nicht aus Hardcodierung im Code.

Die Konfiguration ist nach **Tasks** organisiert. In Woche 1 nutzen wir zunaechst nur den
Task `player`, spaetere Schritte koennen weitere Tasks und Modelle hinzufuegen.

## Design-Ueberlegungen

Wir bleiben nah an der Standard Library. Fuer diesen Schritt sind zwei Laufzeitabhaengigkeiten
sinnvoll:

- `python-dotenv` fuer das Laden von `.env`
- `PyYAML` fuer `settings.yml`/`settings.yaml`

Der Rest basiert auf Standardmodulen (`pathlib`, `os`).

## Code-Struktur

| Datei | Zweck |
|------|---------|
| `boukensha/config.py` | `Config`-Klasse (Port von `lib/boukensha/config.rb`) |
| `boukensha/tasks/base.py` | Abstrakte `Base`-Task-Klasse (provider/model + Prompt-Aufloesung) |
| `boukensha/tasks/player.py` | Konkrete `Player`-Task-Klasse |
| `boukensha/cli.py` | Direkter Step-00-Aufruf als Funktion `run_step0(...)` |
| `boukensha/__main__.py` | Modul-Entry-Point fuer `python -m boukensha` |
| `boukensha/__init__.py` | Paket-Exports fuer `Config`, `PROMPTS_DIR`, `Player` |
| `prompts/system.md` | Standard-Systemprompt im Projekt |
| `tests/test_config.py` | Kurze Tests fuer Konfiguration und Prompt-Aufloesung |
| `pyproject.toml` | Projektmetadaten und Abhaengigkeiten |

## Aufloesung des Konfigurationsordners

`Config` sucht den `.boukensha/`-Ordner in folgender Reihenfolge:

1. Uebergebener `directory`-Parameter (z. B. in Tests)
2. `BOUKENSHA_DIR` Umgebungsvariable
3. Naechster Projektordner mit `.boukensha/settings.yml` oder `.boukensha/settings.yaml`
   (ausgehend vom aktuellen Arbeitsverzeichnis)
4. `~/.boukensha` als Default

## Erwartete Struktur

```text
.boukensha/
  .env
  settings.yml
  prompts/
    <task>/
      system.md
```

Hinweis: `settings.yaml` wird ebenfalls gelesen, falls `settings.yml` nicht existiert.

## Tasks und Prompt-Aufloesung

`boukensha.tasks.base.Base` ist stateless und arbeitet ueber `@classmethod`s.
`Config.tasks("player")` liefert die Task-Settings, die dann z. B. an `Player.provider(...)`
oder `Player.system_prompt(...)` uebergeben werden.

Aufloesungsreihenfolge fuer System-Prompts:

1. `.boukensha/prompts/<task>/system.md` (wenn `prompt_override.system: true`)
2. `prompts/system.md` (Default im Projekt)

Zusaetzlich gibt es `Config.save_prompt(task, prompt_name, content)`, um eingegebene Prompts
in `.boukensha/prompts/<task>/<prompt_name>.md` zu speichern.

## Konfigurationsschema

```yaml
tasks:
  player:
    provider: anthropic
    model: claude-haiku-4-5
    prompt_override:
      system: true
mud:
  host: localhost
  port: 4000
  username: dummy
  password: helloworld
```

## Setup

```zsh
cd week1_baseline/python/00_config
uv sync
```

## Ausfuehren mit `uv run`

```zsh
cd week1_baseline/python/00_config
uv run python -m boukensha
```

Alternativ direkt als Funktion:

```zsh
cd week1_baseline/python/00_config
uv run python -c "from boukensha import run_step0; raise SystemExit(run_step0())"
```

Die Funktion `run_step0()` ist in `boukensha/cli.py` implementiert und wird vom Modul-Entry-Point
`boukensha/__main__.py` genutzt.

## Tests ausfuehren

```zsh
cd week1_baseline/python/00_config
uv run python -m unittest tests/test_config.py
```
