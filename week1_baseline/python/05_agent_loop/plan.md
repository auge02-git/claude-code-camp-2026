# Schritt 05 Plan - Agent Loop

## Ziel
Implementierung von `05_agent_loop` auf Basis von Schritt 04 und Ruby-Referenz mit vergleichbarem Funktionsumfang.

## Checkliste

- [x] **Plan zuerst pflegen**
  - [x] `plan.md` angelegt
  - [x] Nach Umsetzung auf erledigt setzen

- [x] **Baseline aus Schritt 04 uebernehmen**
  - [x] Bestehende Dateien in `boukensha/` nach `05_agent_loop` uebertragen
  - [x] `Client`, `PromptBuilder`, `Backends`, `Registry`, `Config` weiterfuehren

- [x] **Agent-Schleife einfuehren**
  - [x] `boukensha/agent.py` anlegen
  - [x] `Agent.run(user_input)` mit Iterationslogik implementieren
  - [x] `tool_use` -> Tool-Dispatch -> naechster API-Call
  - [x] `end_turn` -> finale Antwort zurueckgeben

- [x] **Wind-Down bei Iterationslimit**
  - [x] `max_iterations` aus Task-Settings nutzen
  - [x] Wrap-up Nachricht ohne Tools (`tools: []`) senden
  - [x] Fallback-Text bei Fehler/leerem Ergebnis

- [x] **Response-Normalisierung sichern**
  - [x] `parse_response()` fuer alle Backends bereitstellen/pruefen
  - [x] Normalisierte Form `{stop_reason, content}` in Agent nutzen

- [x] **Task-Settings erweitern**
  - [x] `tasks/base.py` um `max_iterations` und `max_output_tokens` erweitern
  - [x] Guarding fuer fehlende Werte beibehalten

- [x] **Fehlerklassen erweitern**
  - [x] `LoopError` in `errors.py` ergaenzen (wie Ruby Schritt 5)

- [x] **CLI auf Schritt 5 anheben**
  - [x] `run_step5()` in `boukensha/cli.py`
  - [x] Context + Registry + Agent zusammenbauen
  - [x] Ausgabe der finalen Assistant-Antwort

- [x] **Tests erstellen**
  - [x] Unit-Tests fuer Agent-Loop (`tool_use`, `end_turn`, Iterationslimit)
  - [x] Tests fuer Task-Settings-Resolver
  - [x] Smoke-Test fuer `run_step5()` mit gemocktem Client/Backend

- [x] **Doku aktualisieren**
  - [x] `README.md` in Deutsch
  - [x] `pyproject.toml` pruefen/aktualisieren
  - [x] `uv run` Kommandos dokumentieren

## Ausfuehrung

```zsh
cd week1_baseline/python/05_agent_loop
uv sync
uv run python -m unittest discover -s tests -v
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

## Hinweise

- Fokus liegt auf der **agentischen Schleife** (mehrere API-Aufrufe + Tool-Dispatch).
- Verhalten bleibt nah an der Ruby-Referenz; Python-spezifische Unterschiede sind dokumentiert.
