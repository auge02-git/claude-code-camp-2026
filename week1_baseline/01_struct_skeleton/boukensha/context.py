from __future__ import annotations

from typing import Any

from .message import Message
from .tool import Tool


class Context:
    """Zentrale Container fuer alle API-Call-Daten."""

    def __init__(self, task: type[Any], system: str | None = None) -> None:
        self.task = task
        self.system = system
        self.messages: list[Message] = []
        self.tools: dict[str, Tool] = {}

    def register_tool(self, tool: Tool) -> None:
        """Registriert ein Werkzeug im Kontext."""
        self.tools[tool.name] = tool

    def add_message(
        self,
        role: str,
        content: str,
        tool_use_id: str | None = None,
    ) -> None:
        """Fuegt eine Nachricht zur Gespraechi-Historie hinzu."""
        self.messages.append(Message(role, content, tool_use_id))

    @property
    def tool_count(self) -> int:
        """Anzahl registrierter Tools."""
        return len(self.tools)

    @property
    def turn_count(self) -> int:
        """Anzahl Nachrichten (Turns)."""
        return len(self.messages)

    def __repr__(self) -> str:
        task_name = self.task.task_name() if self.task else "unknown"
        return f"#<Context task={task_name} turns={self.turn_count} tools={self.tool_count}>"

