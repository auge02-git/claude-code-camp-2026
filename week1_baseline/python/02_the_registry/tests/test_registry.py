from __future__ import annotations

import sys
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha import Context, Player, Registry, UnknownToolError


class ToolRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context(task=Player, system="Test system")
        self.registry = Registry(self.ctx)

    def test_tool_decorator_registration(self) -> None:
        @self.registry.tool("test", description="Test tool")
        def test_func() -> str:
            return "works"

        self.assertEqual(len(self.ctx.tools), 1)
        self.assertIn("test", self.ctx.tools)

    def test_dispatch_successful(self) -> None:
        @self.registry.tool("greet", description="Greet someone",
                            parameters={"name": {"type": "string"}})
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        result = self.registry.dispatch("greet", {"name": "Alice"})
        self.assertEqual(result, "Hello, Alice!")

    def test_dispatch_unknown_tool_error(self) -> None:
        with self.assertRaises(UnknownToolError):
            self.registry.dispatch("unknown")

    def test_multiple_tools(self) -> None:
        @self.registry.tool("t1", description="Tool 1")
        def t1() -> str:
            return "t1"

        @self.registry.tool("t2", description="Tool 2")
        def t2() -> str:
            return "t2"

        self.assertEqual(len(self.ctx.tools), 2)


if __name__ == "__main__":
    unittest.main()

