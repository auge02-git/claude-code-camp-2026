# Schritt 06 Plan - Logger (mit log_viz-Kompatibilitaet)

## Ziel
Implementierung von `06_the_logger` auf Basis von Schritt 05.
Abweichung: Die Logger-Ausgabe soll mit `week1_baseline/log_viz/server.py` kompatibel sein.

## Checkliste

- [x] **Plan zuerst pflegen**
  - [x] `plan.md` angelegt
  - [x] Nach Umsetzung auf erledigt setzen

- [x] **Referenz und Abweichung analysieren**
  - [x] Ruby Schritt 06 (`06_the_logger`) gelesen
  - [x] Python Schritt 06 README gelesen
  - [x] `log_viz/server.py` gelesen und Log-Format abgeleitet

- [x] **Baseline aus Schritt 05 uebernehmen**
  - [x] Bestehende `boukensha/` Dateien nach `06_the_logger` uebertragen
  - [x] Agent-Loop und Backends weitergefuehrt

- [x] **Logger-Kern implementieren**
  - [x] `boukensha/logger.py` angelegt
  - [x] Session-Datei erzeugt (log_viz-kompatibles JSONL)
  - [x] Logging-Hooks fuer Request/Response/Tool-Events integriert
  - [x] Event-Struktur an `log_viz` angepasst (`ts`, `session`, `typ`)

- [x] **Integration in Agent/Client/CLI**
  - [x] Logger in `run_step6()` instanziiert
  - [x] Agent-Iteration, Tool-Calls, Responses werden geloggt
  - [x] Session-Pfad wird in CLI ausgegeben

- [x] **Tests erstellt**
  - [x] Unit-Test fuer Logger-Dateierzeugung
  - [x] Unit-Test fuer Event-Format (log_viz-kompatibel)
  - [x] Smoke-Test fuer `run_step6()` mit gemocktem Agent

- [x] **Doku und Projektdateien aktualisiert**
  - [x] `README.md` in Deutsch
  - [x] Besonderheit `log_viz` dokumentiert
  - [x] `uv run` Kommandos dokumentiert

## Ausfuehrung

```zsh
cd week1_baseline/python/06_the_logger
uv sync
uv run python -m unittest discover -s tests -v
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

## Hinweise

- Fokus liegt auf Session-Logging mit nutzbarer Visualisierung in `log_viz`.
- Bei Abweichung zwischen Ruby-Referenz und Visualisierung hat `log_viz`-Kompatibilitaet Vorrang.
