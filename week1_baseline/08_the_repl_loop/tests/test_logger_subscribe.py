from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha.logger import Logger


class LoggerSubscribeTests(unittest.TestCase):
    def test_turn_and_subscribe_emit_original_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            logger = Logger(session_id="sess-1", dir=Path(tmp))
            events: list[dict] = []
            logger.subscribe(events.append)

            logger.turn(1)
            logger.iteration(1, 5)
            logger.close()

            self.assertEqual(events[0]["typ"], "turn")
            self.assertEqual(events[0]["n"], 1)
            self.assertEqual(events[1]["typ"], "iteration")
            self.assertNotIn("session", events[0])
            self.assertNotIn("ts", events[0])


if __name__ == "__main__":
    unittest.main()

