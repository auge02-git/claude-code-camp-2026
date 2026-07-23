from __future__ import annotations

import os
import sys
import tempfile
import textwrap
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha import PROMPTS_DIR, Config, Player
from boukensha.cli import run_step0


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.boukensha_dir = Path(self.temp_dir.name) / ".boukensha"
        self.boukensha_dir.mkdir(parents=True, exist_ok=True)

        settings = textwrap.dedent(
            """
            tasks:
              player:
                provider: anthropic
                model: claude-haiku-4-5
                prompt_override:
                  system: true
            mud:
              host: mud.local
              port: 5000
              username: dummy
              password: secret
            """
        ).strip()
        (self.boukensha_dir / "settings.yml").write_text(settings + "\n", encoding="utf-8")

        env_text = "ANTHROPIC_API_KEY=test-key\n"
        (self.boukensha_dir / ".env").write_text(env_text, encoding="utf-8")

        self._old_dir = os.environ.get("BOUKENSHA_DIR")
        os.environ["BOUKENSHA_DIR"] = str(self.boukensha_dir)

    def tearDown(self) -> None:
        if self._old_dir is None:
            os.environ.pop("BOUKENSHA_DIR", None)
        else:
            os.environ["BOUKENSHA_DIR"] = self._old_dir

    def test_config_loads_settings_and_env(self) -> None:
        config = Config()
        player = config.tasks("player")

        self.assertEqual(player["provider"], "anthropic")
        self.assertEqual(player["model"], "claude-haiku-4-5")
        self.assertEqual(config.mud_host(), "mud.local")
        self.assertEqual(config.mud_port(), 5000)
        self.assertEqual(config.mud_username(), "dummy")
        self.assertEqual(config.mud_password(), "secret")
        self.assertEqual(os.environ.get("ANTHROPIC_API_KEY"), "test-key")

    def test_prompt_resolution_prefers_user_override(self) -> None:
        config = Config()
        player = config.tasks("player")

        default_dir = Path(self.temp_dir.name) / "defaults"
        default_dir.mkdir(parents=True, exist_ok=True)
        (default_dir / "system.md").write_text("default prompt", encoding="utf-8")

        prompt_path = config.save_prompt("player", "system", "custom prompt")
        self.assertTrue(prompt_path.exists())

        prompt = Player.system_prompt(
            player,
            user_prompts_dir=config.user_prompts_dir,
            default_prompts_dir=default_dir,
        )
        self.assertEqual(prompt, "custom prompt")

    def test_prompt_resolution_uses_default_when_override_disabled(self) -> None:
        player = {
            "provider": "anthropic",
            "model": "claude-haiku-4-5",
            "prompt_override": {"system": False},
        }

        default_prompt = Player.system_prompt(
            player,
            user_prompts_dir=Path(self.temp_dir.name) / "missing",
            default_prompts_dir=PROMPTS_DIR,
        )
        self.assertIsNotNone(default_prompt)

    def test_cli_run_step0_returns_zero_with_valid_settings(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            result = run_step0(config_dir=self.boukensha_dir)

        self.assertEqual(result, 0)
        self.assertIn("Boukensha Schritt 0: Konfiguration", stdout.getvalue())

    def test_config_discovers_project_boukensha_dir_from_cwd(self) -> None:
        os.environ.pop("BOUKENSHA_DIR", None)

        project_root = Path(self.temp_dir.name) / "project"
        nested = project_root / "a" / "b"
        nested.mkdir(parents=True, exist_ok=True)

        project_boukensha = project_root / ".boukensha"
        project_boukensha.mkdir(parents=True, exist_ok=True)
        (project_boukensha / "settings.yml").write_text("tasks: {}\n", encoding="utf-8")

        old_cwd = Path.cwd()
        os.chdir(nested)
        try:
            config = Config()
        finally:
            os.chdir(old_cwd)

        self.assertEqual(config.dir, project_boukensha.resolve())


if __name__ == "__main__":
    unittest.main()

