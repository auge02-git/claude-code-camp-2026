# 00 — HIER FORTFAHREN (Einstieg für die nächste Sitzung)

Diese Datei ist der **Startpunkt**, um an genau dieser Stelle weiterzumachen.
Zuerst lesen, dann bei „Nächste Schritte" ansetzen.

Stand: **2026-07-12**.

## Dokumente in diesem Ordner
| Datei | Inhalt |
|---|---|
| `00_fortsetzen_hier.md` | **diese Datei** — Live-Zustand + nächste Schritte |
| `vorgaben.md` | **alle Vorgaben/Leitplanken** (Baseline, Guardrails, Modell) |
| `umsetzung.md` | **Umsetzungsstand** — was bereits gebaut wurde (Datei für Datei) |
| `boukensha_architecture_python.md` | Architektur-Blaupause (JSON → Python-Module) |
| `week0_dummy_level-and-skills.md` | Spielplan: `dummy` leveln/Skills + Fortschritts-Log |
| `Claude Code Camp Agent Architecture - Baseline.json` | **Quelle der Wahrheit** der Architektur (Lucidchart) |
| `… - Baseline.svg` / `… .png` | dieselbe Architektur als Bild |

> SVG-Text ist als Vektor-Glyphen kodiert (nicht als Text lesbar). Zum Ansehen als
> Bild rendern: `rsvg-convert -w 2000 "…Baseline.svg" -o arch.png`, dann öffnen.
> Für Maschinenlesbarkeit die **`.json`** nutzen.

## Live-Zustand (zum sofortigen Weitermachen)

### A) MUD-Charakter `dummy`
- Krieger, **Level 1**, **336 Exp** (noch ~1664 bis Level 2), **20 Gold**.
- Skill **kick** gelernt (`kick (bad)`); **voll ausgerüstet** (small sword etc.).
- **Gespeichert** über kostenlose Rent (`quit` beim Rezeptionisten in *The Reception*).
- Login: MCP-Tools `mud_connect()` + `mud_login()` **ohne Argumente** (nutzt `credentials.json`).
- Sicherheitsregeln beim Spielen: siehe `week0_dummy_level-and-skills.md` und
  `../../week0_explore/logs/mud-session-2026-07-12.md`.

### B) Autonomer Farm-Loop
- Cron-Job **`f40a8f93`**, `*/5 * * * *`, farmt Fidos bis Level 2, dann Stopp+Sicherung.
- **Session-only** (endet mit der Claude-Sitzung), läuft max. 7 Tage.
- Abbrechen: `CronDelete` mit ID `f40a8f93`.
- Realität: Fidos sind spärlich/wandernd + roamende Wachen → Fortschritt langsam.
  Ergiebigster Spawn: Raum **3024** (Eastern End of Poor Alley).

### C) Architektur-Arbeit (Boukensha-Agent)
- **Blaupause fertig** (`boukensha_architecture_python.md`), leitplanken-konform.
- **Gerüst GEBAUT + IN BETRIEB GENOMMEN** unter `week0_explore/boukensha/`:
  `uv sync` ok, Verdrahtungs-Smoke-Test ok (9 Werkzeuge, Haiku 4.5), MUD-Pfad
  ohne LLM live getestet (connect/login/look/score/quit), Agent-Home
  `~/.boukensha` angelegt (`settings.yml` + deutscher `prompts/system.md`),
  README geschrieben. Details: `umsetzung.md` Abschnitt E.
- **Farm-Loop `f40a8f93` wurde GESTOPPT** (CronDelete) — läuft nicht mehr.

## Nächste Schritte (Priorität)
1. **Echter Live-Lauf mit LLM:** `cd week0_explore/boukensha`, `export ANTHROPIC_API_KEY=…`,
   dann `uv run boukensha` (verbindet + loggt via `credentials.json` ein → REPL).
   (Key war beim letzten Test nicht in der Shell gesetzt — nur das fehlte noch.)
2. **Modell-ID Sonnet 4.6 final bestätigen** (`config.py:ALT_MODEL` = `claude-sonnet-4-6`).
3. Optional: Feinschliff Agentic Loop (expliziter Reflect-Schritt).
4. Optional/später: MUD-Farmen wieder aufnehmen (Level 2) — Ansatz ggf. anpassen
   (größeres Intervall / Sewer), da 5-Min-Loop bei spärlichen Fidos zäh war.

## Wichtige Wiederanlauf-Kommandos
```sh
# MUD-Server läuft?
docker ps | grep circlemud
# MCP-Server-Code (Login/Session): week0_explore/mud-mcp/
# Architektur als Bild rendern:
cd docs/plans && rsvg-convert -w 2000 "Claude Code Camp Agent Architecture - Baseline.svg" -o arch.png
```
