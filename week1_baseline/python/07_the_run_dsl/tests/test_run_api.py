from __future__ import annotations

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

import boukensha


class RunApiTests(unittest.TestCase):
    def test_run_wires_setup_and_writes_snapshot_log(self) -> None:
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
                        max_iterations: 4
                        max_output_tokens: 333
                    mud:
                      host: localhost
                      port: 4000
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            seen: dict[str, object] = {}
            log_path = cfg / "logs" / "custom.jsonl"

            def fake_run(self, task: str) -> str:
                seen["task"] = task
                seen["tools"] = list(self._context.tools.keys())
                return "DSL ok"

            def setup(t) -> None:
                @t.tool(
                    "read_file",
                    description="Read a file",
                    parameters={"path": {"type": "string"}},
                )
                def _read_file(path: str) -> str:
                    return path

            with patch.object(boukensha.Agent, "run", fake_run):
                result = boukensha.run(
                    task="Summarise README.md",
                    setup=setup,
                    config_dir=cfg,
                    log=log_path,
                )

            self.assertEqual(result, "DSL ok")
            self.assertEqual(seen["task"], "Summarise README.md")
            self.assertEqual(seen["tools"], ["read_file"])
            first_event = json.loads(log_path.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(first_event["typ"], "session_start")
            self.assertEqual(first_event["snapshot"]["provider"], "lmstudio")
            self.assertEqual(first_event["snapshot"]["max_iterations"], 4)
            self.assertEqual(first_event["snapshot"]["max_output_tokens"], 333)


if __name__ == "__main__":
    unittest.main()

