from __future__ import annotations

from typing import Any, ClassVar

from ..errors import UnsupportedModelError


class Base:
    MODELS: ClassVar[dict[str, dict[str, Any]] | None] = None

    def __init__(self) -> None:
        self._model = ""
        self._model_info: dict[str, Any] = {}

    @classmethod
    def models(cls) -> dict[str, dict[str, Any]]:
        if cls.MODELS is None:
            raise NotImplementedError(f"{cls.__name__} must define MODELS")
        return cls.MODELS

    @classmethod
    def model_info_for(cls, model: str) -> dict[str, Any] | None:
        return cls.models().get(str(model))

    @classmethod
    def validate_model(cls, model: str) -> str:
        model_str = str(model)
        if cls.model_info_for(model_str):
            return model_str

        supported = ", ".join(sorted(cls.models().keys()))
        raise UnsupportedModelError(
            f"{cls.__name__} does not support model {model_str!r}. Supported models: {supported}"
        )

    @property
    def model(self) -> str:
        return self._model

    @property
    def model_info(self) -> dict[str, Any]:
        return self._model_info

    @property
    def context_window(self) -> int:
        return int(self.model_info["context_window"])

    @property
    def input_token_cost_per_million(self) -> float | None:
        return self.model_info["cost_per_million"]["input"]

    @property
    def output_token_cost_per_million(self) -> float | None:
        return self.model_info["cost_per_million"]["output"]

    @property
    def usage_unit(self) -> str:
        return str(self.model_info["usage_unit"])

    @property
    def usage_level(self) -> str | None:
        level = self.model_info.get("usage_level")
        return str(level) if level is not None else None

    def estimate_cost(self, *, input_tokens: int, output_tokens: int) -> float | None:
        input_cost = self.input_token_cost_per_million
        output_cost = self.output_token_cost_per_million
        if input_cost is None or output_cost is None:
            return None

        return ((input_tokens * input_cost) + (output_tokens * output_cost)) / 1_000_000.0

    def configure_model(self, model: str) -> None:
        self._model = self.validate_model(model)
        info = self.model_info_for(self._model)
        self._model_info = info or {}

