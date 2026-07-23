from __future__ import annotations

import sys
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha.agent import Agent
from boukensha.context import Context
from boukensha.errors import ApiError
from boukensha.tasks.player import Player


class FakeRegistry:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def dispatch(self, name: str, args: dict):
        self.calls.append((name, args))
        if name == "list_directory":
            return "README.md\nmain.py"
        return "ok"


class FakeBuilder:
    def parse_response(self, response):
        return response


class FakeClient:
    def __init__(self, responses: list[dict], fail_on_wrap_up: bool = False) -> None:
        self.responses = responses
        self.calls: list[dict] = []
        self.fail_on_wrap_up = fail_on_wrap_up

    def call(self, **kwargs):
        self.calls.append(kwargs)
        if kwargs.get("tools") == [] and self.fail_on_wrap_up:
            raise ApiError("wrap-up failed")
        return self.responses.pop(0)


class AgentLoopTests(unittest.TestCase):
    def test_tool_use_then_end_turn(self) -> None:
        ctx = Context(task=Player, system="sys")
        registry = FakeRegistry()
        builder = FakeBuilder()
        client = FakeClient(
            [
                {
                    "stop_reason": "tool_use",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "call_1",
                            "name": "list_directory",
                            "input": {"path": "."},
                        }
                    ],
                },
                {
                    "stop_reason": "end_turn",
                    "content": [{"type": "text", "text": "Found files in current directory."}],
                },
            ]
        )

        agent = Agent(
            context=ctx,
            registry=registry,
            builder=builder,
            client=client,
            max_iterations=5,
        )
        result = agent.run("Liste Dateien")

        self.assertEqual(result, "Found files in current directory.")
        self.assertEqual(registry.calls[0][0], "list_directory")
        self.assertEqual(ctx.messages[1].role, "assistant")
        self.assertEqual(ctx.messages[2].role, "tool_result")
        self.assertEqual(ctx.messages[2].tool_use_id, "call_1")

    def test_wrap_up_when_iteration_limit_hit(self) -> None:
        ctx = Context(task=Player, system="sys")
        registry = FakeRegistry()
        builder = FakeBuilder()
        client = FakeClient(
            [
                {
                    "stop_reason": "tool_use",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "call_1",
                            "name": "list_directory",
                            "input": {"path": "."},
                        }
                    ],
                },
                {
                    "stop_reason": "end_turn",
                    "content": [{"type": "text", "text": "Wrap-up summary."}],
                },
            ]
        )

        agent = Agent(
            context=ctx,
            registry=registry,
            builder=builder,
            client=client,
            max_iterations=1,
        )
        result = agent.run("Liste Dateien")

        self.assertEqual(result, "Wrap-up summary.")
        self.assertEqual(client.calls[-1]["tools"], [])
        self.assertEqual(client.calls[-1]["max_output_tokens"], 400)

    def test_wrap_up_fallback_on_api_error(self) -> None:
        ctx = Context(task=Player, system="sys")
        registry = FakeRegistry()
        builder = FakeBuilder()
        client = FakeClient(
            [
                {
                    "stop_reason": "tool_use",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "call_1",
                            "name": "list_directory",
                            "input": {"path": "."},
                        }
                    ],
                }
            ],
            fail_on_wrap_up=True,
        )

        agent = Agent(
            context=ctx,
            registry=registry,
            builder=builder,
            client=client,
            max_iterations=1,
        )
        result = agent.run("Liste Dateien")

        self.assertIn("limit", result)
        self.assertIn("continue", result)


if __name__ == "__main__":
    unittest.main()

