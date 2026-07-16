"""Interactive MUD player — connects to localhost:4000, logs in as dummy/helloworld.

Uses MudSession from mud-mcp directly (no MCP overhead).

Usage:
    uv run --directory ../../mud-mcp python mud_player.py
    python mud_player.py                    # if mud-mcp is on PYTHONPATH
    python mud_player.py look               # run single command and exit
    python mud_player.py look "score" who   # run multiple commands and exit
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make mud-mcp importable when running directly from this directory.
# Script lives at .claude/scripts/ → parents[4] = week0_explore/
MUD_MCP_SRC = Path(__file__).resolve().parents[4] / "mud-mcp"
sys.path.insert(0, str(MUD_MCP_SRC))

from mud_mcp.session import MudSession  # noqa: E402

HOST = "localhost"
PORT = 4000
USERNAME = "dummy"
PASSWORD = "helloworld"


def send(session: MudSession, command: str) -> str:
    """Send one command and return the response up to the next prompt."""
    session.send_command(command)
    return session.read_until_prompt()


def interactive_loop(session: MudSession) -> None:
    """REPL: type commands, see responses, 'quit' exits."""
    print("Connected. Type MUD commands (quit/exit to disconnect).\n")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        response = send(session, raw)
        print(response)
        if raw.lower() in ("quit", "exit"):
            break


def main() -> None:
    session = MudSession(HOST, PORT)
    session.open()
    print(f"[+] Connected to {HOST}:{PORT}")

    transcript = session.login(USERNAME, PASSWORD)
    print("[+] Logged in")
    # Show the room/welcome text that arrived after login.
    if transcript.strip():
        print(transcript)

    # Flush any leftover banner text.
    leftover = session.read_until_quiet(quiet_seconds=0.5, timeout=2.0)
    if leftover.strip():
        print(leftover)

    args = sys.argv[1:]
    if args:
        # Batch mode: run each argument as a command, print responses, then quit.
        for cmd in args:
            print(f"\n>> {cmd}")
            print(send(session, cmd))
        session.send_command("quit")
    else:
        interactive_loop(session)

    session.close()
    print("[+] Disconnected")


if __name__ == "__main__":
    main()
