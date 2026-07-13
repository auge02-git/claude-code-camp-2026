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

from mud_mcp.session import (  # wiederverwendet, unverändert
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
    MudSession,
)

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_NAME_PROMPT = re.compile(r"By what name do you wish to be known.*\?", re.I)
_PASSWORD_PROMPT = re.compile(r"[Pp]assword")
_RECONNECT = re.compile(r"Reconnecting", re.I)
_WRONG_PW = re.compile(r"Wrong password", re.I)
_MENU = re.compile(r"Make your choice|Enter the game", re.I)
_PRESS_RETURN = re.compile(r"PRESS RETURN|\[ Return to continue", re.I)
# Spiel-Prompt der Form "25H 100M 83V ... >" signalisiert: wir sind in der Welt.
_GAME_PROMPT = re.compile(r"\d+H\s+\d+M\s+\d+V.*>")


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
        """Robuster Login — ohne Argumente via ``credentials.json`` (mud-mcp).

        Nutzt die (unveränderten) ``MudSession``-Primitiven und behandelt BEIDE
        Fälle, an denen die schlichte ``session.login()`` scheitert:
        - **Reconnecting** (Charakter war link-dead) → sofort in der Welt, und
        - **sauberer Login** (frisch ausgeloggt) → erst MOTD/„PRESS RETURN" und
          das Hauptmenü („1) Enter the game"), das quittiert werden muss.
        """
        s = self._session
        assert s is not None, "vor login zuerst connect() aufrufen"
        user = username or DEFAULT_USERNAME
        pw = password or DEFAULT_PASSWORD

        # Namens-Prompt kann von connect() schon konsumiert sein → tolerant warten.
        try:
            s.read_until(_NAME_PROMPT, timeout=2.0)
        except Exception:
            pass
        s.send_command(user)
        s.read_until(_PASSWORD_PROMPT, timeout=8.0)
        s.send_command(pw)

        # Post-Passwort-Ablauf abarbeiten (Reconnect | MOTD/Menü), begrenzt.
        transcript = ""
        for _ in range(8):
            out = s.read_until_quiet(quiet_seconds=1.0, timeout=8.0)
            transcript += out
            if _WRONG_PW.search(out):
                raise RuntimeError("Login fehlgeschlagen: falsches Passwort")
            if _RECONNECT.search(out) or _GAME_PROMPT.search(out):
                break  # in der Welt
            if _MENU.search(out):
                s.send_command("1")  # Spiel betreten
                continue
            if _PRESS_RETURN.search(out) or out.rstrip().endswith(":"):
                s.send_command("")  # MOTD/Return-Gate wegklicken
                continue
            if not out.strip():
                break  # nichts mehr → fertig
            s.send_command("")  # Unbekanntes: mit Return weiterschalten
        return _clean(transcript)

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
