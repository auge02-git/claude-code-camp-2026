"""Long-lived telnet connection to a tbaMUD/CircleMUD server.

Python port of MudManager::Session (mud_manager/lib/mud_manager/session.rb).
A background thread continuously drains the socket into an internal buffer,
stripping telnet IAC negotiation bytes. Callers send a command and then use
``read_until_prompt`` / ``read_until_quiet`` to collect the response plus any
async chatter that arrived in the meantime.
"""

from __future__ import annotations

import json
import os
import re
import socket
import threading
import time
from pathlib import Path

# Credentials file. Read once when this module is imported ("beim Starten der
# session.py") so a session can log in without credentials being passed
# explicitly. Location is overridable via MUD_CREDENTIALS_FILE; the default sits
# at the mud-mcp project root (next to pyproject.toml).
CREDENTIALS_FILE = Path(
    os.environ.get(
        "MUD_CREDENTIALS_FILE",
        str(Path(__file__).resolve().parent.parent / "credentials.json"),
    )
)


def load_credentials(path: Path = CREDENTIALS_FILE) -> tuple[str, str]:
    """Read ``{"username": ..., "password": ...}`` from the credentials JSON.

    Returns ``("", "")`` if the file is missing or malformed — a missing file
    is not an error, it just means credentials must be supplied another way.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "", ""
    return str(data.get("username", "")), str(data.get("password", ""))


# Loaded at import time; login() falls back to these when none are passed.
DEFAULT_USERNAME, DEFAULT_PASSWORD = load_credentials()

# Telnet protocol bytes. We don't negotiate — we consume and discard IAC
# sequences so they don't pollute the buffer.
IAC = 0xFF
DONT = 0xFE
DO = 0xFD
WONT = 0xFC
WILL = 0xFB
SB = 0xFA
SE = 0xF0

# CircleMUD terminates every command response with a prompt ending in "> ".
PROMPT_SENTINEL = "> "


class SessionError(Exception):
    pass


class ConnectionClosed(SessionError):
    pass


class LoginError(SessionError):
    pass


class ReadTimeout(SessionError):
    pass


def _strip_iac(data: bytes) -> bytes:
    """Discard telnet IAC negotiation sequences, keeping literal 0xFF."""
    out = bytearray()
    i = 0
    n = len(data)
    while i < n:
        b = data[i]
        if b == IAC:
            nxt = data[i + 1] if i + 1 < n else None
            if nxt is None:
                break
            if nxt == IAC:
                out.append(0xFF)
                i += 2
            elif nxt in (WILL, WONT, DO, DONT):
                i += 3
            elif nxt == SB:
                j = i + 2
                while j < n and not (data[j] == IAC and j + 1 < n and data[j + 1] == SE):
                    j += 1
                i = j + 2
            else:
                i += 2
        else:
            out.append(b)
            i += 1
    return bytes(out)


class MudSession:
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 4000
    DEFAULT_TIMEOUT = 10.0

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self._socket: socket.socket | None = None
        self._reader: threading.Thread | None = None
        self._buffer = ""
        self._cond = threading.Condition()
        self._closed = False
        self._last_recv_at: float | None = None

    # ----- lifecycle -----

    def open(self) -> "MudSession":
        if self._socket is not None:
            raise SessionError("already open")
        try:
            self._socket = socket.create_connection((self.host, self.port), timeout=self.timeout)
        except OSError as e:
            raise ConnectionClosed(f"connect {self.host}:{self.port} failed: {e}") from e
        self._socket.settimeout(None)
        self._closed = False
        self._start_reader()
        return self

    @property
    def is_open(self) -> bool:
        return self._socket is not None and not self._closed

    def close(self) -> None:
        if self._closed:
            return
        with self._cond:
            self._closed = True
            self._cond.notify_all()
        try:
            if self._socket is not None:
                self._socket.close()
        except OSError:
            pass
        if self._reader is not None:
            self._reader.join(1)
        self._socket = None
        self._reader = None

    # ----- sending -----

    def send_command(self, command: str) -> str:
        if not self.is_open:
            raise SessionError("session not open")
        line = "" if command in ("\n", "\r\n") else command
        assert self._socket is not None
        self._socket.sendall((line + "\r\n").encode("utf-8", "replace"))
        return line

    # ----- reading -----

    def drain(self) -> str:
        with self._cond:
            out, self._buffer = self._buffer, ""
            return out

    def read_until_quiet(self, quiet_seconds: float = 1.0, timeout: float | None = None) -> str:
        if not self.is_open:
            raise SessionError("session not open")
        deadline = _monotime() + (timeout or self.timeout)
        with self._cond:
            while True:
                remaining_total = deadline - _monotime()
                if remaining_total <= 0:
                    break
                if (
                    self._last_recv_at is not None
                    and (_monotime() - self._last_recv_at) >= quiet_seconds
                    and self._buffer
                ):
                    break
                if self._last_recv_at is not None and self._buffer:
                    wait_for = quiet_seconds - (_monotime() - self._last_recv_at)
                else:
                    wait_for = remaining_total
                wait_for = min(wait_for, remaining_total)
                if wait_for <= 0:
                    break
                self._cond.wait(wait_for)
            out, self._buffer = self._buffer, ""
            return out

    def read_until(self, pattern: str | re.Pattern[str], timeout: float | None = None) -> str:
        if not self.is_open:
            raise SessionError("session not open")
        regexp = pattern if isinstance(pattern, re.Pattern) else re.compile(re.escape(pattern))
        deadline = _monotime() + (timeout or self.timeout)
        with self._cond:
            while True:
                m = regexp.search(self._buffer)
                if m:
                    cut = m.end(0)
                    out, self._buffer = self._buffer[:cut], self._buffer[cut:]
                    return out
                remaining = deadline - _monotime()
                if remaining <= 0:
                    raise ReadTimeout(f"read_until {pattern!r} after {timeout or self.timeout}s")
                if self._closed:
                    raise ConnectionClosed("socket closed while waiting")
                self._cond.wait(remaining)

    def read_until_prompt(self, timeout: float | None = None) -> str:
        try:
            return self.read_until(PROMPT_SENTINEL, timeout=timeout)
        except ReadTimeout:
            # e.g. combat spraying async lines; return whatever buffered.
            return self.drain()

    # ----- login dance -----

    def login(self, username: str | None = None, password: str | None = None) -> str:
        """Walk the CircleMUD login flow for an *existing* character.

        Credentials default to those read from the credentials file at import
        (``DEFAULT_USERNAME`` / ``DEFAULT_PASSWORD``) when not passed. Returns
        the transcript collected while entering the world. Raises LoginError on
        a wrong password or when no credentials are available. Creating a
        brand-new character (name/class/gender menus) is intentionally not
        handled here.
        """
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD
        if not username or not password:
            raise LoginError(
                "no credentials given and none found in credentials file "
                f"({CREDENTIALS_FILE})"
            )
        # mud_connect already reads up to the name prompt, so by the time we get
        # here it is usually gone from the buffer. Tolerate its absence: wait a
        # short moment in case it is still pending, otherwise proceed straight to
        # sending the name. (Blocking on it forever was the login bug.)
        try:
            transcript = self.read_until(
                re.compile(r"By what name do you wish to be known.*\?", re.I),
                timeout=2.0,
            )
        except ReadTimeout:
            transcript = ""
        self.send_command(username)
        transcript += self.read_until(re.compile(r"Password", re.I))
        self.send_command(password)
        output = self.read_until(re.compile(r"Welcome|Reconnecting|Wrong password", re.I))
        transcript += output
        if re.search(r"Reconnecting", output, re.I):
            pass  # already in-world
        elif re.search(r"Welcome", output, re.I):
            self.send_command("\n")  # dismiss motd -> main menu
            self.send_command("1")  # enter the game
            transcript += self.read_until_quiet()
        elif re.search(r"Wrong password", output, re.I):
            raise LoginError("wrong password")
        return transcript

    # ----- internals -----

    def _start_reader(self) -> None:
        def run() -> None:
            try:
                while True:
                    try:
                        chunk = self._socket.recv(4096)  # type: ignore[union-attr]
                    except OSError:
                        break
                    if not chunk:
                        break
                    text = _strip_iac(chunk).decode("utf-8", "replace")
                    if text:
                        with self._cond:
                            self._buffer += text
                            self._last_recv_at = _monotime()
                            self._cond.notify_all()
            finally:
                with self._cond:
                    self._closed = True
                    self._cond.notify_all()

        self._reader = threading.Thread(target=run, name="mud-reader", daemon=True)
        self._reader.start()


def _monotime() -> float:
    return time.monotonic()