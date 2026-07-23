# 04 · API Client (Python-Port)

Python-3-Port von `ruby/04_api_client`: In diesem Schritt wird der erste echte HTTP-Call
gegen ein Provider-Endpoint ausgefuehrt.

## Ziel von Schritt 04

`PromptBuilder` baut weiterhin nur Payloads. Neu ist `Client`, der diese Payloads wirklich
per HTTP POST verschickt, Response-JSON zurueckliefert und Fehler robust behandelt.

## Neue Komponenten

- `boukensha/client.py`
- `ApiError` in `boukensha/errors.py`
- `prompts/system.md` (Schritt-04 Prompt)

Die Bausteine aus Schritt 03 (`Config`, `Context`, `Tool`, `Message`, `Registry`,
`PromptBuilder`, Backends) werden uebernommen.

## Client-Verhalten

`Client.call(max_output_tokens=1024)`:

- baut den Request-Body aus `builder.to_api_payload(...)`
- sendet HTTP POST an `builder.url()`
- nutzt `builder.headers()`
- gibt geparstes JSON (`dict`) zurueck

### Retry-Strategie

- Retryable Status: `408, 409, 429, 500, 502, 503, 504`
- Transiente Fehler: Connection reset/refused, Timeout, SSL, DNS, HTTP-Protokollfehler
- `MAX_RETRIES = 3`  → insgesamt bis zu 4 Versuche
- Exponential Backoff: `0.5s`, `1.0s`, `2.0s`

Nach finalem Fehlschlag wird `ApiError` geworfen.

## CLI

`python -m boukensha` startet jetzt `run_step4()`:

- erstellt Context + Registry + Demo-Tools
- baut Payload ueber PromptBuilder
- sendet echten Request ueber `Client`
- gibt rohe API-Response formatiert aus

## Setup

```zsh
cd week1_baseline/python/04_api_client
uv sync
```

## Tests

```zsh
cd week1_baseline
uv run python -m unittest discover -s python/04_api_client/tests -v
```

Enthaelt:

- `tests/test_client.py` (HTTP-Mockserver, Erfolg/Retry/Fehler)
- `tests/test_run_step4.py` (Smoke-Test fuer CLI-Flow mit gemocktem Client)

## Ausfuehrung

Mit Projekt-Config:

```zsh
cd week1_baseline/python/04_api_client
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

Hinweis zu Providern:

- `lmstudio` funktioniert lokal ohne API-Key
- `anthropic`, `openai`, `gemini`, `ollama_cloud` benoetigen passende API-Keys
- `ollama` benoetigt lokalen Ollama-Server

## Relevante Dateien

- `python/04_api_client/boukensha/client.py`
- `python/04_api_client/boukensha/errors.py`
- `python/04_api_client/boukensha/cli.py`
- `python/04_api_client/tests/test_client.py`
- `python/04_api_client/tests/test_run_step4.py`
