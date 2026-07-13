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

## G) Agenten-Testlauf + Login-Robustheit  ✅ verifiziert (2026-07-13)
Mit gesetztem `ANTHROPIC_API_KEY` und laufendem MUD getestet.
- **Aufruf:** aus `week0_explore/boukensha/`, `uv run boukensha --dsl journeys/test_pruefung.txt`
  (bzw. `uv run --directory week0_explore/boukensha boukensha …`, wenn cwd der Repo-Root ist).
- **Agent läuft:** verbindet, loggt ein, führt die Tool-Use-Schleife aus
  (`look` → `score`), erzeugt deutsche Zusammenfassung. **Logging vollständig:**
  JSONL in `~/.boukensha/logs/<id>/<datum>.jsonl` mit `prompt/action/tool/usage/output`.
- **Prompt-Caching verifiziert (isolierter Backend-Test):**
  - Sonnet 5 (Schwelle ~1024): Aufruf 2 `cache_read=2355` → Treffer, große Ersparnis.
  - Haiku 4.5 großer Präfix (~12,6k): Aufruf 2 `cache_read=12602` → Treffer.
  - Haiku 4.5 mit aktuellem Agent-Präfix (~2074 Tok.): `cache_read=0` — **unter**
    Haikus Cache-Schwelle. Greift erst, wenn der Verlauf über die Schwelle wächst
    (lange Mehr-Schritt-Sessions) oder bei Sonnet. Kein Bug, sondern Schwellwert.
- **Login-Bug behoben** in `boukensha/mud.py` (additiv; `session.py` unverändert):
  `MudManager.login()` treibt den Login jetzt selbst über die `MudSession`-Primitiven
  und behandelt BEIDE Fälle — *Reconnecting* (link-dead) UND *frischer Login*
  (MOTD/„PRESS RETURN" + Hauptmenü „1) Enter the game"). Beide Pfade live getestet
  → landen in der Welt (Temple Of Midgaard). Zuvor lief der frische Login in einen
  `ReadTimeout`.
- **Neu:** `journeys/test_pruefung.txt` (sicherer Prüf-Lauf: nur `look`+`score`).

## H) Auth: explizite `auth_token`-Umschaltung wieder ENTFERNT  ✅ (2026-07-13)
Die zuvor eingebaute explizite `auth_token`/OAuth-Umschaltung wurde auf Wunsch
**zurückgebaut**. Backend/Agent/Config nutzen wieder ausschließlich den
argumentlosen `anthropic.Anthropic()` (→ `ANTHROPIC_API_KEY` aus der Umgebung).
- Entfernt: `Config.auth_token`, `ClaudeBackend(auth_token=…)`-Zweig, die
  `BOUKENSHA_AUTH_TOKEN`/`settings.yml: auth_token`-Auflösung, sowie die
  README-Tabelle und der settings.yml-Kommentar.
- Hinweis bleibt bestehen: Das SDK kann ein `ant`-OAuth-Profil weiterhin selbst
  auflösen — das bucht aber auf API-Guthaben, nicht auf ein Abo (siehe Abschn. I).

## I) OAuth-Profil-„Absturz" analysiert + behoben  ✅ (2026-07-13)
Symptom: Agent stürzt bei Nutzung des `ant auth login`-OAuth-Profils „immer" ab.
- **Diagnose (reproduziert):** Alle Requests werden authentifiziert (SDK 0.116
  liest das Profil), aber die API antwortet mit `400 – "Your credit balance is too
  low"`. Ursache ist **kein Code-Bug**: `ant auth login` bucht auf das **API-Guthaben**
  der Console-Org, nicht auf ein claude.ai-Abo — und die Org hat kein Guthaben. Der
  `anthropic-beta: oauth-…`-Header ist hier NICHT der Blocker (mit/ohne identischer 400).
  Der „Absturz" war die **unbehandelte** `BadRequestError`-Exception (Traceback).
- **Fix (Code):**
  - `agent.py`: `step()` fängt Backend-/API-Fehler ab → kein Traceback mehr; neue
    Hilfsfunktion `_fehlermeldung()` übersetzt Billing/Auth/Rate-Limit in klare
    deutsche Hinweise; Fehler wird als `error`-Ereignis geloggt.
  - `cli.py`: Top-Level `try/except` um Connect/Login/REPL → sauberer Exit statt
    Traceback (KeyboardInterrupt → 130, sonst → 1).
- **Doku:** README-Abschnitt „Authentifizierung" um Abrechnungs-Warnung ergänzt.
- **Verifiziert:** kompiliert sauber; `agent.step()` liefert bei OAuth-only-Profil
  jetzt die Klartext-Meldung statt eines Absturzes.

## Nicht angefasst (bewusst, laut Vorgaben)
- `.boukensha/` (unverändert).
- `week0_explore/mud_manager/` (Ruby-Gem, unverändert).
- `preview/web`, `infrastructure/` (unverändert).
