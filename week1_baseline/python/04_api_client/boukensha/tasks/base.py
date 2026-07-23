from __future__ import annotations

from pathlib import Path
from typing import Any


class Base:
    @classmethod
    def task_name(cls) -> str:
        raise NotImplementedError(f"{cls.__name__} must define task_name()")

    @classmethod
    def provider(cls, settings: dict[str, Any]) -> str:
        provider_name = cls._fetch(settings, "provider")
        if not isinstance(provider_name, str) or not provider_name:
            raise ValueError(f"tasks.{cls.task_name()}.provider is required in settings.yaml")
        return provider_name

    @classmethod
    def model(cls, settings: dict[str, Any]) -> str:
        model_name = cls._fetch(settings, "model")
        if not isinstance(model_name, str) or not model_name:
            raise ValueError(f"tasks.{cls.task_name()}.model is required in settings.yaml")
        return model_name

    @classmethod
    def prompt_override(cls, settings: dict[str, Any], prompt: str = "system") -> bool:
        node = cls._fetch(settings, "prompt_override")
        return isinstance(node, dict) and node.get(prompt) is True

    @classmethod
    def prompt(
        cls,
        settings: dict[str, Any],
        name: str = "system",
        user_prompts_dir: Path | None = None,
        default_prompts_dir: Path | None = None,
    ) -> str | None:
        if cls.prompt_override(settings, name):
            user_text = cls._read_user_prompt(name, user_prompts_dir=user_prompts_dir)
            if user_text:
                return user_text

        return cls._read_default_prompt(name, default_prompts_dir=default_prompts_dir)

    @classmethod
    def system_prompt(
        cls,
        settings: dict[str, Any],
        user_prompts_dir: Path | None = None,
        default_prompts_dir: Path | None = None,
    ) -> str | None:
        return cls.prompt(
            settings,
            "system",
            user_prompts_dir=user_prompts_dir,
            default_prompts_dir=default_prompts_dir,
        )

    @classmethod
    def _fetch(cls, settings: dict[str, Any], key: str) -> Any:
        if not isinstance(settings, dict):
            return None
        return settings.get(key)

    @classmethod
    def _read_user_prompt(cls, prompt_name: str, user_prompts_dir: Path | None = None) -> str | None:
        if user_prompts_dir is None:
            return None
        return cls._read_file(user_prompts_dir / cls.task_name() / f"{prompt_name}.md")

    @classmethod
    def _read_default_prompt(
        cls,
        prompt_name: str,
        default_prompts_dir: Path | None = None,
    ) -> str | None:
        if default_prompts_dir is None:
            return None
        return cls._read_file(default_prompts_dir / f"{prompt_name}.md")

    @staticmethod
    def _read_file(path: Path) -> str | None:
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8").strip()

