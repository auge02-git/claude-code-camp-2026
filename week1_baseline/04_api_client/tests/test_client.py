from __future__ import annotations

import json
import os
import sys
import tempfile
import textwrap
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boukensha.backends.lmstudio import LMStudio
from boukensha.client import Client
from boukensha.config import Config, PROMPTS_DIR
from boukensha.context import Context
from boukensha.errors import ApiError
from boukensha.prompt_builder import PromptBuilder
from boukensha.registry import Registry
from boukensha.tasks.player import Player


class _QueueHandler(BaseHTTPRequestHandler):
    responses: list[tuple[int, dict]] = []

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        _ = self.rfile.read(length)
        status, payload = self.responses.pop(0)

        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):  # noqa: A003
        return


class ClientTests(unittest.TestCase):
    def _build_builder(self, base_url: str) -> PromptBuilder:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        boukensha_dir = Path(temp_dir.name) / ".boukensha"
        boukensha_dir.mkdir(parents=True, exist_ok=True)
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
        (boukensha_dir / "settings.yml").write_text(settings + "\n", encoding="utf-8")

        config = Config(directory=boukensha_dir)
        player_settings = config.tasks("player")
        system_prompt = Player.system_prompt(
            player_settings,
            user_prompts_dir=config.user_prompts_dir,
            default_prompts_dir=PROMPTS_DIR,
        )

        ctx = Context(task=Player, system=system_prompt)
        registry = Registry(ctx)

        @registry.tool("list_directory", description="List files", parameters={"path": {"type": "string"}})
        def list_directory(path: str) -> str:
            return path

        ctx.add_message("user", "List files")

        backend = LMStudio(model="google/gemma-4-12b-qat", base_url=base_url)
        return PromptBuilder(ctx, backend)

    def _start_server(self):
        server = HTTPServer(("127.0.0.1", 0), _QueueHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        return server

    def test_call_success(self) -> None:
        _QueueHandler.responses = [(200, {"ok": True, "id": "r1"})]
        server = self._start_server()
        builder = self._build_builder(f"http://127.0.0.1:{server.server_port}")
        client = Client(builder)

        response = client.call()
        self.assertTrue(response["ok"])

    def test_call_retries_retryable_status_then_success(self) -> None:
        _QueueHandler.responses = [
            (429, {"error": "rate"}),
            (200, {"ok": True}),
        ]
        server = self._start_server()
        builder = self._build_builder(f"http://127.0.0.1:{server.server_port}")
        client = Client(builder)

        response = client.call()
        self.assertEqual(response["ok"], True)

    def test_call_raises_api_error_on_persistent_failure(self) -> None:
        _QueueHandler.responses = [
            (500, {"error": "boom"}),
            (500, {"error": "boom"}),
            (500, {"error": "boom"}),
            (500, {"error": "boom"}),
        ]
        server = self._start_server()
        builder = self._build_builder(f"http://127.0.0.1:{server.server_port}")
        client = Client(builder)

        with self.assertRaises(ApiError):
            client.call()


if __name__ == "__main__":
    unittest.main()

