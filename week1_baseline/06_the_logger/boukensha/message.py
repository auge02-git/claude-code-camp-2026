from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    """Eine Nachricht in der Konversation."""

    role: str
    content: str | list[dict[str, Any]]
    tool_use_id: str | None = None

    def __repr__(self) -> str:
        id_tag = f" [{self.tool_use_id}]" if self.tool_use_id else ""
        text = self.content if isinstance(self.content, str) else str(self.content)
        content_truncated = text[:61]
        return f"#<Message role={self.role}{id_tag} content={content_truncated}...>"

