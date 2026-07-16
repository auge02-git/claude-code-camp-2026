# AGENTS.md

## Purpose of This Repository
- Multi-project workspace for AI agent experiments and infrastructure setups (not a single product).
- Focus areas: `claudeCodeCamp/` (MCP + MUD), `copilotTests/` (agent prompts/personas), `l2-monitoring-stack/` (observability).

## Big Picture Architecture
- `claudeCodeCamp/week0_explore/` forms a pipeline of multiple services:
  - `infrastructure/`: starts tbaMUD/CircleMUD via Docker Compose (local MUD server).
  - `circlemud-world-parser/`: Python/uv parser for world files (`*.wld/*.mob/*.obj/...`) to JSON.
  - `preview/`: uses generated JSON data for web visualization.
  - `mud_manager/`: Ruby-based Telnet client/command layer.
  - `mud-mcp/`: Python FastMCP server, exposes `mud_*` tools for AI agents.
- Data flow (important for changes): World Files → Parser → JSON Bundles → Preview/Agent-Tools.

## Service Boundaries & Integrations
- MCP integration is central: root-level `/.mcp.json` registers MCP servers for agent tooling.
- Runtime coupling: `mud-mcp` expects running `infrastructure` (typically `localhost:4000`).

## Concrete Developer Workflows
- Start MUD infrastructure:
```bash
cd claudeCodeCamp/week0_explore/infrastructure
docker compose up --build -d
```
- Build/test parser (per project structure with Make + uv):
```bash
cd claudeCodeCamp/week0_explore/circlemud-world-parser
make test
make lint
make all
```
- Start MCP server locally:
```bash
cd claudeCodeCamp/week0_explore/mud-mcp
uv sync
uv run python -m mud_mcp.server
```

## Repository-Specific Conventions
- Polyglot toolchain: Python (`uv`), Node (`npm`), Ruby (`gem`), Docker Compose.
- Multiple `docker-compose*.yml` variants per subproject for different deployment scenarios.
- Generated artifacts and runtime state live in project-local folders (e.g., parser output/preview data) rather than a central build directory.
- AI prompting/personas are organized as files (no proprietary tooling required).

## Notes for Coding Agents
- Before making code changes, start by working within the affected subproject; there is no global build entry point.
- For MCP-related changes, always consider the dependency on the running MUD infrastructure.
- For parser/data model changes, verify downstream effects on `preview/` and MCP tool responses.

