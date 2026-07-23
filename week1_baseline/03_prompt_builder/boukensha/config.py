from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

DEFAULT_DIR = Path.home() / ".boukensha"
PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


class Config:
    """Laedt die Boukensha-Konfiguration aus einem .boukensha-Verzeichnis."""

    def __init__(self, directory: Path | None = None) -> None:
        self.dir = self._resolve_dir(directory)
        self._load_env()
        self.settings = self._load_settings()

    def tasks(self, name: str | None = None) -> dict[str, Any]:
        all_tasks = self.dig("tasks") or {}
        if not isinstance(all_tasks, dict):
            return {}
        if name is None:
            return all_tasks

        task = all_tasks.get(name)
        return task if isinstance(task, dict) else {}

    @property
    def user_prompts_dir(self) -> Path:
        return self.dir / "prompts"

    def mud_host(self) -> str:
        value = self.dig("mud", "host")
        return value if isinstance(value, str) and value else "localhost"

    def mud_port(self) -> int:
        value = self.dig("mud", "port")
        return int(value) if value is not None else 4000

    def mud_username(self) -> str | None:
        value = self.dig("mud", "username")
        return str(value) if value is not None else None

    def mud_password(self) -> str | None:
        value = self.dig("mud", "password")
        return str(value) if value is not None else None

    def dig(self, *keys: str) -> Any:
        node: Any = self.settings
        for key in keys:
            if not isinstance(node, dict):
                return None
            node = node.get(key)
        return node

    def __repr__(self) -> str:
        task_names = ",".join(self.tasks().keys())
        return f"#<Boukensha.Config dir={self.dir} tasks={task_names}>"

    def _resolve_dir(self, directory: Path | None) -> Path:
        if directory is not None:
            return directory.expanduser().resolve()

        raw = os.environ.get("BOUKENSHA_DIR")
        if raw:
            return Path(raw).expanduser().resolve()

        project_dir = self._discover_project_boukensha_dir()
        if project_dir is not None:
            return project_dir

        return DEFAULT_DIR

    def _discover_project_boukensha_dir(self) -> Path | None:
        cwd = Path.cwd().resolve()
        for candidate in [cwd, *cwd.parents]:
            config_dir = candidate / ".boukensha"
            if (config_dir / "settings.yml").exists() or (config_dir / "settings.yaml").exists():
                return config_dir
        return None

    def _load_env(self) -> None:
        env_file = self.dir / ".env"
        if env_file.exists():
            load_dotenv(env_file, override=False)

    def _load_settings(self) -> dict[str, Any]:
        for filename in ("settings.yml", "settings.yaml"):
            settings_file = self.dir / filename
            if not settings_file.exists():
                continue

            loaded = yaml.safe_load(settings_file.read_text(encoding="utf-8"))
            return loaded if isinstance(loaded, dict) else {}

        return {}

