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

## E) Boukensha-Agent (Architektur-Umsetzung)  ✅ in Betrieb genommen
- **Gerüst angelegt** unter `week0_explore/boukensha/` (kompiliert sauber,
  `python -m compileall boukensha log_viz` = OK). Alle Module additiv, leitplanken-konform.
- **Inbetriebnahme erledigt (2026-07-13):**
  - `uv sync` ✅ — `mud-mcp` als editierbare Pfad-Abhängigkeit eingebunden,
    `anthropic`/`pyyaml`/`rich` installiert.
  - Verdrahtungs-Smoke-Test ✅ — Config lädt (Modell `claude-haiku-4-5-20251001`),
    Registry mit **9 Werkzeugen**, Anthropic-Schemas gültig, Backend lazy (Haiku 4.5).
  - MUD-Pfad **ohne LLM** live getestet ✅ — `MudManager` connect → login (via
    `credentials.json`) → `look`/`score`/`quit` gegen den laufenden Server
    (Puffer-Latenz wie dokumentiert, vom `read_pending`/`observe()`-Schritt abgefangen).
  - **Agent-Home `~/.boukensha` angelegt** ✅ — `settings.yml` (Modell + MUD)
    + `prompts/system.md` (deutscher System-Prompt, 2070 Z.). Config lädt ihn.
  - **README** für das Paket geschrieben ✅ (`week0_explore/boukensha/README.md`).
- **Noch offen:**
  - **`ANTHROPIC_API_KEY` setzen** und echten Live-Lauf mit LLM fahren
    (`uv run boukensha`) — Key war in der Test-Shell nicht gesetzt.
  - Modell-ID **Sonnet 4.6** final bestätigen (`config.py:ALT_MODEL` = `claude-sonnet-4-6`).
  - Optional: Feinschliff Agentic Loop (Reflect-Schritt explizit).
- **Gebautes Gerüst:**
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

## F) Prompt-Caching (Token-Ersparnis)  ✅ eingebaut (2026-07-13)
Datei: `week0_explore/boukensha/boukensha/backends/anthropic.py`
- `cache_control: {"type": "ephemeral"}` an den bei jedem Loop-Schritt erneut
  gesendeten Content-Blöcken gesetzt: **System-Prompt**, **letztes Werkzeug**
  (cacht den ganzen Tool-Block) und **letzte User-Nachricht** (inkrementelles
  Caching des wachsenden Verlaufs). Eingaben werden nicht mutiert; per
  `ClaudeBackend(use_cache=False)` abschaltbar.
- **Wichtig:** `cache_control` gehört an **Content-Blöcke**, NICHT als Top-Level-
  Parameter von `messages.create` (den gibt es nicht). Greift erst ab Mindest-
  Präfixlänge (Sonnet ~1024, Haiku ~2048 Tokens), sonst folgenlos ignoriert.
- **`agent.py`**: `_log_usage()` protokolliert `input/output/cache_write/cache_read`
  je Schritt (Cache-Wirkung im JSONL sichtbar).
- Verifiziert: Kompiliert sauber; Transformationen getestet (Breakpoints korrekt,
  keine Mutation der Original-Objekte).

## Nicht angefasst (bewusst, laut Vorgaben)
- `.boukensha/` (unverändert).
- `week0_explore/mud_manager/` (Ruby-Gem, unverändert).
- `preview/web`, `infrastructure/` (unverändert).
