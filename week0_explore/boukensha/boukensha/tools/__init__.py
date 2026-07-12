"""Werkzeuge (Diagramm-Knoten ``tool.rb`` / „Tool Use").

Werkzeuge kapseln konkrete MUD-Aktionen und werden von der Agentic Loop über
die :class:`~boukensha.registry.ToolRegistry` aufgerufen.
"""

from __future__ import annotations

from .base import Tool
from .mud_tools import build_default_tools

__all__ = ["Tool", "build_default_tools"]
