from __future__ import annotations

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

    def to_payload(self, context, *, max_output_tokens: int = 1024):
        return {
            "model": self.model,
            "messages": self.to_messages(context.system, context.messages),
            "tools": self.to_tools(context.tools),
            "max_tokens": max_output_tokens,
        }

    def headers(self):
        return {"Content-Type": "application/json"}

    def url(self):
        return f"{self._base_url}/v1/chat/completions"

