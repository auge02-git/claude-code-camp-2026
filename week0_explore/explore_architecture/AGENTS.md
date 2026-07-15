# AGENTS.md

## Zweck dieses Repos
- Multi-Projekt-Workspace fuer AI-Agent-Experimente und Infrastruktur-Setups (nicht ein einzelnes Produkt).
- Schwerpunkte: `claudeCodeCamp/` (MCP + MUD), `copilotTests/` (Agent-Prompts/Personas), `l2-monitoring-stack/` (Observability).

## Big Picture Architektur
- `claudeCodeCamp/week0_explore/` bildet eine Pipeline aus mehreren Services:
  - `infrastructure/`: startet tbaMUD/CircleMUD via Docker Compose (MUD-Server lokal).
  - `circlemud-world-parser/`: Python/uv Parser fuer World-Files (`*.wld/*.mob/*.obj/...`) nach JSON.
  - `preview/`: nutzt erzeugte JSON-Daten fuer Web-Visualisierung.
  - `mud_manager/`: Ruby-basierter Telnet-Client/Command-Layer.
  - `mud-mcp/`: Python FastMCP-Server, exponiert `mud_*` Tools fuer AI-Agenten.
- Datenfluss (wichtig fuer Aenderungen): World-Files -> Parser -> JSON-Bundles -> Preview/Agent-Tools.

## Service-Grenzen & Integrationen
- MCP-Integration ist zentral: Root-`/.mcp.json` registriert MCP-Server fuer Agent-Tooling.
- Laufzeitkopplung: `mud-mcp` erwartet laufende `infrastructure` (typisch `localhost:4000`).

## Konkrete Entwickler-Workflows
- MUD-Infrastruktur starten:
```bash
cd claudeCodeCamp/week0_explore/infrastructure
docker compose up --build -d
```
- Parser bauen/testen (laut Projektstruktur mit Make + uv):
```bash
cd claudeCodeCamp/week0_explore/circlemud-world-parser
make test
make lint
make all
```
- MCP-Server lokal starten:
```bash
cd claudeCodeCamp/week0_explore/mud-mcp
uv sync
uv run python -m mud_mcp.server
```

## Repo-spezifische Konventionen
- Polyglot Toolchain: Python (`uv`), Node (`npm`), Ruby (`gem`), Docker Compose.
- Mehrere `docker-compose*.yml` Varianten pro Teilprojekt fuer unterschiedliche Deploy-Szenarien.
- Generierte Artefakte und Runtime-State liegen in projektlokalen Ordnern (z. B. Parser-Output / Preview-Daten) statt zentralem Build-Dir.
- AI-Prompting/Personas sind als Dateien organisiert (kein proprietaeres Tooling erforderlich).

## Hinweise fuer Coding Agents
- Vor Code-Aenderungen zuerst im betroffenen Teilprojekt arbeiten; es gibt keinen globalen Build-Entry-Point.
- Bei MCP-bezogenen Aenderungen immer Abhaengigkeit zur laufenden MUD-Infrastruktur mitdenken.
- Bei Parser-/Datenmodell-Aenderungen Downstream-Effekte auf `preview/` und MCP-Tool-Antworten pruefen.


