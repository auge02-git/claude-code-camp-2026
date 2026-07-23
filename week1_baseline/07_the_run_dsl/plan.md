# Schritt 07 Plan - Run DSL

## Ziel
Implementierung von `07_the_run_dsl` auf Basis von Schritt 06 und Ruby-Referenz mit vergleichbarem Funktionsumfang.

## Checkliste

- [x] **Plan zuerst pflegen**
  - [x] `plan.md` angelegt
  - [ ] Nach Umsetzung auf erledigt setzen

- [ ] **Referenz analysieren**
  - [ ] Ruby Schritt 07 gelesen
  - [ ] Python Schritt 07 README gelesen
  - [ ] Unterschiede Ruby -> Python fuer DSL festgehalten

- [ ] **Baseline aus Schritt 06 uebernehmen**
  - [ ] Bestehende `boukensha/` Dateien nach `07_the_run_dsl` uebertragen
  - [ ] Logger-/Agent-/Backend-Verhalten weiterfuehren

- [ ] **Run DSL implementieren**
  - [ ] `boukensha/run_dsl.py` anlegen
  - [ ] `RunDSL.tool(...)` als schmale DSL-Fassade implementieren
  - [ ] Top-level `run(...)` API bereitstellen

- [ ] **Logger erweitern**
  - [ ] `turn(n)` Event ergaenzen
  - [ ] `subscribe(callback)` unterstuetzen
  - [ ] Subscriber bei jedem Event benachrichtigen

- [ ] **CLI und API erweitern**
  - [ ] `run_step7()` in `boukensha/cli.py`
  - [ ] DSL-basiertes Beispiel statt manueller Verdrahtung
  - [ ] `python -m boukensha` auf Schritt 07 ausrichten

- [ ] **Tests erstellen**
  - [ ] Unit-Tests fuer `RunDSL.tool()`
  - [ ] Integrationstest fuer `run(...)`
  - [ ] Tests fuer Logger-Subscriber/Turn-Events
  - [ ] Smoke-Test fuer `run_step7()`

- [ ] **Doku aktualisieren**
  - [ ] `README.md` in Deutsch
  - [ ] Python-spezifische DSL-Form (`setup(dsl)` statt Ruby `instance_eval`) dokumentieren
  - [ ] `uv run` Kommandos dokumentieren

## Ausfuehrung (geplant)

```zsh
cd week1_baseline/python/07_the_run_dsl
uv sync
uv run python -m unittest discover -s tests -v
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

## Hinweise

- In Python wird die DSL ueber einen `setup`-Callable exponiert, nicht ueber Ruby-`instance_eval`.
- Die Logger-Events muessen kompatibel zu `log_viz` bleiben.

