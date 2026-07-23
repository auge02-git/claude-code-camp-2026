from __future__ import annotations

from .base import Base


class Gemini(Base):
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    MODELS = {
        "gemini-3.5-flash": {
            "context_window": 1_048_576,
            "cost_per_million": {"input": 1.5, "output": 9.0},
            "usage_unit": "tokens",
        },
        "gemini-3.1-flash-lite": {
            "context_window": 1_048_576,
            "cost_per_million": {"input": 0.25, "output": 1.5},
            "usage_unit": "tokens",
        },
        "gemini-2.5-pro": {
            "context_window": 1_048_576,
            "cost_per_million": {"input": 1.25, "output": 10.0},
            "usage_unit": "tokens",
        },
        "gemini-2.5-flash": {
            "context_window": 1_048_576,
            "cost_per_million": {"input": 0.30, "output": 2.50},
            "usage_unit": "tokens",
        },
        "gemini-2.5-flash-lite": {
            "context_window": 1_048_576,
            "cost_per_million": {"input": 0.10, "output": 0.40},
            "usage_unit": "tokens",
        },
    }

    def __init__(self, *, api_key: str, model: str) -> None:
        super().__init__()
        self._api_key = api_key
        self.configure_model(model)

    def to_messages(self, messages):
        out = []
        for msg in messages:
            if msg.role == "assistant":
                out.append({"role": "model", "parts": self._assistant_parts(msg.content)})
            elif msg.role == "tool_result":
                out.append(
                    {
                        "role": "user",
                        "parts": [
                            {
                                "functionResponse": {
                                    "name": msg.tool_use_id,
                                    "response": {"content": msg.content},
                                }
                            }
                        ],
                    }
                )
            else:
                out.append({"role": str(msg.role), "parts": [{"text": msg.content}]})
        return out

    def to_tools(self, tools):
        if not tools:
            return []

        return [
            {
                "functionDeclarations": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            "type": "object",
                            "properties": tool.parameters,
                            "required": [str(key) for key in tool.parameters.keys()],
                        },
                    }
                    for tool in tools.values()
                ]
            }
        ]

    def to_payload(self, context, *, max_output_tokens: int = 1024, tools=None):
        return {
            "systemInstruction": {"parts": [{"text": context.system}]},
            "contents": self.to_messages(context.messages),
            "tools": self.to_tools(context.tools) if tools is None else tools,
            "generationConfig": {"maxOutputTokens": max_output_tokens},
        }

    def headers(self):
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": self._api_key,
        }

    def url(self):
        return f"{self.BASE_URL}/{self.model}:generateContent"

    def parse_response(self, response):
        parts = (((response.get("candidates") or [{}])[0]).get("content") or {}).get("parts") or []
        content = []
        tool_used = False

        for part in parts:
            if "functionCall" in part:
                fc = part.get("functionCall") or {}
                content.append(
                    {
                        "type": "tool_use",
                        "id": fc.get("name"),
                        "name": fc.get("name"),
                        "input": fc.get("args") or {},
                    }
                )
                tool_used = True
            elif "text" in part:
                content.append({"type": "text", "text": part.get("text", "")})

        return {"stop_reason": "tool_use" if tool_used else "end_turn", "content": content}

    def _assistant_parts(self, content):
        blocks = content if isinstance(content, list) else [{"type": "text", "text": str(content)}]
        parts = []
        for block in blocks:
            if block.get("type") == "tool_use":
                parts.append(
                    {
                        "functionCall": {
                            "name": block.get("name"),
                            "args": block.get("input") or {},
                        }
                    }
                )
            else:
                parts.append({"text": block.get("text", "")})
        return parts

