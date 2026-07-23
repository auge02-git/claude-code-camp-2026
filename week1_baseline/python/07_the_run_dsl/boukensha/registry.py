from __future__ import annotations

from typing import Any, Callable

from .context import Context
from .errors import UnknownToolError
from .tool import Tool


class Registry:
    """Verwaltet Werkzeuge und dispatcht deren Aufrufe."""

    def __init__(self, context: Context) -> None:
        self._context = context

    def tool(
        self,
        name: str,
        *,
        description: str,
        parameters: dict[str, Any] | None = None,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        if parameters is None:
            parameters = {}

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            tool_instance = Tool(name, description, parameters, func)
            self._context.register_tool(tool_instance)
            return func

        return decorator

    def dispatch(self, name: str, args: dict[str, Any] | None = None) -> Any:
        if args is None:
            args = {}

        tool = self._context.tools.get(name)
        if not tool:
            raise UnknownToolError(f"No tool registered as '{name}'")

        return tool.block(**args)

