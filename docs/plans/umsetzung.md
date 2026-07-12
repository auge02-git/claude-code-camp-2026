# Umsetzungsstand (was bereits gebaut/geändert wurde)

Stand: **2026-07-12**. Ergänzt zu `00_fortsetzen_hier.md` (Live-Zustand) und
`vorgaben.md` (Regeln). Hier: konkrete, bereits erfolgte Änderungen — Datei für Datei.

## A) mud-mcp — Login-Fix + automatische Credentials  ✅ erledigt
Verzeichnis: `week0_explore/mud-mcp/`
- **`mud_mcp/session.py`**
  - Bug behoben: `login()` wartete erneut auf den Namens-Prompt, den `mud_connect`
    schon konsumiert hatte → jetzt **tolerant** (kurzer Timeout, sonst weiter).
  - **Credentials-Loader** ergänzt: `load_credentials()` liest beim Import
    `credentials.json` → `DEFAULT_USERNAME` / `DEFAULT_PASSWORD`. Pfad via
    `MUD_CREDENTIALS_FILE` überschreibbar. `login()`-Argumente sind optional.
- **`mud_mcp/server.py`**: `mud_login(username="", password="")` — Reihenfolge
  Argument → `MUD_NAME`/`MUD_PASSWORD` → `credentials.json`.
- **`credentials.json`** (neu): `{ "username": "dummy", "password": "helloworld" }`.
- **`credentials.example.json`** (neu): Vorlage.
- **`.gitignore`**: `credentials.json` ausgenommen (Klartext-Passwort nicht committen).
- Verifiziert: `mud_login()` **ohne Argumente** loggt live ein; Persistenz nach
  `quit`/Reconnect bestätigt.

> Wirksam erst nach **Neustart** des MCP-Servers (`/mcp` reconnect) — bereits erfolgt.

## B) Projekt-Doku  ✅ erledigt
- **`CLAUDE.md`** (Repo-Root): `mud-mcp` als 5. Sub-Projekt ergänzt (Tools, Pfade,
  Login-Bug-Hinweis, „fünf Sub-Projekte").

## C) MUD-Spiel-Logs & Pläne  ✅ erledigt
Verzeichnis: `week0_explore/logs/` bzw. `docs/plans/`
- **`week0_explore/logs/mud-session-2026-07-12.md`** (+ `.log`): nachlaufbare Route,
  Monster-Markierungen (schwach/stark), optimierte Route v2, Fehler-Protokoll.
- **`docs/plans/week0_dummy_level-and-skills.md`**: Spielplan + Fortschritts-Log.
- **`docs/plans/boukensha_architecture_python.md`**: Architektur-Blaupause (JSON→Python).
- **`docs/plans/00_fortsetzen_hier.md`, `vorgaben.md`, `umsetzung.md`** (diese Dateien).

## D) MUD-Spielfortschritt (`dummy`)  ✅ teilweise
- Erreicht: Wasser, Essen, Marktplatz gefunden, Skill **kick** gelernt.
- Geleveled: **236 → 336 Exp**; **10 → 20 Gold**; gesichert (free-rent `quit`).
- Autonomer Farm-Loop `f40a8f93` aktiv (siehe `00_fortsetzen_hier.md`).

## E) Boukensha-Agent (Architektur-Umsetzung)  ⏳ offen
- **Nur geplant, noch nicht gebaut.** Blaupause steht; Paket-Gerüst unter
  `week0_explore/boukensha/` **wartet auf Go**.
- Geplantes Gerüst (neu, additiv):
  ```
  week0_explore/boukensha/
    pyproject.toml            # entry: boukensha = boukensha.cli:main (uv)
    boukensha/__init__.py     # Bounkensha.run()
      config.py logger.py context.py registry.py
      agent.py                # Agentic Loop (Observe→Take Action→Reflect→Observe/→Output)
      mud.py                  # dünner Wrapper um mud_mcp.session (nur Import)
      tools/base.py tools/mud_tools.py
      backends/anthropic.py   # Claude-Backend (Haiku 4.5, Alt.: Sonnet 4.6)
      cli.py repl.py run_dsl.py
    log_viz/server.py         # FastAPI (neu)
  ```

## Nicht angefasst (bewusst, laut Vorgaben)
- `.boukensha/` (unverändert).
- `week0_explore/mud_manager/` (Ruby-Gem, unverändert).
- `preview/web`, `infrastructure/` (unverändert).
