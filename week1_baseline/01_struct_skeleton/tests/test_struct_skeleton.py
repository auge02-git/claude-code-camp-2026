from __future__ import annotations
import sys
import unittest
from pathlib import Path
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))
from boukensha import Config, Context, Message, Player, Tool
class StructSkeletonTests(unittest.TestCase):
    def test_tool_creation(self) -> None:
        tool = Tool(
            "move",
            "Move the player in a direction (north, south, east, west, up, down)",
            {"direction": {"type": "string"}},
            lambda d: f"Moved {d}",
        )
        self.assertEqual(tool.name, "move")
        self.assertEqual(tool.parameters["direction"]["type"], "string")
        self.assertTrue(callable(tool.block))
        self.assertEqual(tool.block("north"), "Moved north")
    def test_tool_repr_truncates_description(self) -> None:
        long_desc = "A" * 100
        tool = Tool("test", long_desc, {}, lambda: None)
        repr_str = repr(tool)
        self.assertIn("A" * 41, repr_str)
        self.assertNotIn("A" * 50, repr_str)
    def test_message_creation(self) -> None:
        msg = Message("user", "Hello, agent!")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.content, "Hello, agent!")
        self.assertIsNone(msg.tool_use_id)
    def test_message_with_tool_use_id(self) -> None:
        msg = Message("tool_result", "Result text", tool_use_id="tool_123")
        self.assertEqual(msg.tool_use_id, "tool_123")
        self.assertIn("[tool_123]", repr(msg))
    def test_message_repr_truncates_content(self) -> None:
        long_content = "B" * 100
        msg = Message("user", long_content)
        repr_str = repr(msg)
        self.assertIn("B" * 61, repr_str)
        self.assertNotIn("B" * 80, repr_str)
        self.assertIn("...", repr_str)
    def test_context_creation(self) -> None:
        ctx = Context(task=Player, system="You are a helpful assistant.")
        self.assertEqual(ctx.task, Player)
        self.assertEqual(ctx.system, "You are a helpful assistant.")
        self.assertEqual(ctx.turn_count, 0)
        self.assertEqual(ctx.tool_count, 0)
    def test_context_register_tool(self) -> None:
        ctx = Context(task=Player)
        tool = Tool("test", "Test tool", {}, lambda: None)
        ctx.register_tool(tool)
        self.assertEqual(ctx.tool_count, 1)
        self.assertIn("test", ctx.tools)
        self.assertEqual(ctx.tools["test"], tool)
    def test_context_add_message(self) -> None:
        ctx = Context(task=Player)
        ctx.add_message("user", "Hello")
        ctx.add_message("assistant", "Hi there")
        self.assertEqual(ctx.turn_count, 2)
        self.assertEqual(ctx.messages[0].role, "user")
        self.assertEqual(ctx.messages[1].role, "assistant")
    def test_context_repr(self) -> None:
        ctx = Context(task=Player)
        ctx.add_message("user", "Test")
        tool = Tool("test", "Test", {}, lambda: None)
        ctx.register_tool(tool)
        repr_str = repr(ctx)
        self.assertIn("player", repr_str)
        self.assertIn("turns=1", repr_str)
        self.assertIn("tools=1", repr_str)
if __name__ == "__main__":
    unittest.main()
