# Schritt 09 Plan - Globale Executable

## Ziel
BOUKENSHA als globalen `boukensha`-Befehl verpacken. Ein eigenstaendiger Loader (`boukensha_loader.py`) loest auf, welchen Schritt-Ordner er laedt, und startet dann die REPL.

## Checkliste

- [x] **Plan zuerst pflegen**
  - [x] `plan.md` angelegt

- [x] **Referenz analysieren**
  - [x] Python Schritt 09 README gelesen
  - [x] Unterschiede zu Schritt 08 festgehalten (cwd-Suche, HTTP-401-Handling, Banner)

- [x] **Baseline aus Schritt 08 uebernehmen**
  - [x] `boukensha/` Paket uebertragen (agent, backends, cli, client, config, context, errors, logger, message, prompt_builder, registry, repl, run_dsl, tasks, tool, version)
  - [x] `prompts/system.md` uebernommen
  - [x] `pyproject.toml` angepasst

- [x] **Loader implementieren** (`boukensha_loader.py`)
  - [x] Top-Level-Modul ausserhalb des `boukensha/`-Pakets
  - [x] Aufloesung: `BOUKENSHA_PATH` (Env) > `boukensha_path` (rc-Datei) > eingebetteter Standard
  - [x] `boukensha_dir` aus rc-Datei setzt `BOUKENSHA_DIR` in Env (wird von `Config._resolve_dir` gelesen)
  - [x] `BOUKENSHA_DIR` aus Env wird nicht durch rc-Datei ueberschrieben
  - [x] Pruefung auf `boukensha/__init__.py` im Zielpfad; Abbruch mit Hinweis sonst
  - [x] Schritt-Ordner per `sys.path.insert(0, ...)` laden, dann `importlib.import_module("boukensha")`
  - [x] Abbruch mit Hinweis, wenn geladener Schritt kein callable `repl` hat (vor Schritt 8)
  - [x] `BOUKENSHA_DEBUG=1` gibt Ladepfad auf stderr aus
  - [x] Legacy-Format: rc-Datei enthaelt nur einen Pfad-String (kein YAML-Mapping)

- [x] **Executable anlegen** (`bin/boukensha`)
  - [x] Fuegt Elternverzeichnis in `sys.path` ein, importiert und ruft `load_and_start_repl()` auf
  - [x] Skript ist ausfuehrbar

- [x] **`pyproject.toml` anpassen**
  - [x] `[project.scripts]`: `boukensha = "boukensha_loader:load_and_start_repl"`
  - [x] `VERSION` auf `0.9.0` gesetzt

- [x] **Boukensha-Bibliothek bereinigen (Aenderungen gegenueber Schritt 08)**
  - [x] `Config._resolve_dir`: nur `BOUKENSHA_DIR`-Env oder `~/.boukensha` (cwd-Suche aus Schritt 08 entfernt)
  - [x] `Client`: HTTP-401-Sonderfall entfernt
  - [x] REPL-Banner vereinfacht: nur `config` / `provider` / `model` — keine API-Key- oder Dir-Pruefung

- [x] **Tests erstellen**
  - [x] `test_boukensha_loader.py`: Aufloesung per Env-Var, rc-Datei (Mapping + Legacy-String), Standard (bundled)
  - [x] Test: Env-Var hat Vorrang vor rc-Datei
  - [x] Test: `boukensha_dir` aus rc setzt `BOUKENSHA_DIR`; Env-Var wird nicht ueberschrieben
  - [x] Test: Abbruch bei fehlendem `boukensha/__init__.py`
  - [x] Test: `load_and_start_repl` ruft `boukensha.repl()` auf
  - [x] Test: Abbruch wenn geladener Schritt kein `repl` hat
  - [x] `test_run_step9.py`, `test_run_step8.py`, `test_run_api.py`, `test_logger_subscribe.py` vorhanden

- [x] **Doku aktualisieren**
  - [x] `README.md` vorhanden
  - [x] `README_DE.md` erstellt

## Ausfuehrung

```zsh
cd week1_baseline/python/09_global_executable
pip install .
boukensha
BOUKENSHA_PATH=$PWD/../07_the_run_dsl boukensha
BOUKENSHA_DEBUG=1 boukensha
```

Oder ohne Installation (direkt aus `week1_baseline/`):

```zsh
bin/09_global_executable_python
BOUKENSHA_DEBUG=1 bin/09_global_executable_python
```

Tests ausfuehren:

```zsh
cd week1_baseline/python/09_global_executable
uv run python -m unittest discover -s tests -v
```

## Hinweise

- `boukensha_loader.py` muss Top-Level-Modul bleiben — wuerde es ins `boukensha/`-Paket gehoeren, koennte es kein fremdes `boukensha`-Paket per `sys.path`-Manipulation nachladen.
- `BOUKENSHA_DIR` (Konfigurationsverzeichnis) und `BOUKENSHA_PATH` (Schritt-Ordner) sind unabhaengig.
- Schritte vor Schritt 8 haben kein callable `repl` — der Loader bricht mit hilfreicher Fehlermeldung ab.
