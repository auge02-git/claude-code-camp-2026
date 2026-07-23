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

from boukensha.cli import run_step7


class RunStep7Tests(unittest.TestCase):
    def test_run_step7_with_mocked_dsl_run(self) -> None:
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
            with patch("boukensha.run", return_value="Zusammenfassung"):
                with redirect_stdout(output):
                    code = run_step7(config_dir=cfg)

            self.assertEqual(code, 0)
            rendered = output.getvalue()
            self.assertIn("Step 7: The Boukensha.run DSL", rendered)
            self.assertIn("FINAL RESPONSE", rendered)
            self.assertIn("Zusammenfassung", rendered)


if __name__ == "__main__":
    unittest.main()

