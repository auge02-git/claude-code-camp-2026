"""MudManager (Diagramm-Knoten ``MudManager``) — dünner Wrapper.

**Wiederverwendung, keine Änderung:** Diese Klasse importiert die bestehende
``mud_mcp.session.MudSession`` (aus dem Paket ``mud-mcp``) und stellt sie dem
Agenten bereit. Die Datei ``mud-mcp/mud_mcp/session.py`` wird NICHT verändert.

Verhalten spiegelt den vorhandenen MCP-Server (``mud_mcp/server.py``):
- ``connect`` liest bis zum Namens-Prompt,
- ``login`` nutzt die Credentials aus ``credentials.json`` (Argumente optional),
- ``send`` wartet auf den ``> ``-Prompt (Fallback: Ruhefenster).
"""

from __future__ import annotations

import re

from mud_mcp.session import MudSession  # wiederverwendet, unverändert

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_NAME_PROMPT = re.compile(r"By what name do you wish to be known.*\?", re.I)


def _clean(text: str) -> str:
    """ANSI-Codes entfernen, Zeilenenden normalisieren (wie im MCP-Server)."""
    return _ANSI_RE.sub("", text).replace("\r\n", "\n").replace("\r", "")


class MudManager:
    """Verwaltet die Telnet-Sitzung zum tbaMUD (``telnet localhost 4000``)."""

    def __init__(self, host: str = "localhost", port: int = 4000) -> None:
        self.host = host
        self.port = port
        self._session: MudSession | None = None

    def connect(self) -> str:
        """Öffnet die Verbindung, liefert das Banner bis zum Namens-Prompt."""
        if self._session is not None and self._session.is_open:
            self._session.close()
        self._session = MudSession(host=self.host, port=self.port)
        self._session.open()
        try:
            banner = self._session.read_until(_NAME_PROMPT, timeout=10.0)
        except Exception:
            banner = self._session.drain()
        return _clean(banner)

    def login(self, username: str = "", password: str = "") -> str:
        """Loggt ein — ohne Argumente via ``credentials.json`` (mud-mcp)."""
        assert self._session is not None, "vor login zuerst connect() aufrufen"
        return _clean(self._session.login(username or None, password or None))

    def send(self, command: str, quiet_seconds: float = 1.0, timeout: float = 10.0) -> str:
        """Sendet ein Kommando und liefert die Antwort (bis zum ``> ``-Prompt)."""
        assert self._session is not None, "nicht verbunden"
        self._session.send_command(command)
        out = self._session.read_until_prompt(timeout=timeout)
        if not out.strip():
            out = self._session.read_until_quiet(quiet_seconds=quiet_seconds, timeout=timeout)
        return _clean(out)

    def read(self, quiet_seconds: float = 1.0, timeout: float = 5.0) -> str:
        """Liest anstehende Ausgabe (Kampfrunden, Ereignisse) ohne zu senden."""
        assert self._session is not None, "nicht verbunden"
        return _clean(self._session.read_until_quiet(quiet_seconds=quiet_seconds, timeout=timeout))

    @property
    def is_open(self) -> bool:
        return self._session is not None and self._session.is_open

    def close(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None
