from __future__ import annotations

from .context import Context


class PromptBuilder:
    """Delegiert Context-Serialisierung an ein konkretes Backend."""

    def __init__(self, context: Context, backend: object) -> None:
        self._context = context
        self._backend = backend

    @property
    def backend(self):
        return self._backend

    def to_messages(self):
        return self._backend.to_messages(self._context.messages)

    def to_tools(self):
        return self._backend.to_tools(self._context.tools)

    def to_api_payload(self, *, max_output_tokens: int = 1024, tools=None):
        return self._backend.to_payload(
            self._context,
            max_output_tokens=max_output_tokens,
            tools=tools,
        )

    def parse_response(self, response):
        return self._backend.parse_response(response)

    def headers(self):
        return self._backend.headers()

    def url(self):
        return self._backend.url()

