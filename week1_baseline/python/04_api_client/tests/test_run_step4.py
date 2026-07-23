from __future__ import annotations

import io
import os
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

from boukensha.cli import run_step4


class RunStep4Tests(unittest.TestCase):
    def test_run_step4_with_mocked_client(self) -> None:
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
                mud:
                  host: localhost
                  port: 4000
                """
            ).strip()
            (cfg / "settings.yml").write_text(settings + "\n", encoding="utf-8")

            fake_response = {"id": "resp_1", "output": "ok"}
            out = io.StringIO()
            with patch("boukensha.cli.Client.call", return_value=fake_response):
                with redirect_stdout(out):
                    code = run_step4(config_dir=cfg)

            self.assertEqual(code, 0)
            rendered = out.getvalue()
            self.assertIn("Step 4: API Client", rendered)
            self.assertIn('"id": "resp_1"', rendered)


if __name__ == "__main__":
    unittest.main()

