from __future__ import annotations

import os
from pathlib import Path

from .config import PROMPTS_DIR, Config
from .tasks.player import Player


def run_step0(config_dir: Path | None = None) -> int:
    """Gibt die geladene Schritt-00-Konfiguration aus."""
    config = Config(directory=config_dir)
    player_settings = config.tasks("player")

    print("=== Boukensha Schritt 0: Konfiguration ===")
    print()
    print(f"Config dir:     {config.dir}")
    print(f"Tasks:          {', '.join(config.tasks().keys())}")
    print()
    print("-- player task --")

    if not player_settings:
        print("Keine 'player'-Task in settings.yml oder settings.yaml gefunden.")
        return 1

    print(f"Provider:       {Player.provider(player_settings)}")
    print(f"Model:          {Player.model(player_settings)}")
    print(f"Prompt override?{Player.prompt_override(player_settings, 'system')}")

    system_prompt = Player.system_prompt(
        player_settings,
        user_prompts_dir=config.user_prompts_dir,
        default_prompts_dir=PROMPTS_DIR,
    )
    preview = (system_prompt or "")[:60]
    print(f"System prompt:  {preview}...")
    print()
    print(f"MUD host:       {config.mud_host()}:{config.mud_port()}")
    print(f"MUD user:       {config.mud_username()}")
    print()
    print(f"API key set?    {os.environ.get('ANTHROPIC_API_KEY') is not None}")
    print()
    print(config)
    return 0


def main() -> None:
    raise SystemExit(run_step0())

