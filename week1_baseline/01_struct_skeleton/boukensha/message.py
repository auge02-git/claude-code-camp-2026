from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Message:
    """Eine Nachricht in der Konversation."""

    role: str
    content: str
    tool_use_id: str | None = None

    def __repr__(self) -> str:
        id_tag = f" [{self.tool_use_id}]" if self.tool_use_id else ""
        content_truncated = self.content[:61]
        return f"#<Message role={self.role}{id_tag} content={content_truncated}...>"

