from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from secrets import token_hex
from typing import Any


class Logger:
    """Schreibt strukturierte JSONL-Events im log_viz-kompatiblen Format."""

    def __init__(
        self,
        *,
        session_id: str | None = None,
        dir: Path | None = None,
        log: Path | None = None,
        snapshot: dict[str, Any] | None = None,
    ) -> None:
        self.session_id = session_id or self._new_session_id()
        self.root_dir = dir or self._default_logs_dir()
        self.session_dir = self.root_dir / self.session_id
        self.session_dir.mkdir(parents=True, exist_ok=True)

        self.path = log or (self.session_dir / "events.jsonl")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")

        event: dict[str, Any] = {}
        if snapshot is not None:
            event["snapshot"] = snapshot
        self._write("session_start", event)

    def close(self) -> None:
        if not self._fh.closed:
            self._fh.close()

    def iteration(self, n: int, max: int) -> None:  # noqa: A002
        self._write("iteration", {"n": n, "max": max})

    def prompt(self, messages: list[Any], tools: dict[str, Any]) -> None:
        self._write(
            "prompt",
            {
                "message_count": len(messages),
                "messages": [m.role for m in messages],
                "tool_count": len(tools),
                "tools": list(tools.keys()),
            },
        )

    def response(
        self,
        *,
        text: str,
        usage: dict[str, Any] | None,
        stop_reason: str,
        task: str,
        backend: Any,
    ) -> dict[str, Any]:
        token_meta = self._extract_tokens(usage or {})
        cost = backend.estimate_cost(
            input_tokens=token_meta["input_tokens"],
            output_tokens=token_meta["output_tokens"],
        )

        event = {
            "text": text,
            "stop_reason": stop_reason,
            "task": task,
            "provider": backend.__class__.__name__.lower(),
            "model": backend.model,
            "usage_unit": backend.usage_unit,
            "usage_level": backend.usage_level,
            "usage": usage or {},
            "input_tokens": token_meta["input_tokens"],
            "output_tokens": token_meta["output_tokens"],
            "cost_usd": cost,
        }
        self._write("response", event)
        return token_meta

    def tool_call(self, name: str, args: dict[str, Any]) -> None:
        self._write("tool_call", {"name": name, "args": args})

    def tool_result(self, *, name: str, result: str, ok: bool, error: str | None = None) -> None:
        self._write(
            "tool_result",
            {
                "name": name,
                "result": result,
                "ok": ok,
                "error": error,
            },
        )

    def raw(self, data: dict[str, Any]) -> None:
        self._write("raw", {"data": data})

    def limit_reached(self, *, kind: str, n: int, max: int) -> None:  # noqa: A002
        self._write("limit_reached", {"kind": kind, "n": n, "max": max})

    def turn_end(self, *, reason: str, iterations: int, tokens: dict[str, Any]) -> None:
        self._write(
            "turn_end",
            {
                "reason": reason,
                "iterations": iterations,
                "tokens": tokens,
            },
        )

    def _write(self, typ: str, payload: dict[str, Any]) -> None:
        event = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "session": self.session_id,
            "typ": typ,
            **payload,
        }
        self._fh.write(json.dumps(event, ensure_ascii=False) + "\n")
        self._fh.flush()

    @staticmethod
    def _default_logs_dir() -> Path:
        root = Path(os.environ.get("BOUKENSHA_DIR", str(Path.home() / ".boukensha")))
        return root / "logs"

    @staticmethod
    def _new_session_id() -> str:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return f"{ts}-{token_hex(4)}"

    @staticmethod
    def _extract_tokens(usage: dict[str, Any]) -> dict[str, int]:
        input_tokens = int(
            usage.get("input_tokens")
            or usage.get("prompt_tokens")
            or usage.get("promptTokenCount")
            or usage.get("prompt_eval_count")
            or 0
        )
        output_tokens = int(
            usage.get("output_tokens")
            or usage.get("completion_tokens")
            or usage.get("candidatesTokenCount")
            or usage.get("eval_count")
            or 0
        )
        return {"input_tokens": input_tokens, "output_tokens": output_tokens}

