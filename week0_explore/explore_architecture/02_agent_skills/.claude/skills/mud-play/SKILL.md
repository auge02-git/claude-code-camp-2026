---
name: mud-play
description: Manage the CircleMUD/tbaMUD connection on localhost:4000. Use when the user wants to connect, login, send commands, run the mud_player script, or interact with the MUD server. Credentials: dummy / helloworld.
---

# MUD Play

Helps manage a live telnet connection to the CircleMUD/tbaMUD server at `localhost:4000`.
Two ways to connect:
- **Python script** (`mud_player.py`) — direct telnet, no MCP needed
- **MCP tools** (`mud_*`) — via the mud-mcp server, used by Claude Code

## Python Script (mud_player.py)

Located at `week0_explore/explore_architecture/02_agent_skills/.claude/scripts/mud_player.py`.

Run from the repo root (`claudeCodeCamp/`). The `cd` trick avoids the `uv run --directory`
path-resolution quirk (it resolves script paths relative to its own directory, not cwd):

```sh
# Interactive REPL
(cd week0_explore/mud-mcp && uv run python \
  ../explore_architecture/02_agent_skills/.claude/scripts/mud_player.py)

# Single command, then exit
(cd week0_explore/mud-mcp && uv run python \
  ..//explore_architecture/02_agent_skills/.claude/scripts/mud_player.py look)

# Multiple commands in batch
(cd week0_explore/mud-mcp && uv run python \
  ../explore_architecture/02_agent_skills/.claude/scripts/mud_player.py look score who)
```

The script imports `MudSession` from `mud-mcp` directly. It connects, logs in as
`dummy`/`helloworld`, and either drops into an interactive REPL or runs the
commands passed as arguments and exits.

Uses the `mud_*` MCP tools (provided by `mud-mcp/`) to control the session.

## Connection Setup

### Step 1: Connect
```
mud_connect  →  host: localhost, port: 4000
```
Check the result — the server should respond with the login banner.

### Step 2: Login
```
mud_login  →  name: dummy, password: helloworld
```
Wait for the "Welcome to tbaMUD" prompt. If the character doesn't exist yet, create it
manually once via `telnet localhost 4000` before using this skill.

### Step 3: Verify
```
mud_read  →  read any pending output to confirm you are at the game prompt
```

## Sending Commands

Use `mud_send` for every in-game action:

| Goal                      | Command to send                       |
|---------------------------|---------------------------------------|
| Look around               | `look`                                |
| Check inventory           | `inventory`                           |
| Move (n/s/e/w/u/d)        | `north`, `south`, …                   |
| Check score / stats       | `score`                               |
| Who is online             | `who`                                 |
| Read room exits           | `exits`                               |
| Pick up an item           | `get <item>`                          |
| Talk to an NPC            | `say <text>`  or  `tell <npc> <text>` |
| Check connection status   | `mud_status`                          |

After each `mud_send`, call `mud_read` to capture the server response.

## Disconnecting

```
mud_send  →  quit
mud_disconnect
```

## Troubleshooting

- **Not connected**: run `mud_status` — if disconnected, repeat Step 1 and 2.
- **Login fails**: character may not exist yet — create it manually via telnet first.
- **No output from mud_read**: the MUD may be waiting for input; send `\n` (empty line) first.
- **MUD server not running**: start it with `cd week0_explore/infrastructure && docker compose up -d`.

## Credentials (default)

| Field    | Value      |
|----------|------------|
| host     | localhost  |
| port     | 4000       |
| name     | dummy      |
| password | helloworld |