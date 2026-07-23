from __future__ import annotations


class RunDSL:
    """Kleine DSL-Fassade, die nur Tool-Registrierung exponiert."""

    def __init__(self, registry) -> None:
        self._registry = registry

    def tool(self, name: str, *, description: str, parameters: dict | None = None):
        return self._registry.tool(name, description=description, parameters=parameters)

