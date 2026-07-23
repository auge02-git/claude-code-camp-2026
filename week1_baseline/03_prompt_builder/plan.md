# Schritt 03 Plan - Prompt Builder

## Ziel
Implementierung von `03_prompt_builder` auf Basis von Schritt 02 und Ruby-Referenz mit vergleichbarem Funktionsumfang.

## Checkliste

- [x] **Baseline aus Schritt 02 uebernehmen**
  - [x] Bestehende Dateien in `boukensha/` nach `03_prompt_builder` uebertragen
  - [x] `Config`, `Context`, `Tool`, `Message`, `Registry`, `Tasks` unveraendert weiterfuehren

- [x] **Prompt-Builder Kern einfuehren**
  - [x] `boukensha/prompt_builder.py` anlegen
  - [x] `PromptBuilder(context, backend)` implementieren
  - [x] Methoden: `to_messages()`, `to_tools()`, `to_api_payload(max_output_tokens=...)`, `headers()`, `url()`

- [x] **Backend-Abstraktion erstellen**
  - [x] `boukensha/backends/base.py` mit gemeinsamem Vertrag
  - [x] Modellvalidierung ueber `MODELS` Tabelle
  - [x] Kosten-/Kontextfenster-Helfer
  - [x] `UnsupportedModelError` in `boukensha/errors.py` ergaenzen

- [x] **Konkrete Backends implementieren**
  - [x] `boukensha/backends/anthropic.py`
  - [x] `boukensha/backends/openai.py`
  - [x] `boukensha/backends/gemini.py`
  - [x] `boukensha/backends/ollama.py`
  - [x] `boukensha/backends/ollama_cloud.py`
  - [x] Provider-spezifische Payload-, Message- und Tool-Serialisierung

- [x] **Prompt-Handling vervollstaendigen**
  - [x] `prompts/system.md` fuer Schritt 03 bereitstellen
  - [x] Rueckkehr von `PROMPTS_DIR` in `config.py` (wie Ruby Schritt 03)

- [x] **CLI und Runner erweitern**
  - [x] `run_step3()` in `boukensha/cli.py`
  - [x] Demo-Ausgabe fuer verschiedene Backends/Serialisierungen
  - [x] `python -m boukensha` auf Schritt 03 ausrichten

- [x] **Tests erstellen**
  - [x] Unit-Tests fuer `PromptBuilder`
  - [x] Unit-Tests pro Backend (Messages/Tools/Payload)
  - [x] Fehlerfaelle: unbekanntes Modell, fehlende Tool-IDs, etc.
  - [x] Smoke-Test fuer Schritt 03 CLI

- [x] **Doku und Projektdateien aktualisieren**
  - [x] `README.md` in Deutsch
  - [x] `pyproject.toml` pruefen/aktualisieren
  - [x] Ausfuehrungsbeispiele mit `uv run`

## Ausfuehrung

```zsh
cd week1_baseline/python/03_prompt_builder
uv sync
uv run python -m unittest tests -v
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

## Hinweise

- Fokus bleibt auf API-Serialisierung, nicht auf HTTP-Call-Ausfuehrung (kommt spaeter).
- Verhalten bleibt nah an der Ruby-Referenz; Python-typische Unterschiede sind dokumentiert.
