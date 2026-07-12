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
- **Noch NICHT gebaut:** Paket-Gerüst unter `week0_explore/boukensha/` — **wartet auf Go**.

## Nächste Schritte (Priorität)
1. **Boukensha-Gerüst anlegen** in `week0_explore/boukensha/` gemäß Blaupause
   (pyproject + Agentic Loop + config/logger/context/registry + `mud.py`-Wrapper).
   Backend-Modell: **Haiku 4.5** (Alt.: Sonnet 4.6). *Leitplanken beachten (siehe `vorgaben.md`).*
2. **Farmen fortsetzen** bis Level 2 (oder Ansatz ändern: größeres Intervall / Sewer freigeben).
3. **Nach Level-Up:** neue Krieger-Skills im Practice Yard (Raum 3023) lernen
   (`practice`), z. B. bash/rescue/second attack.
4. Optional: `log_viz` (FastAPI) + `run_dsl` ergänzen.

## Wichtige Wiederanlauf-Kommandos
```sh
# MUD-Server läuft?
docker ps | grep circlemud
# MCP-Server-Code (Login/Session): week0_explore/mud-mcp/
# Architektur als Bild rendern:
cd docs/plans && rsvg-convert -w 2000 "Claude Code Camp Agent Architecture - Baseline.svg" -o arch.png
```
