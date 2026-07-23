import os

from . import backends
from .agent import Agent
from .backends.anthropic import Anthropic
from .backends.gemini import Gemini
from .backends.lmstudio import LMStudio
from .backends.ollama import Ollama
from .backends.ollama_cloud import OllamaCloud
from .backends.openai import OpenAI
from .cli import run_step7
from .client import Client
from .config import Config, PROMPTS_DIR
from .context import Context
from .errors import ApiError, LoopError, UnknownToolError, UnsupportedModelError
from .logger import Logger
from .message import Message
from .prompt_builder import PromptBuilder
from .registry import Registry
from .run_dsl import RunDSL
from .tasks.player import Player
from .tool import Tool

_quiet = False
_debug = False
_config: Config | None = None


def config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config


def set_quiet(value: bool = True) -> None:
    global _quiet
    _quiet = value


def quiet() -> bool:
    return _quiet


def set_debug(value: bool = True) -> None:
    global _debug
    _debug = value


def debug() -> bool:
    return _debug


def _resolve_backend(*, backend: str, model: str, api_key: str | None, ollama_host: str):
    if backend == "anthropic":
        return Anthropic(api_key=api_key or "", model=model)
    if backend == "openai":
        return OpenAI(api_key=api_key or "", model=model)
    if backend == "gemini":
        return Gemini(api_key=api_key or "", model=model)
    if backend == "ollama":
        return Ollama(model=model, host=ollama_host)
    if backend == "ollama_cloud":
        return OllamaCloud(api_key=api_key or "", model=model)
    if backend == "lmstudio":
        return LMStudio(model=model)
    raise ValueError(
        f"Unknown backend {backend!r}. Use 'anthropic', 'openai', 'gemini', 'ollama', 'ollama_cloud', or 'lmstudio'."
    )


def run(
    *,
    task: str,
    system: str | None = None,
    model: str | None = None,
    backend: str | None = None,
    api_key: str | None = None,
    ollama_host: str = "http://localhost:11434",
    log=None,
    max_output_tokens: int | None = None,
    setup=None,
    config_dir=None,
):
    cfg = Config(directory=config_dir)
    task_class = Player
    task_settings = cfg.tasks(task_class.task_name())

    system = system or task_class.system_prompt(
        task_settings,
        user_prompts_dir=cfg.user_prompts_dir,
        default_prompts_dir=PROMPTS_DIR,
    )
    model = model or task_class.model(task_settings)
    backend = backend or task_class.provider(task_settings)

    if api_key is None:
        api_key = {
            "anthropic": os.environ.get("ANTHROPIC_API_KEY"),
            "openai": os.environ.get("OPENAI_API_KEY"),
            "gemini": os.environ.get("GEMINI_API_KEY"),
            "ollama_cloud": os.environ.get("OLLAMA_API_KEY"),
        }.get(backend)

    ctx = Context(task=task_class, system=system)
    registry = Registry(ctx)
    if setup is not None:
        setup(RunDSL(registry))

    be = _resolve_backend(backend=backend, model=model, api_key=api_key, ollama_host=ollama_host)
    builder = PromptBuilder(ctx, be)
    client = Client(builder)
    effective_max_iterations = task_class.max_iterations(task_settings)
    effective_max_output = max_output_tokens if max_output_tokens is not None else task_class.max_output_tokens(task_settings)
    logger = Logger(
        dir=cfg.dir / "logs",
        log=log,
        snapshot={
            "task": task_class.task_name(),
            "max_iterations": effective_max_iterations,
            "max_output_tokens": effective_max_output,
            "model": model,
            "provider": backend,
        },
    )
    try:
        agent = Agent(
            context=ctx,
            registry=registry,
            builder=builder,
            client=client,
            logger=logger,
            task_settings=task_settings,
            max_iterations=effective_max_iterations,
            max_output_tokens=effective_max_output,
        )
        return agent.run(task)
    finally:
        logger.close()

__all__ = [
    "Config",
    "PROMPTS_DIR",
    "Context",
    "Agent",
    "Client",
    "Logger",
    "Message",
    "Tool",
    "Registry",
    "PromptBuilder",
    "RunDSL",
    "Player",
    "ApiError",
    "LoopError",
    "UnknownToolError",
    "UnsupportedModelError",
    "backends",
    "config",
    "set_quiet",
    "quiet",
    "set_debug",
    "debug",
    "run",
    "run_step7",
]

