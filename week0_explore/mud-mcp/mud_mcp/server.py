"""FastMCP server: telnet control of the tbaMUD/CircleMUD server.

Exposes a single long-lived MUD session as MCP tools so an agent (or Claude
Code) can connect, log in, and drive the game one command at a time. Output is
returned verbatim (ANSI escape codes stripped) so the caller sees exactly what
a human at a telnet prompt would.

Transport is stdio (the default for Claude Code MCP servers). Do not print to
stdout anywhere except via the MCP protocol — it would corrupt the stream.
"""

from __future__ import annotations

import os
import re

from mcp.server.fastmcp import FastMCP

from .session import LoginError, MudSession, SessionError

mcp = FastMCP("mud")

# A single shared session — this server manages one telnet connection.
_session: MudSession | None = None

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _clean(text: str) -> str:
    """Strip ANSI escape codes and normalise line endings for readability."""
    return _ANSI_RE.sub("", text).replace("\r\n", "\n").replace("\r", "")


@mcp.tool()
def mud_connect(host: str = "localhost", port: int = 4000) -> str:
    """Open a telnet connection to the MUD and return the login banner.

    Defaults target the local Docker server (localhost:4000). Call this before
    any other tool. Reconnecting closes an existing session first.
    """
    global _session
    if _session is not None and _session.is_open:
        _session.close()
    _session = MudSession(host=host, port=port)
    try:
        _session.open()
    except SessionError as e:
        _session = None
        return f"ERROR: {e}"
    # The MUD spends a few seconds detecting the client before the banner
    # settles, so wait for the name prompt rather than a quiet window.
    try:
        banner = _session.read_until(
            re.compile(r"By what name do you wish to be known.*\?", re.I), timeout=10.0
        )
    except SessionError:
        banner = _session.drain()
    return _clean(banner) or "(connected; no banner received yet)"


@mcp.tool()
def mud_login(username: str, password: str) -> str:
    """Log an existing character into the world (username + password).

    Walks the CircleMUD login dance and enters the game. Creating a brand-new
    character is not supported here — do that once via `telnet localhost 4000`.
    Credentials may also come from MUD_NAME / MUD_PASSWORD env vars if omitted.
    """
    if _session is None or not _session.is_open:
        return "ERROR: not connected — call mud_connect first."
    username = username or os.environ.get("MUD_NAME", "")
    password = password or os.environ.get("MUD_PASSWORD", "")
    if not username or not password:
        return "ERROR: username and password required (or set MUD_NAME / MUD_PASSWORD)."
    try:
        transcript = _session.login(username, password)
    except LoginError as e:
        return f"LOGIN FAILED: {e}"
    except SessionError as e:
        return f"ERROR: {e}"
    return _clean(transcript)


@mcp.tool()
def mud_send(command: str, quiet_seconds: float = 1.0, timeout: float = 10.0) -> str:
    """Send one command to the MUD and return the response.

    Waits for the CircleMUD prompt ("> ") that terminates a response; falls
    back to a quiet-window drain if no prompt arrives within `timeout` (e.g.
    during combat). Example commands: "look", "north", "score", "kill rat".
    """
    if _session is None or not _session.is_open:
        return "ERROR: not connected — call mud_connect first."
    try:
        _session.send_command(command)
        out = _session.read_until_prompt(timeout=timeout)
        if not out.strip():
            out = _session.read_until_quiet(quiet_seconds=quiet_seconds, timeout=timeout)
    except SessionError as e:
        return f"ERROR: {e}"
    return _clean(out) or "(no output)"


@mcp.tool()
def mud_read(quiet_seconds: float = 1.0, timeout: float = 5.0) -> str:
    """Read pending async output (tells, combat rounds, room events).

    Returns whatever the server has pushed since the last read, without
    sending a command. Useful to poll for chatter between actions.
    """
    if _session is None or not _session.is_open:
        return "ERROR: not connected — call mud_connect first."
    try:
        out = _session.read_until_quiet(quiet_seconds=quiet_seconds, timeout=timeout)
    except SessionError as e:
        return f"ERROR: {e}"
    return _clean(out) or "(nothing pending)"


@mcp.tool()
def mud_status() -> str:
    """Report whether a session is currently connected, and to where."""
    if _session is None:
        return "disconnected (no session)"
    if _session.is_open:
        return f"connected to {_session.host}:{_session.port}"
    return "disconnected (session closed)"


@mcp.tool()
def mud_disconnect() -> str:
    """Close the telnet connection to the MUD."""
    global _session
    if _session is None or not _session.is_open:
        return "already disconnected"
    _session.close()
    _session = None
    return "disconnected"


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
