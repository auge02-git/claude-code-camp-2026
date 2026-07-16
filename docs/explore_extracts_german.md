# Architektur-Exploration: Erkenntnisse aus den Teilschritten (Aktueller Stand)

## Ziel
Die Teilschritte definieren einen schlanken Agenten-Workflow mit klarer Sprach- und Kontextsteuerung, um Tokenverbrauch zu reduzieren und Off-Task-Verhalten zu vermeiden. Die Architektur ist jetzt produktionsreif und wurde über 9+ Iterationen mit echtem MUD-Gameplay getestet.

## Implementierte Teilschritte (konsolidiert, aktuell)

### 1. Modellwahl nach dem Start
- **Default:** `Claude Haiku 4.5` (kostengünstig, für Iterationsschleifen optimiert)
- **Alternative:** `Claude Sonnet 4.6` (bessere Qualität, höhere Kosten)
- **Lokal:** `google/gemma-4-12b-qat` oder andere via LiteLLM/Ollama für kostenlose Experimente
- **Konfiguration:** Via `ANTHROPIC_API_KEY`, `--model`, `--llm-base-url` Flags oder Umgebungsvariablen

### 2. Kontextspezifische Dateien laden (Hierarchie)
- **System-Level:** `explore_architecture/EXPLORATION.md` (Architektur-Übersicht)
- **Operativ:** `explore_architecture/AGENTS_PROMPTING_INSTRUCTIONS.md` (Sicherheitsregeln, Navigationsanker)
- **Referenz:** `explore_architecture/AGENTS.md` (Service-Grenzen, Workflows)
- **Historie:** `week0_explore/logs/mud-journeys-*.log` (Iterationskorpus für Few-Shot-Learning)
- **Leitlinie:** Nur Dateien laden, die für den aktuellen Agenten-Schritt notwendig sind

### 3. Sprachsteuerung
- **UI/Benutzer-Output:** Deutsch möglich (aber flexibel per Agent-Konfiguration)
- **Interne Code/Identifiers:** Englisch (Python-Idiom, Stabilität)
- **System-Prompt:** Kann gemischt sein (Deutsch für Anweisungen, Englisch für technische Details)
- **Logs:** JSONL mit englischen Feldnamen, deutsche Kommentare optional

### 4. Zentrale Wissensquellen (Agenten-Registry)
- **`EXPLORATION.md`:** Modulare Architektur, Komponenten, Guardrails
- **`AGENTS.md`:** Service-Grenzen, Workflow-Dokumentation, Developer-Guidelines
- **`AGENTS_PROMPTING_INSTRUCTIONS.md`:** Operative Handlungsanweisungen, Sicherheitsregeln, Failure-Patterns
- **`week0_explore/journeys/`:** Versioned DSL-Szenarien für reproduzierbare Runs
- **`week0_explore/logs/`:** Historische Ausführungsdaten (Optimierungskorpus)

### 5. Ausgabe-Optimierung (kompakt halten)
- **Token-Ziele:** Input/Output je Step <1000 Tokens
- **Prompt-Caching:** Ephemerale Cache-Kontrolle auf System-Prompt, Tools, Nachrichtenverlauf
- **Step-Limits:** Default `--max-steps=12`, konfigurierbar für längere Runs
- **Telemetry:** `input_tokens`, `output_tokens`, `cache_write_tokens`, `cache_read_tokens` pro Step geloggt

## Beobachtungen und Erkenntnisse (aktualisiert, aus 9+ Runs)

### Architektur-Level
- ✅ **Persistente Session-Schnittstelle funktioniert:** `mud-mcp` + `mud_manager` bietet stabile Telnet-Abstraktion
- ❌ **Ad-hoc Socket-Skripte waren fragil:** Zeitweise erzeugte Agenten temporäre Skripte → hoher Fehlerquote
- ✅ **Zentrale Konfiguration reduziert Off-Task:** Mit `~/.boukensha/settings.yml` und Env-Vars bleibt Agent auf Kurs
- ✅ **Context-Disziplin spart 15–20% Tokens:** Selective File Loading reduziert Drift deutlich

### Operativ (MUD-Gameplay)
- **Navigation war größter Blocker:** Loops zwischen `Common Square`, `Market Square`, `Poor Alley` → Lösung: Hard-codierte Route-Checkpoints
- **Fountain-Effizienz-Problem:** Brunnen zu lange nicht gefunden → Lösung: Wasser-Suche in Top-5 Prioritäten
- **Farming stagnierte:** Agenten erreichten Farm-Zone selten → Lösung: Phase-1-Stabilisierungsplan mit <10 Schritt-Budget
- **Void-State-Verluste:** Nach 15+ `look`-Kommandos ohne Aktion → Lösung: Erzwungene <3-Look-Limite pro Raum
- **Guard-Eskalationen:** Verzögerte Flee-Reaktionen → Lösung: "has arrived" → Sofort-Flee-Reflex ohne Zwischen-Evaluation

### Kostenoptimierung
- **Haiku 4.5 Effizienz:** 60–70% der Sonnet-Qualität bei ~1/6 der Kosten; ideal für Iterationen
- **Prompt-Caching wirksam:** ~20–30% Input-Token-Reduktion auf 2nd+ Durchlauf der gleichen Session
- **Journey-DSL reduziert Latenz:** Pre-scripted Kommandosequenzen vs. interaktives Prompting ~3x schneller

## Abgeleitete Architektur-Empfehlungen (bestätigt)

### Zentrale Kapseln
- ✅ **Session-Abstraktions-Layer (`mud-mcp/mud_manager`)** — reussieren, nicht neu schreiben
- ✅ **Tool-Registry (`boukensha/registry.py`)** — Standard-Werkzeuge (`look`, `move`, `kill`, `flee`, `loot`, `eat`) zentral pflegen
- ✅ **Config-Loader (`boukensha/config.py`)** — Model, Host, Port, System-Prompt-Pfade hierarchisch auflösen

### Context-Management
- ✅ **Nur notwendige Dateien pro Schritt laden** — kein rekursives Directory-Scanning
- ✅ **Journey-Versionierung** — `mud-journeys-2026-07-15_v*.log` für Regression-Tests verwenden
- ✅ **JSONL-Logging für Audit** — jeden Schritt mit Usage/Tool-Call/Outcome protokollieren

### Error Recovery (robust)
- ✅ **Shared Session-API statt ad-hoc Skripte** — Login-Fehler zentral behandeln
- ✅ **Fallback-Chains** — `ANTHROPIC_API_KEY` → env-var → Gateway-Token → interaktive Aufforderung
- ✅ **Graceful Degradation** — Local LLM als Fallback, wenn API überlastet (HTTP 429)

## Praktische Leitlinie für Agent-Runs (Stand 2026-07-16)

### Vor dem Start
1. **Modell + Sprache fixieren:**
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   export ANTHROPIC_LLM_MODEL=claude-haiku-4-5
   ```
2. **Infrastructure starten:**
   ```bash
   cd week0_explore/infrastructure
   docker compose up -d
   ```
3. **Agent konfigurieren:**
   ```bash
   cd week0_explore/boukensha
   cat ~/.boukensha/settings.yml  # oder defaults verwenden
   ```

### Während des Runs
- **Sicherheitsregeln als Reflex-Level-Constraints:**
  - NIEMALS: `cityguard`, `Peacekeeper`, `knight`, `sorcerer`, `Mayor` angreifen
  - "has arrived" → Sofort `flee` (keine `look` davor)
  - HP <30% → Sofort `flee`
  - <3 `look`-Kommandos pro Raum, dann `move` oder Reset

- **Navigation mit Checkpoints (statt Trial-and-Error):**
  - Start: `Common Square` → `Temple Square` (Wasser) → `Poor Alley` → `Eastern End (3024)` (Farm)
  - Jeder Raum: Exits aus `Exits: ...` Zeile extrahieren, nur diese verwenden

- **Bei Verbindungsfehlern:**
  - 1. Versuchen: Reconnect über `mud-mcp/session.py`
  - 2. Fallback: Frischer Login über MOTD/Menü
  - 3. Last Resort: Lokales LLM starten (`--local-llm --model google/gemma-4-12b-qat`)

- **Antworten kurz halten:**
  - Pro Step 1–2 Sätze + Aktion
  - Telemetry nur am Run-Ende zusammenfassen
  - Output-Tokens <500/Step anstreben

### Nach dem Run
- **Logs archivieren:** `week0_explore/logs/mud-journeys-DATUM_vN.log`
- **Metriken auswerten:** Token-Verbrauch, Cache-Hit-Rate, Completion-Zeit
- **Erkenntnisse als neuen Journey-Plan festhalten:** `week0_explore/boukensha/journeys/erfahrungen_vN.txt`
- **Bei Erfolg sichern:** `quit` bei Reception (kostenlos, persistent)

## Aktualisierte Implementierungs-Status (Stand 2026-07-16)

| Komponente | Status | Bemerkung |
|---|---|---|
| `infrastructure/` (CircleMUD Docker) | ✅ Live | läuft, persistent |
| `mud-mcp/` (MCP-Bridge) | ✅ Produktiv | stabil, getestet |
| `mud_manager/` (Ruby-Session) | ✅ Legacy-Stable | unverändert, als Boundary bewahrt |
| `boukensha/agent.py` | ✅ Produktiv | Agentic Loop + Prompt-Caching |
| `boukensha/config.py` | ✅ Produktiv | Model-Overrides, Env-Vars |
| `boukensha/cli.py` + `repl.py` + `run_dsl.py` | ✅ Produktiv | REPL, Journey-DSL, alle Einstiegspunkte |
| `boukensha/tools/` | ✅ Produktiv | 8–10 MUD-Werkzeuge implementiert |
| `boukensha/log_viz/server.py` (FastAPI) | ✅ Optional | für Session-Replay + Analytics |
| `circlemud-world-parser/` | ✅ Produktiv | JSON-Export von World-Files |
| `preview/` | ✅ Optional | Web-Visualisierung der Welt |
| `journeys/` (DSL-Scripts) | ✅ Aktiv | 9+ Versionen, optimiert |
| `logs/` (Korpus) | ✅ Aktiv | Archiv für Few-Shot-Learning |

## Nächste Schritte (Roadmap)

### Phase 1 – Stabilisierung (abgeschlossen, Validierung läuft)
- ✅ Sichere Farmrouten etabliert
- ✅ Sicherheitsregeln als System-Prompt codiert
- ⏳ Live-Test mit echtem API-Key (in Bearbeitung)

### Phase 2 – Optimierung (w.o. – nächste 2–3 Runs)
- Farm-Loop auf 5+ Kills pro Run skalieren
- Level 2 erreichen (1764 Exp erforderlich)
- Neue Orte erkunden (Kanalisation, Läden, Gildenmeister)

### Phase 3 – Erweiterung (w.o. – Woche 2)
- Skill-Acquisition nach Level-Up automatisieren
- Multi-Character-Support (mehrere Agenten parallel)
- Dynamische Ruten-Erzeugung (basierend auf geparsten World-Daten)

### Phase 4 – Wirtschaft (w.o. – Woche 3+)
- ATM-Integration (Geldverwaltung)
- NPC-Handel + Preisoptimierung
- Quest-Automation (falls möglich)

