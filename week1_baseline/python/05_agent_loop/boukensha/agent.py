from __future__ import annotations

from .errors import ApiError


class Agent:
    MAX_ITERATIONS = 25
    WRAP_UP_OUTPUT_TOKENS = 400
    WRAP_UP_DIRECTIVE = (
        "You have reached your action limit for this turn. Do not call any more tools.\n"
        "Briefly summarize what you accomplished, what is still unfinished, and the\n"
        "single next action you would take."
    )

    def __init__(
        self,
        *,
        context,
        registry,
        builder,
        client,
        task_settings: dict | None = None,
        max_iterations: int | None = None,
        max_output_tokens: int | None = None,
    ) -> None:
        self._context = context
        self._registry = registry
        self._builder = builder
        self._client = client
        self._max_iterations = self._resolve_max_iterations(task_settings, max_iterations)
        self._max_output_tokens = self._resolve_max_output_tokens(task_settings, max_output_tokens)
        self._iteration = 0

    def run(self, user_input: str) -> str:
        self._context.add_message("user", user_input)

        while True:
            if self._iteration_limit_reached():
                return self._wrap_up("max_iterations")

            self._iteration += 1
            response = self._client.call(**self._call_opts())
            parsed = self._builder.parse_response(response)

            if parsed["stop_reason"] == "tool_use":
                self._handle_tool_calls(parsed["content"])
                continue

            return self._extract_text(parsed["content"])

    def _resolve_max_iterations(self, task_settings: dict | None, explicit: int | None) -> int:
        if explicit is not None:
            return int(explicit)
        if task_settings and hasattr(self._context.task, "max_iterations"):
            return int(self._context.task.max_iterations(task_settings))
        return self.MAX_ITERATIONS

    def _resolve_max_output_tokens(self, task_settings: dict | None, explicit: int | None) -> int | None:
        if explicit is not None:
            return int(explicit)
        if task_settings and hasattr(self._context.task, "max_output_tokens"):
            return self._context.task.max_output_tokens(task_settings)
        return None

    def _iteration_limit_reached(self) -> bool:
        return self._max_iterations > 0 and self._iteration >= self._max_iterations

    def _call_opts(self) -> dict:
        return {"max_output_tokens": self._max_output_tokens} if self._max_output_tokens else {}

    def _wrap_up(self, reason: str) -> str:
        self._context.add_message("user", self.WRAP_UP_DIRECTIVE)
        try:
            response = self._client.call(tools=[], max_output_tokens=self.WRAP_UP_OUTPUT_TOKENS)
            parsed = self._builder.parse_response(response)
            text = self._extract_text(parsed["content"]).strip()
            return text if text else self._fallback_message(reason)
        except ApiError:
            return self._fallback_message(reason)

    def _fallback_message(self, reason: str) -> str:
        return (
            f"I reached my {self._max_iterations}-action limit for this turn before finishing "
            f"({reason}). Ask me to continue and I'll pick up from here."
        )

    def _extract_text(self, content: list[dict]) -> str:
        return "".join(block.get("text", "") for block in content if block.get("type") == "text")

    def _handle_tool_calls(self, content: list[dict]) -> None:
        self._context.add_message("assistant", content)

        for block in content:
            if block.get("type") != "tool_use":
                continue

            name = block.get("name")
            args = block.get("input") or {}
            use_id = block.get("id")
            result = self._registry.dispatch(name, args)
            self._context.add_message("tool_result", str(result), tool_use_id=use_id)

