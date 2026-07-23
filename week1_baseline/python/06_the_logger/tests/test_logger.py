from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha.logger import Logger


class LoggerFormatTests(unittest.TestCase):
    def test_writes_log_viz_compatible_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            logger = Logger(session_id="s1", dir=Path(tmp))
            logger.iteration(1, 10)
            logger.tool_call("list_directory", {"path": "."})
            logger.tool_result(name="list_directory", result="a\nb", ok=True)
            logger.turn_end(reason="completed", iterations=1, tokens={"input_tokens": 1, "output_tokens": 2})
            logger.close()

            log_file = Path(tmp) / "s1" / "events.jsonl"
            self.assertTrue(log_file.exists())

            for line in log_file.read_text(encoding="utf-8").splitlines():
                event = json.loads(line)
                self.assertIn("ts", event)
                self.assertIn("session", event)
                self.assertIn("typ", event)
                self.assertEqual(event["session"], "s1")


if __name__ == "__main__":
    unittest.main()

