from __future__ import annotations

import json

from .base import Base


class LMStudio(Base):
    """OpenAI-kompatibles Backend fuer lokale LM Studio Server."""

    MODELS = {
        "google/gemma-4-12b-qat": {
            "context_window": 128_000,
            "cost_per_million": {"input": 0.0, "output": 0.0},
            "usage_unit": "local_compute",
        }
    }

    def __init__(self, *, model: str, base_url: str = "http://localhost:1234") -> None:
        super().__init__()
        self._base_url = base_url.rstrip("/")
        self.configure_model(model)

    def to_messages(self, system, messages):
        system_message = [{"role": "system", "content": system}]
        conversation = []
        for msg in messages:
            if msg.role == "tool_result":
                conversation.append(
                    {"role": "tool", "tool_call_id": msg.tool_use_id, "content": msg.content}
                )
            elif msg.role == "assistant":
                conversation.append(self._assistant_message(msg.content))
            else:
                conversation.append({"role": str(msg.role), "content": msg.content})
        return system_message + conversation

    def to_tools(self, tools):
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": tool.parameters,
                        "required": [str(key) for key in tool.parameters.keys()],
                    },
                },
            }
            for tool in tools.values()
        ]

    def to_payload(self, context, *, max_output_tokens: int = 1024, tools=None):
        return {
            "model": self.model,
            "messages": self.to_messages(context.system, context.messages),
            "tools": self.to_tools(context.tools) if tools is None else tools,
            "max_tokens": max_output_tokens,
        }

    def headers(self):
        return {"Content-Type": "application/json"}

    def url(self):
        return f"{self._base_url}/v1/chat/completions"

    def parse_response(self, response):
        message = ((response.get("choices") or [{}])[0]).get("message") or {}
        tool_calls = message.get("tool_calls") or []

        content = []
        if message.get("content"):
            content.append({"type": "text", "text": message["content"]})

        for call in tool_calls:
            function = call.get("function") or {}
            args_json = function.get("arguments") or "{}"
            try:
                args = json.loads(args_json)
            except json.JSONDecodeError:
                args = {}
            content.append(
                {
                    "type": "tool_use",
                    "id": call.get("id"),
                    "name": function.get("name"),
                    "input": args,
                }
            )

        return {"stop_reason": "tool_use" if tool_calls else "end_turn", "content": content}

    def _assistant_message(self, content):
        blocks = content if isinstance(content, list) else [{"type": "text", "text": str(content)}]
        text_blocks = [b for b in blocks if b.get("type") == "text"]
        tool_blocks = [b for b in blocks if b.get("type") == "tool_use"]

        message = {"role": "assistant", "content": "".join(b.get("text", "") for b in text_blocks)}
        if tool_blocks:
            message["tool_calls"] = [
                {
                    "id": b.get("id"),
                    "type": "function",
                    "function": {
                        "name": b.get("name"),
                        "arguments": json.dumps(b.get("input") or {}),
                    },
                }
                for b in tool_blocks
            ]
        return message

