from __future__ import annotations

from .errors import ApiError
from .logger import Logger


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
        logger: Logger | None = None,
        task_settings: dict | None = None,
        max_iterations: int | None = None,
        max_output_tokens: int | None = None,
    ) -> None:
        self._context = context
        self._registry = registry
        self._builder = builder
        self._client = client
        self._logger = logger or Logger()
        self._max_iterations = self._resolve_max_iterations(task_settings, max_iterations)
        self._max_output_tokens = self._resolve_max_output_tokens(task_settings, max_output_tokens)
        self._iteration = 0

    def run(self, user_input: str) -> str:
        self._logger.turn(1)
        self._context.add_message("user", user_input)

        while True:
            if self._iteration_limit_reached():
                self._logger.limit_reached(kind="max_iterations", n=self._iteration, max=self._max_iterations)
                return self._wrap_up("max_iterations")

            self._iteration += 1
            self._logger.iteration(self._iteration, self._max_iterations)
            self._logger.prompt(self._context.messages, self._context.tools)
            response = self._client.call(**self._call_opts())
            self._logger.raw(response)
            parsed = self._builder.parse_response(response)

            if parsed["stop_reason"] == "tool_use":
                self._handle_tool_calls(parsed["content"])
                continue

            text = self._extract_text(parsed["content"])
            tokens = self._logger.response(
                text=text,
                usage=self._extract_usage(response),
                stop_reason=parsed["stop_reason"],
                task=self._context.task.task_name(),
                backend=self._builder.backend,
            )
            self._logger.turn_end(reason="completed", iterations=self._iteration, tokens=tokens)
            return text

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
            self._logger.raw(response)
            parsed = self._builder.parse_response(response)
            text = self._extract_text(parsed["content"]).strip()
            final = text if text else self._fallback_message(reason)
            tokens = self._logger.response(
                text=final,
                usage=self._extract_usage(response),
                stop_reason=parsed["stop_reason"],
                task=self._context.task.task_name(),
                backend=self._builder.backend,
            )
            self._logger.turn_end(reason=reason, iterations=self._iteration, tokens=tokens)
            return final
        except ApiError:
            final = self._fallback_message(reason)
            self._logger.response(
                text=final,
                usage={},
                stop_reason="end_turn",
                task=self._context.task.task_name(),
                backend=self._builder.backend,
            )
            self._logger.turn_end(reason=reason, iterations=self._iteration, tokens={"input_tokens": 0, "output_tokens": 0})
            return final

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
            self._logger.tool_call(name, args)
            try:
                result = self._registry.dispatch(name, args)
                result_text = str(result)
                self._logger.tool_result(name=name, result=result_text, ok=True)
            except Exception as exc:  # noqa: BLE001
                result_text = f"ERROR: {exc.__class__.__name__}: {exc}"
                self._logger.tool_result(name=name, result=result_text, ok=False, error=str(exc))
            self._context.add_message("tool_result", result_text, tool_use_id=use_id)

    @staticmethod
    def _extract_usage(response: dict) -> dict:
        if "usage" in response and isinstance(response["usage"], dict):
            return response["usage"]
        return response.get("usageMetadata") or {}

