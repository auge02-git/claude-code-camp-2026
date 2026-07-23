from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Tool:
    """Ein Werkzeug, das ein Agent aufrufen kann."""

    name: str
    description: str
    parameters: dict[str, Any]
    block: Callable[..., Any]

    def __repr__(self) -> str:
        desc_truncated = self.description[:41]
        params = list(self.parameters.keys())
        return f"#<Tool name={self.name} description={desc_truncated} params={params}>"

