# 03 · Prompt Builder (Python-Port)

Python-3-Port von `ruby/03_prompt_builder`: Der `PromptBuilder` serialisiert einen `Context`
in das jeweilige API-Format des ausgewaehlten Backends.

## Was ist neu in Schritt 03?

- `boukensha/prompt_builder.py`
- `boukensha/backends/base.py`
- `boukensha/backends/anthropic.py`
- `boukensha/backends/openai.py`
- `boukensha/backends/gemini.py`
- `boukensha/backends/lmstudio.py`
- `boukensha/backends/ollama.py`
- `boukensha/backends/ollama_cloud.py`
- `prompts/system.md`
- `UnsupportedModelError` in `boukensha/errors.py`

Die Bausteine aus Schritt 02 (`Config`, `Context`, `Tool`, `Message`, `Registry`, `Tasks`) werden
weiterverwendet.

## PromptBuilder

`PromptBuilder` delegiert an ein Backend:

- `to_messages()`
- `to_tools()`
- `to_api_payload(max_output_tokens=1024)`
- `headers()`
- `url()`

## Backends (in diesem Schritt)

- `Anthropic`
- `OpenAI`
- `Gemini`
- `LMStudio`
- `Ollama`
- `OllamaCloud`

Jedes Backend hat:

- `MODELS`-Tabelle (mit `context_window`, `cost_per_million`, `usage_unit`, optional `usage_level`)
- Modellvalidierung (`UnsupportedModelError`)
- provider-spezifische Serialisierung von Messages, Tools und Payload

## Setup

```zsh
cd week1_baseline/python/03_prompt_builder
uv sync
```

## Ausfuehrung

Mit der Projekt-Konfiguration:

```zsh
cd week1_baseline/python/03_prompt_builder
BOUKENSHA_DIR=../../.boukensha uv run python -m boukensha
```

Hinweis: Bei `provider: anthropic`, `openai`, `gemini` oder `ollama_cloud` muss der passende
API-Key gesetzt sein (z. B. `ANTHROPIC_API_KEY`).

`provider: lmstudio` nutzt ein lokales OpenAI-kompatibles Endpoint (`http://localhost:1234/v1/chat/completions`)
und benoetigt keinen API-Key.

## Tests

```zsh
cd week1_baseline
uv run python -m unittest python/03_prompt_builder/tests/test_prompt_builder.py -v
```

## Wichtige Dateien

- `python/03_prompt_builder/boukensha/config.py`
- `python/03_prompt_builder/boukensha/prompt_builder.py`
- `python/03_prompt_builder/boukensha/backends/base.py`
- `python/03_prompt_builder/boukensha/backends/anthropic.py`
- `python/03_prompt_builder/boukensha/backends/openai.py`
- `python/03_prompt_builder/boukensha/backends/gemini.py`
- `python/03_prompt_builder/boukensha/backends/lmstudio.py`
- `python/03_prompt_builder/boukensha/backends/ollama.py`
- `python/03_prompt_builder/boukensha/backends/ollama_cloud.py`
- `python/03_prompt_builder/boukensha/cli.py`
- `python/03_prompt_builder/tests/test_prompt_builder.py`
