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

from boukensha.cli import run_step5


class RunStep5Tests(unittest.TestCase):
    def test_run_step5_with_mocked_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / ".boukensha"
            cfg.mkdir(parents=True, exist_ok=True)
            settings = textwrap.dedent(
                """
                tasks:
                  player:
                    provider: lmstudio
                    model: google/gemma-4-12b-qat
                    prompt_override:
                      system: false
                    max_iterations: 3
                mud:
                  host: localhost
                  port: 4000
                """
            ).strip()
            (cfg / "settings.yml").write_text(settings + "\n", encoding="utf-8")

            out = io.StringIO()
            with patch("boukensha.cli.Agent.run", return_value="Fertig."):
                with redirect_stdout(out):
                    code = run_step5(config_dir=cfg)

            self.assertEqual(code, 0)
            rendered = out.getvalue()
            self.assertIn("Step 5: Agent Loop", rendered)
            self.assertIn("Final response:", rendered)
            self.assertIn("Fertig.", rendered)


if __name__ == "__main__":
    unittest.main()

