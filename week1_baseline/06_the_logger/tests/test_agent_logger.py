from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha.agent import Agent
from boukensha.context import Context
from boukensha.logger import Logger
from boukensha.tasks.player import Player


class _FakeRegistry:
    def dispatch(self, name: str, args: dict):
        if name == "list_directory":
            return "README.md"
        return "ok"


class _FakeBackend:
    model = "fake-model"
    usage_unit = "tokens"
    usage_level = None

    @staticmethod
    def estimate_cost(*, input_tokens: int, output_tokens: int):
        return 0.0


class _FakeBuilder:
    def __init__(self):
        self.backend = _FakeBackend()

    @staticmethod
    def parse_response(response):
        return response


class _FakeClient:
    def __init__(self):
        self.responses = [
            {
                "stop_reason": "tool_use",
                "content": [
                    {
                        "type": "tool_use",
                        "id": "u1",
                        "name": "list_directory",
                        "input": {"path": "."},
                    }
                ],
                "usage": {"input_tokens": 10, "output_tokens": 2},
            },
            {
                "stop_reason": "end_turn",
                "content": [{"type": "text", "text": "Dateien gefunden."}],
                "usage": {"input_tokens": 11, "output_tokens": 5},
            },
        ]

    def call(self, **kwargs):
        return self.responses.pop(0)


class AgentLoggerTests(unittest.TestCase):
    def test_agent_emits_logger_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            logger = Logger(session_id="sess-a", dir=Path(tmp))
            ctx = Context(task=Player, system="sys")
            agent = Agent(
                context=ctx,
                registry=_FakeRegistry(),
                builder=_FakeBuilder(),
                client=_FakeClient(),
                logger=logger,
                max_iterations=5,
            )

            text = agent.run("Liste Dateien")
            self.assertEqual(text, "Dateien gefunden.")
            logger.close()

            log_file = Path(tmp) / "sess-a" / "events.jsonl"
            events = [json.loads(x) for x in log_file.read_text(encoding="utf-8").splitlines()]
            typs = [e["typ"] for e in events]

            self.assertIn("iteration", typs)
            self.assertIn("prompt", typs)
            self.assertIn("tool_call", typs)
            self.assertIn("tool_result", typs)
            self.assertIn("response", typs)
            self.assertIn("turn_end", typs)


if __name__ == "__main__":
    unittest.main()

