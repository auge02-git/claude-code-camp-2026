# mud-mcp

MCP server that exposes telnet control of the tbaMUD/CircleMUD server
(`localhost:4000`) as tools, so Claude Code or an agent can play the MUD one
command at a time. Python + FastMCP, managed with `uv`.

## Tools

| Tool | Purpose |
|------|---------|
| `mud_connect(host="localhost", port=4000)` | Open the telnet connection; returns the login banner up to the name prompt. |
| `mud_login(username, password)` | Log an **existing** character into the world. Falls back to `MUD_NAME` / `MUD_PASSWORD` env vars. |
| `mud_send(command, quiet_seconds=1.0, timeout=10.0)` | Send one command, return the response (waits for the `> ` prompt). |
| `mud_read(quiet_seconds=1.0, timeout=5.0)` | Read pending async output (tells, combat) without sending anything. |
| `mud_status()` | Report connection state. |
| `mud_disconnect()` | Close the connection. |

The telnet/IAC-stripping and CircleMUD login logic are a Python port of
`mud_manager/lib/mud_manager/session.rb`. Creating a **new** character
(name confirmation + class/gender menus) is not handled — do that once
manually via `telnet localhost 4000` (see `../HOW_TO_PLAY.md`), then log in
with `mud_login`.

## Registration

Registered for this repo in `../../.mcp.json` (project scope). Claude Code
starts it from the repo root with:

```sh
uv run --directory week0_explore/mud-mcp mud-mcp
```

Requires the MUD server to be running (`cd ../infrastructure && docker compose up -d`).

## Development

```sh
uv sync                              # install deps into .venv
uv run python scripts/smoke_test.py  # drive the server over stdio against the live MUD
uv run python -m mud_mcp.server      # run the server directly (stdio)
```
