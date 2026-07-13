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
ALT_MODEL = "claude-sonnet-4-6"  # Modell-ID vor Nutzung bestätigen


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
    # Explizites OAuth-/Auth-Token (z. B. claude.ai-Konto). None → der
    # anthropic-Client löst Credentials selbst auf (API-Key, ANTHROPIC_AUTH_TOKEN,
    # `ant auth login`-Profil, …). Siehe README Abschnitt „Authentifizierung".
    auth_token: str | None = None
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
        # Auth-Token: Umgebung hat Vorrang, dann settings.yml (auth_token),
        # sonst None (→ SDK-Auto-Auflösung: API-Key / ANTHROPIC_AUTH_TOKEN / ant-Profil).
        auth_token = (
            os.environ.get("BOUKENSHA_AUTH_TOKEN")
            or (settings.get("auth_token") if isinstance(settings, dict) else None)
            or None
        )
        return cls(
            home=home,
            model=str(settings.get("model", DEFAULT_MODEL)),
            system_prompt=system_prompt,
            mud_host=str(mud.get("host", "localhost")),
            mud_port=int(mud.get("port", 4000)),
            auth_token=str(auth_token) if auth_token else None,
            settings=settings if isinstance(settings, dict) else {},
        )
