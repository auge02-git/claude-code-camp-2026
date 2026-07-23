from __future__ import annotations


class UnknownToolError(Exception):
    """Wird geworfen, wenn ein unbekanntes Tool aufgerufen wird."""


class UnsupportedModelError(Exception):
    """Wird geworfen, wenn ein Modell fuer ein Backend nicht unterstuetzt ist."""


class ApiError(Exception):
    """Wird geworfen, wenn ein API-Request fehlschlaegt."""


