from __future__ import annotations

import sys
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha.tasks.player import Player


class TaskSettingsTests(unittest.TestCase):
    def test_max_iterations_and_output_tokens(self) -> None:
        settings = {
            "provider": "lmstudio",
            "model": "google/gemma-4-12b-qat",
            "max_iterations": 12,
            "max_output_tokens": 2048,
        }

        self.assertEqual(Player.max_iterations(settings), 12)
        self.assertEqual(Player.max_output_tokens(settings), 2048)

    def test_defaults_when_missing(self) -> None:
        settings = {"provider": "lmstudio", "model": "google/gemma-4-12b-qat"}
        self.assertEqual(Player.max_iterations(settings), 25)
        self.assertIsNone(Player.max_output_tokens(settings))

    def test_provider_model_error_on_invalid_settings(self) -> None:
        with self.assertRaises(ValueError):
            Player.provider(None)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            Player.model(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

