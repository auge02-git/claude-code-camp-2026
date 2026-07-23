from __future__ import annotations

import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha.backends.anthropic import Anthropic
from boukensha.backends.lmstudio import LMStudio
from boukensha.backends.ollama import Ollama
from boukensha.backends.ollama_cloud import OllamaCloud
from boukensha.backends.openai import OpenAI
from boukensha.config import Config, PROMPTS_DIR
from boukensha.context import Context
from boukensha.errors import UnsupportedModelError
from boukensha.prompt_builder import PromptBuilder
from boukensha.registry import Registry
from boukensha.tasks.player import Player


class PromptBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.boukensha_dir = Path(self.temp_dir.name) / ".boukensha"
        self.boukensha_dir.mkdir(parents=True, exist_ok=True)

        settings = textwrap.dedent(
            """
            tasks:
              player:
                provider: anthropic
                model: claude-haiku-4-5
                prompt_override:
                  system: false
            mud:
              host: localhost
              port: 4000
            """
        ).strip()
        (self.boukensha_dir / "settings.yml").write_text(settings + "\n", encoding="utf-8")

    def _build_context(self) -> Context:
        config = Config(directory=self.boukensha_dir)
        player_settings = config.tasks("player")
        system_prompt = Player.system_prompt(
            player_settings,
            user_prompts_dir=config.user_prompts_dir,
            default_prompts_dir=PROMPTS_DIR,
        )

        ctx = Context(task=Player, system=system_prompt)
        registry = Registry(ctx)

        @registry.tool("look", description="Look around", parameters={})
        def look() -> str:
            return "A dark room"

        @registry.tool(
            "move",
            description="Move in direction",
            parameters={"direction": {"type": "string"}},
        )
        def move(direction: str) -> str:
            return f"Move {direction}"

        ctx.add_message("user", "Look around")
        ctx.add_message("assistant", "I will look")
        ctx.add_message("tool_result", "A dark room", tool_use_id="toolu_1")
        return ctx

    def test_anthropic_payload_shape(self) -> None:
        ctx = self._build_context()
        backend = Anthropic(api_key="k", model="claude-haiku-4-5")

        payload = backend.to_payload(ctx, max_output_tokens=123)
        self.assertEqual(payload["model"], "claude-haiku-4-5")
        self.assertEqual(payload["max_tokens"], 123)
        self.assertEqual(payload["messages"][2]["role"], "user")
        self.assertEqual(payload["messages"][2]["content"][0]["type"], "tool_result")

    def test_openai_payload_shape(self) -> None:
        ctx = self._build_context()
        backend = OpenAI(api_key="k", model="gpt-5.4-mini")

        payload = backend.to_payload(ctx)
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertEqual(payload["messages"][3]["role"], "tool")
        self.assertEqual(payload["messages"][3]["tool_call_id"], "toolu_1")

    def test_lmstudio_payload_shape(self) -> None:
        ctx = self._build_context()
        backend = LMStudio(model="google/gemma-4-12b-qat")

        payload = backend.to_payload(ctx, max_output_tokens=777)
        self.assertEqual(payload["model"], "google/gemma-4-12b-qat")
        self.assertEqual(payload["max_tokens"], 777)
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertEqual(payload["messages"][3]["role"], "tool")
        self.assertEqual(payload["messages"][3]["tool_call_id"], "toolu_1")
        self.assertEqual(backend.url(), "http://localhost:1234/v1/chat/completions")

    def test_prompt_builder_delegates_to_backend(self) -> None:
        ctx = self._build_context()
        backend = Anthropic(api_key="k", model="claude-haiku-4-5")
        builder = PromptBuilder(ctx, backend)

        self.assertEqual(builder.url(), "https://api.anthropic.com/v1/messages")
        self.assertIn("x-api-key", builder.headers())
        self.assertIn("messages", builder.to_api_payload())

    def test_unsupported_model_raises(self) -> None:
        with self.assertRaises(UnsupportedModelError):
            Anthropic(api_key="k", model="not-a-model")

    def test_cost_estimation_and_usage_units(self) -> None:
        ollama = Ollama(model="qwen3:8b")
        self.assertEqual(ollama.estimate_cost(input_tokens=1000, output_tokens=1000), 0.0)
        self.assertEqual(ollama.usage_unit, "local_compute")

        cloud = OllamaCloud(api_key="k", model="gemma4:31b-cloud")
        self.assertIsNone(cloud.estimate_cost(input_tokens=1000, output_tokens=1000))
        self.assertEqual(cloud.usage_unit, "ollama_cloud_usage")


if __name__ == "__main__":
    unittest.main()

