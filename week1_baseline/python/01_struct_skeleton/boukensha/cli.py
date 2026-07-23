from __future__ import annotations

import os
from pathlib import Path

from .config import Config
from .context import Context
from .message import Message
from .tasks.player import Player
from .tool import Tool


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


def run_step1(config_dir: Path | None = None) -> int:
    """Ausfuehrung von Schritt 01: Struct Skeleton."""
    config = Config(directory=config_dir)
    player_settings = config.tasks("player")

    system_prompt = Player.system_prompt(
        player_settings,
        user_prompts_dir=config.user_prompts_dir,
    )

    ctx = Context(task=Player, system=system_prompt)

    ctx.register_tool(
        Tool(
            "move",
            "Move the player in a direction (north, south, east, west, up, down)",
            {"direction": {"type": "string", "description": "The direction to move"}},
            lambda direction: f"You move {direction} into a torch-lit corridor.",
        )
    )

    ctx.add_message("user", "Explore north and tell me what you find.")
    ctx.add_message("assistant", "Sure, let me head north and take a look.")

    print("=== Boukensha Schritt 1: Struct Skeleton ===")
    print()
    print(f"Config:   {config}")
    print(f"Context:  {ctx}")
    print(f"Tool:     {ctx.tools['move']}")
    print("Messages:")
    for msg in ctx.messages:
        print(f"  {msg}")
    print()
    return 0


def main() -> None:
    raise SystemExit(run_step1())

