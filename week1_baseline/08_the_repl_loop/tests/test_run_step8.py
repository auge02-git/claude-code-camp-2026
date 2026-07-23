from __future__ import annotations

import io
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha.cli import run_step8


class RunStep8Tests(unittest.TestCase):
    def test_run_step8_with_mocked_repl(self) -> None:
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

            output = io.StringIO()
            with patch("boukensha.repl", return_value=None):
                with redirect_stdout(output):
                    code = run_step8(config_dir=cfg)

            self.assertEqual(code, 0)
            rendered = output.getvalue()
            self.assertIn("Step 8: The REPL Loop", rendered)


if __name__ == "__main__":
    unittest.main()
