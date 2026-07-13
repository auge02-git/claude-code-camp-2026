"""Konfiguration (Diagramm-Knoten ``config.rb``).

Liest das Agent-Home ``~/.boukensha`` (überschreibbar via ``BOUKENSHA_DIR``):
- ``settings.yml``   — Einstellungen (u. a. LLM-Modell)
- ``credentials``    — Zugangsdaten (z. B. .env-artig; hier optional)
- ``prompts/system.md`` — überschreibbarer System-Prompt
- ``logs/<session_id>/<datum>.jsonl`` — Sitzungs-Logs (siehe :mod:`boukensha.logger`)

Die MUD-Zugangsdaten selbst liegen bereits in ``mud-mcp/credentials.json`` und
werden vom MudManager wiederverwendet — hier NICHT dupliziert.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - yaml ist harte Abhängigkeit, aber Stub-tolerant
    yaml = None

# LLM-Modell laut Vorgaben: primär Haiku 4.5, Alternative Sonnet 4.6.
# (Bewusst NICHT das "neueste/Default"-Modell.)
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
ALT_MODEL = "bedrock/eu.anthropic.claude-sonnet-4-6"


def boukensha_dir() -> Path:
    """Agent-Home ``~/.boukensha`` (oder ``$BOUKENSHA_DIR``)."""
    return Path(os.environ.get("BOUKENSHA_DIR", str(Path.home() / ".boukensha")))


@dataclass
class Config:
    """Zusammengeführte Laufzeit-Konfiguration."""

    home: Path
    model: str = DEFAULT_MODEL
    system_prompt: str = ""
    mud_host: str = "localhost"
    mud_port: int = 4000
    llm_base_url: str | None = None
    llm_api_key: str | None = None   # expliziter Key (CLI/Env), überschreibt ANTHROPIC_API_KEY
    settings: dict = field(default_factory=dict)

    @classmethod
    def load(cls) -> "Config":
        """Lädt ``settings.yml`` + ``prompts/system.md`` aus dem Agent-Home.

        Fehlt etwas, werden sinnvolle Vorgabewerte genutzt (kein harter Fehler),
        damit der Agent auch ohne vorbereitetes Home startet.
        """
        home = boukensha_dir()
        settings: dict = {}
        settings_file = home / "settings.yml"
        if yaml is not None and settings_file.exists():
            try:
                settings = yaml.safe_load(settings_file.read_text(encoding="utf-8")) or {}
            except Exception:
                settings = {}

        system_prompt = ""
        sys_file = home / "prompts" / "system.md"
        if sys_file.exists():
            system_prompt = sys_file.read_text(encoding="utf-8")

        mud = settings.get("mud", {}) if isinstance(settings, dict) else {}
        llm = settings.get("llm", {}) if isinstance(settings, dict) else {}
        llm_base_url = os.environ.get("BOUKENSHA_LLM_BASE_URL") or str(
            llm.get("base_url", settings.get("llm_base_url", ""))
        ).strip()
        llm_api_key = os.environ.get("BOUKENSHA_API_KEY") or str(
            llm.get("api_key", settings.get("llm_api_key", ""))
        ).strip() or None
        model = str(settings.get("model", DEFAULT_MODEL))
        model = os.environ.get("BOUKENSHA_LLM_MODEL", model)
        model = os.environ.get("ANTHROPIC_LLM_MODEL", model)
        return cls(
            home=home,
            model=model,
            system_prompt=system_prompt,
            mud_host=str(mud.get("host", "localhost")),
            mud_port=int(mud.get("port", 4000)),
            llm_base_url=llm_base_url or None,
            llm_api_key=llm_api_key,
            settings=settings if isinstance(settings, dict) else {},
        )
