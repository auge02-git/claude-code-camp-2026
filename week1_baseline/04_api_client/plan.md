# Schritt 04 Plan - API Client

## Ziel
Implementierung von `04_api_client` auf Basis von Schritt 03 und Ruby-Referenz mit vergleichbarem Funktionsumfang.

## Checkliste

- [x] **Baseline aus Schritt 03 uebernehmen**
  - [x] Bestehende Dateien in `boukensha/` nach `04_api_client` uebertragen
  - [x] `Config`, `Context`, `Tool`, `Message`, `Registry`, `PromptBuilder`, `Backends`, `Tasks` weiterfuehren

- [x] **API-Client Kern einfuehren**
  - [x] `boukensha/client.py` anlegen
  - [x] `Client(builder)` implementieren
  - [x] `call(max_output_tokens=...)` fuer echten HTTP-POST implementieren

- [x] **Fehler- und Retry-Handling implementieren**
  - [x] `ApiError` in `boukensha/errors.py` ergaenzen
  - [x] Retry auf Statuscodes `{408, 409, 429, 500, 502, 503, 504}`
  - [x] Retry auf transienten Netzwerkfehlern (Connection reset/refused, timeout, SSL, DNS)
  - [x] Exponential Backoff mit `0.5s`, `1.0s`, `2.0s`

- [x] **Task-Guarding angleichen**
  - [x] `tasks/base.py` `_fetch` gegen nicht-dict Eingaben absichern
  - [x] Fehlermeldungen fuer `provider/model` auf `settings.yaml` angleichen

- [x] **Prompt-Handling vervollstaendigen**
  - [x] `prompts/system.md` fuer Schritt 04 bereitstellen
  - [x] `PROMPTS_DIR` in `config.py` beibehalten (funktionierender Pfad)

- [x] **CLI und Runner erweitern**
  - [x] `run_step4()` in `boukensha/cli.py`
  - [x] Aufbau wie Ruby-Beispiel: Context + Tools + PromptBuilder + Client + API-Call
  - [x] `python -m boukensha` auf Schritt 04 ausrichten

- [x] **Provider-Unterstuetzung sichern**
  - [x] Bestehende Provider aus Schritt 03 erhalten (`anthropic`, `openai`, `gemini`, `ollama`, `ollama_cloud`, `lmstudio`)
  - [x] Provider-zu-Backend Dispatch in der CLI pruefen

- [x] **Tests erstellen**
  - [x] Unit-Tests fuer `Client` (Erfolg, retryable Status, dauerhafter Fehler)
  - [x] Unit-Tests fuer Netzwerkfehler-Retry und `ApiError`
  - [x] Smoke-Test fuer `run_step4()` (mit lokaler/temporarer Konfiguration)

- [x] **Doku und Projektdateien aktualisieren**
  - [x] `README.md` in Deutsch
  - [x] `pyproject.toml` pruefen/aktualisieren
  - [x] Ausfuehrungsbeispiele mit `uv run` dokumentieren

## Ausfuehrung

```zsh
cd week1_baseline/python/04_api_client
uv sync
uv run python -m unittest discover -s tests -v
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

## Hinweise

- Fokus liegt auf **HTTP-Transport + robustem Fehlerverhalten**, nicht auf Agent-Loop (kommt in Schritt 05).
- Implementierung bleibt nah an der Ruby-Referenz; Python-spezifische Unterschiede sind dokumentiert.
