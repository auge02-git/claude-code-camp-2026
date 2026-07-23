from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha.cli import run_step9


class RunStep9Tests(unittest.TestCase):
    def test_run_step9_calls_repl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / ".boukensha"
            cfg.mkdir(parents=True, exist_ok=True)
            (cfg / "settings.yml").write_text(
                textwrap.dedent(
                    """
                    tasks:
                      player:
                        provider: lmstudio
                        model: google/gemma-4-12b-qat
                        prompt_override:
                          system: false
                    mud:
                      host: localhost
                      port: 4000
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            with patch("boukensha.repl", return_value=None) as mock_repl:
                code = run_step9(config_dir=cfg)

            self.assertEqual(code, 0)
            mock_repl.assert_called_once_with(config_dir=cfg)


if __name__ == "__main__":
    unittest.main()
