# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repo purpose and structure

This is the repo for the ExamPro "Claude Code Camp": building tooling around a running
CircleMUD/tbaMUD text-adventure server, ultimately so an AI agent can play it. Work is split
into weekly stages, each its own top-level directory:

- `week0_explore/` — current stage, all active code lives here (see below).
- `week1_baseline/`, `week2_capable/` — empty stubs (`.keep` only), reserved for later stages.
- `docs/plans/` — empty, reserved for planning docs.
- `.boukensha/` — empty, reserved (likely the future agent's home).

Everything below is under `week0_explore/`, which has five independent sub-projects wired
together by a data pipeline:

```
infrastructure/ (Docker/tbaMUD server)
        │  world files (lib/world/*.wld,.mob,.obj,.shp,.zon,.trg,.qst)
        ▼
bin/convert-world  ──▶  circlemud-world-parser/ (Python, uv)
        │  per-file JSON
        ▼
preview/data/world/{wld,mob,obj,zon,shp,trg,qst}/*.json
        ▼
preview/web/scripts/build-data.mjs  (aggregates into id-keyed bundles)
        ▼
preview/web/public/data/*.json  ──▶  preview/web (React/Vite SPA, read-only viewer)

mud_manager/ (Ruby gem)   — telnet session + typed command primitives, standalone (examples/).
mud-mcp/ (Python, uv)      — MCP server exposing telnet control of the MUD as tools; a port of
  mud_manager's session logic. This IS the wired agent path — registered in root .mcp.json,
  so Claude Code drives the live MUD via mud_* tools (mud_connect/login/send/read).
```

`bin/convert-world` (at `week0_explore/bin/convert-world`) is the glue: it runs the Python
parser over every file in `infrastructure/lib/world/` and writes JSON into
`preview/data/world/`. Run it from anywhere; it resolves paths relative to itself.

## Component commands

### infrastructure/ — tbaMUD server (Docker Compose)

```sh
cd week0_explore/infrastructure
docker compose up --build       # build image, run server on localhost:4000
docker compose up --build -d    # same, detached
docker compose logs -f
docker compose down              # stop
docker compose down -v           # stop + delete the circlemud-lib volume
bin/reset                        # wipe player data (chars/objects/mail) back to a clean world, restarts container if it was running
```

Connect to the running server with `telnet localhost 4000` or `nc localhost 4000`. The
Dockerfile builds tbaMUD (CircleMUD's successor, ships DG Scripts + quest engine) from source
via `TBAMUD_REF` (default `master`); world/player data is seeded from an in-image
`lib.dist` into the bind-mounted `./lib` on first boot (see `docker-entrypoint.sh`) and is
gitignored — treat `./lib` as generated, mutable state, never commit it.

### circlemud-world-parser/ — world-file → JSON parser (Python, uv-managed)

```sh
cd week0_explore/circlemud-world-parser
make test     # uv run pytest -v
make lint     # uv run isort --check-only + ruff check + ty check
make clean    # remove .pyc and _output/
make all      # clean, then convert assets/ -> _output/ (sample/dev conversion)
```

Run a single test: `uv run pytest -v tests/test_room.py::test_name`.

Requires Python 3.14+ (`.python-version`); dependencies and the `circlemud-parse` CLI entry
point are declared in `pyproject.toml` and locked in `uv.lock` — use `uv run …`, not a bare
`python`/`pip` venv. `requirements.txt` is a stale pre-uv artifact (pins `click`/`flake8`/`black`,
none of which match current deps) — ignore it in favor of `pyproject.toml`.

Parses CircleMUD/tbaMUD world flat-files (`.wld` rooms, `.mob` NPCs, `.obj` items, `.shp`
shops, `.zon` zone resets, plus `.trg`/`.qst` for DG Scripts/quests) into typed JSON. Bitvector
flags and enums are decoded via lookup tables in `circlemud_world_parser/constants.py` — if the
target MUD has non-stock flags, extend there. Since this fork targets tbaMUD (not stock
CircleMUD 3.1), non-standard/extended fields may still fail to parse; parse errors are logged
to stderr per-entry and don't abort the batch.

### mud_manager/ — Ruby telnet client + command primitives

```sh
cd week0_explore/mud_manager
gem build mud_manager.gemspec
gem install ./mud_manager-0.1.0.gem
MUD_NAME=YourCharacterName MUD_PASSWORD=yourpassword ruby examples/live_session_test.rb
```

Two pieces, deliberately separated:
- `MudManager::Session` (`lib/mud_manager/session.rb`) — long-lived telnet connection with a
  background reader thread, IAC stripping, and prompt/quiet-window-based response collection
  (`read_until`, `read_until_quiet`, `read_until_prompt`). Handles the CircleMUD login dance.
- `MudManager::Primitives` (`lib/mud_manager/primitives.rb`) — stateless, enum-validated command
  builders (movement, combat, shops, bank, mail, etc.) that return `Command` structs. These only
  validate argument shape, not runtime preconditions (position, skill availability, room
  flags) — that logic belongs to a future agent layer that wraps primitives as tool calls.

Comments in `primitives.rb` reference `FINDINGS/_synthesis/player-command-surface.md` as the
source of truth for the command surface — that path doesn't exist in this repo yet.

### mud-mcp/ — MCP server for driving the live MUD (Python, uv, FastMCP)

```sh
cd week0_explore/mud-mcp
uv sync                              # install deps into .venv
uv run python scripts/smoke_test.py  # drive the server over stdio against the live MUD
uv run python -m mud_mcp.server      # run the server directly (stdio)
```

Registered in the **root** `.mcp.json` at project scope, so Claude Code auto-starts it via
`uv run --directory week0_explore/mud-mcp mud-mcp` and gets `mud_connect`, `mud_login`,
`mud_send`, `mud_read`, `mud_status`, `mud_disconnect` tools. Requires the MUD server running
(`infrastructure/` up on `localhost:4000`). `mud_mcp/session.py` is a Python port of
`mud_manager`'s `session.rb` (telnet/IAC stripping, CircleMUD login dance); `mud_login` only
logs in **existing** characters — new-character creation (name/class/gender menus) is not
handled, so create a character once manually (`telnet localhost 4000`, see `HOW_TO_PLAY.md`)
before using it. `mud_login` falls back to `MUD_NAME`/`MUD_PASSWORD` env vars.

### preview/web/ — read-only world viewer (React + Vite + TypeScript)

```sh
cd week0_explore/preview/web
npm install
npm run dev          # runs build:data, then vite dev server on :5174
npm run build         # build:data, tsc -b, vite build
npm run build:data    # only regenerate public/data/*.json bundles from preview/data/world
npm run lint          # tsc -b --noEmit
```

`public/data/` (generated bundles) and `node_modules/` are gitignored — always safe to
regenerate via `build:data`. Reverse indexes (e.g. "what spawns in this room", "who sells this
item") are built client-side in `src/data/relations.ts`, not precomputed by the build script.
This app is a developer inspection tool only — it is not, and should not become, part of any
agent's runtime path.

### Playing the MUD manually

`week0_explore/HOW_TO_PLAY.md` documents the manual play/login flow: the first character
ever created on a fresh world becomes the admin (level 34, "the Implementor"); subsequent
characters are normal players. Persistence across sessions requires `offer` + `rent` at an
inn — without it, quitting and reconnecting resets you to the starting room.

## Working across sub-projects

There is no root-level build/test command — each of the five sub-projects (`infrastructure`,
`circlemud-world-parser`, `mud_manager`, `mud-mcp`, `preview/web`) has its own toolchain
(Docker; uv; RubyGems; uv; npm respectively) and must be entered via `cd` before running its
commands.
