# Vorgaben & Leitplanken (verbindlich)

Konsolidierte Sammlung **aller** Vorgaben aus dieser Arbeitsphase. Gilt für alle
weiteren Anpassungen. Siehe auch `00_fortsetzen_hier.md` (Einstieg) und
`boukensha_architecture_python.md` (Architektur-Detail).

## 1. Baseline
- **Implementierung in Python** (uv-verwaltet), analog zu `mud-mcp` / `circlemud-world-parser`.
- **Deutsch** für Dokumentation, Kommentare, Docstrings und TUI-/Ausgabetexte.
- Eigennamen (`Boukensha`, `MudManager`) und Python-idiomatische (englische) Bezeichner bleiben.

## 2. Leitplanken (NICHT verletzen)
- **`.boukensha/` bleibt komplett unangetastet.** Nicht anlegen, ändern oder löschen.
- **Bestehende `.rb`-Dateien werden NICHT nach Python übersetzt und NICHT verändert.**
  Insbesondere das Ruby-Gem `week0_explore/mud_manager/` bleibt unverändert und wird
  nicht ersetzt.
- **Nur additive, neue Python-Erweiterungen.** Im Architektur-Diagramm als Ruby gezeigte
  Bausteine (`agent.rb`, `repl.rb`, `tui.rb`, …) existieren noch nicht als Dateien und
  werden als **neue** Python-Module angelegt — das ist keine Übersetzung.
- **Vorhandener Python-Code wird wiederverwendet, nicht verändert:**
  `week0_explore/mud-mcp/mud_mcp/session.py` (MudManager/Telnet) bleibt wie er ist;
  neue Module **importieren** ihn nur.
- **Neuer Code liegt in `week0_explore/boukensha/`** (nicht in `.boukensha/`).

## 3. Architektur-Quelle
- **Quelle der Wahrheit:** `docs/plans/Claude Code Camp Agent Architecture - Baseline.json`
  (maschinenlesbar). Die `.svg`/`.png` sind dasselbe als Bild.
- Umsetzung/Übersetzung der Architektur nach Python: `boukensha_architecture_python.md`.

## 4. LLM-Modell (Agent-Backend)
- **Primär: Claude Haiku 4.5** (`claude-haiku-4-5-20251001`).
- **Alternative: Sonnet 4.6** (in `settings.yml` umschaltbar).
- **Nicht** das „neueste/Default"-Modell verwenden.
- Exakte Modell-ID vor der Verdrahtung bestätigen (bekannt: Haiku 4.5, Sonnet 5, Opus 4.8).

## 5. MUD-Spielregeln (Sicherheit, aus Erfahrung/Log)
- Niemals `cityguard`/`Peacekeeper`/`knight`/`sorcerer` angreifen.
- Wachen **helfen** angegriffenen Mobs und **wandern** in Räume hinein → bei
  „… has arrived" während eines Kampfs **sofort `flee`** (Puffer-Latenz einkalkulieren).
- Nur **einzelne** Fidos angreifen; Kadaver **sofort** looten.
- Nicht in die Kanalisation (Sewer) gehen. Idle-Zeiten kurz halten (sonst „Void").
- Details/Route: `../../week0_explore/logs/mud-session-2026-07-12.md`.
