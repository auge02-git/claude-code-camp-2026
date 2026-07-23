from __future__ import annotations

import json
import os
from pathlib import Path

from .backends.anthropic import Anthropic
from .backends.gemini import Gemini
from .backends.lmstudio import LMStudio
from .backends.ollama import Ollama
from .backends.ollama_cloud import OllamaCloud
from .backends.openai import OpenAI
from .config import Config, PROMPTS_DIR
from .context import Context
from .prompt_builder import PromptBuilder
from .registry import Registry
from .tasks.player import Player


def run_step3(config_dir: Path | None = None) -> int:
    config = Config(directory=config_dir)
    player_settings = config.tasks("player")
    if not player_settings:
        print("Keine 'player'-Task in settings.yml oder settings.yaml gefunden.")
        return 1

    system_prompt = Player.system_prompt(
        player_settings,
        user_prompts_dir=config.user_prompts_dir,
        default_prompts_dir=PROMPTS_DIR,
    )

    ctx = Context(task=Player, system=system_prompt)
    registry = Registry(ctx)

    @registry.tool("look", description="Look around the current room for details", parameters={})
    def look() -> str:
        return "A damp stone corridor stretches north. Torches flicker on the walls."

    @registry.tool(
        "move",
        description="Move the player in a direction (north, south, east, west, up, down)",
        parameters={"direction": {"type": "string", "description": "The direction to move"}},
    )
    def move(direction: str) -> str:
        return f"You move {direction} into a torch-lit corridor."

    ctx.add_message("user", "I just arrived in the dungeon. What's around me, and can you move north?")
    ctx.add_message("assistant", "Let me take a look around first.")
    ctx.add_message(
        "tool_result",
        "A damp stone corridor stretches north. Torches flicker on the walls.",
        tool_use_id="toolu_01X",
    )

    provider = Player.provider(player_settings)
    model = Player.model(player_settings)

    if provider == "anthropic":
        backend = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], model=model)
    elif provider == "ollama":
        backend = Ollama(model=model)
    elif provider == "ollama_cloud":
        backend = OllamaCloud(api_key=os.environ["OLLAMA_API_KEY"], model=model)
    elif provider == "openai":
        backend = OpenAI(api_key=os.environ["OPENAI_API_KEY"], model=model)
    elif provider == "gemini":
        backend = Gemini(api_key=os.environ["GEMINI_API_KEY"], model=model)
    elif provider == "lmstudio":
        backend = LMStudio(model=model)
    else:
        raise ValueError(f"Unsupported provider for player task: {provider}")

    builder = PromptBuilder(ctx, backend)

    print("=== BOUKENSHA Step 3: Prompt Builder ===")
    print()
    print(f"Config: {config}")
    print(f"Provider: {provider}")
    print(f"Model: {model}")
    print(json.dumps(builder.to_api_payload(), indent=2))
    return 0


def main() -> None:
    raise SystemExit(run_step3())

