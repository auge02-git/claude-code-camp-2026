from __future__ import annotations

import json
import os
from pathlib import Path

from .agent import Agent
from .backends.anthropic import Anthropic
from .backends.gemini import Gemini
from .backends.lmstudio import LMStudio
from .backends.ollama import Ollama
from .backends.ollama_cloud import OllamaCloud
from .backends.openai import OpenAI
from .client import Client
from .config import Config, PROMPTS_DIR
from .context import Context
from .errors import ApiError
from .logger import Logger
from .prompt_builder import PromptBuilder
from .registry import Registry
from .tasks.player import Player


def run_step6(config_dir: Path | None = None) -> int:
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

    @registry.tool(
        "read_file",
        description="Read the contents of a file from disk",
        parameters={"path": {"type": "string", "description": "The file path to read"}},
    )
    def read_file(path: str) -> str:
        return Path(path).read_text(encoding="utf-8")

    @registry.tool(
        "list_directory",
        description="List files in a directory",
        parameters={"path": {"type": "string", "description": "The directory path to list"}},
    )
    def list_directory(path: str) -> str:
        return "\n".join(p.name for p in Path(path).iterdir() if not p.name.startswith("."))

    ctx.add_message("user", "What files are in the current directory?")

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
    client = Client(builder)
    logger = Logger(dir=config.dir / "logs")
    agent = Agent(
        context=ctx,
        registry=registry,
        builder=builder,
        client=client,
        logger=logger,
        task_settings=player_settings,
    )

    print("=== BOUKENSHA Step 6: The Logger ===")
    print()
    print(f"Config: {config}")
    print(f"Provider: {provider}")
    print(f"Model: {model}")
    print(f"Session: {logger.session_id}")
    print(f"Log file: {logger.path}")
    print(f"Sending requests to {builder.url()}...")
    print()

    try:
        final_answer = agent.run("What files are in the current directory?")
    except ApiError as exc:
        print(f"ApiError: {exc}")
        return 1

    print("Final response:")
    print(final_answer)
    logger.close()
    return 0


def main() -> None:
    raise SystemExit(run_step6())

