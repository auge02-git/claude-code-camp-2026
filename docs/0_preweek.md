# 0 Preweek - Erkenntnisse und Doing (Stand: 2026-07-17)

## Hinweis zur Quelle
Ein Ordner `dcos` wurde im Workspace nicht gefunden. Diese Zusammenfassung basiert auf den Inhalten in `claudeCodeCamp/docs` (insbesondere `claudeCodeCamp/docs/plans`).

## Zentrale Erkenntnisse
- Die Boukensha-Architektur ist dokumentiert und als Python-Grundgeruest umgesetzt.
- Das Agenten-Setup laeuft grundsaetzlich (Tool-Loop, Logging, MUD-Anbindung).
- Login- und Reconnect-Pfade wurden stabilisiert; typische Start-/Reconnect-Faelle sind abgedeckt.
- Prompt-Caching wurde getestet; bei ausreichend grossem Prompt-Praefix sind Cache-Treffer sichtbar.
- Fehlerbehandlung fuer Auth-/Billing-Probleme wurde verbessert (sauberer Exit statt unklarer Tracebacks).
- Der autonome Farm-Loop wurde zwischenzeitlich gestoppt (kein aktiver Dauerlauf).

## Doing (zuletzt in Arbeit / zuletzt abgeschlossen)
- Agentenlauf mit Tool-Use erfolgreich durchgespielt (`look` -> `score` als typische Folge).
- Login-Robustheit verbessert (Reconnecting und frischer Login).
- Prompt-Caching-Verhalten mit unterschiedlichen Modell-/Prompt-Konstellationen validiert.
- Auth-Flow vereinfacht auf env-basierten API-Key-Ansatz.
- Runtime-Fehlerpfade zentral abgefangen und benutzerfreundlicher gemacht.

## Offene To-dos (naechste Schritte)
1. `ANTHROPIC_API_KEY` setzen und echten Live-Lauf starten.
2. Modell-ID/Fallback final pruefen und konsistent konfigurieren.
3. Optional: Farm-Loop wieder aufnehmen und Progress auf Level 2 planen.
4. Optional: Reflect-Schritt im Agentic-Loop weiter schaerfen.

## Relevante Dateien
- `claudeCodeCamp/docs/plans/00_fortsetzen_hier.md` (Live-Status, naechste Schritte)
- `claudeCodeCamp/docs/plans/umsetzung.md` (technische Umsetzung, Tests, Fixes)
- `claudeCodeCamp/docs/plans/boukensha_architecture_python.md` (Architektur)
- `claudeCodeCamp/docs/plans/week0_dummy_level-and-skills.md` (MUD-Fortschritt)

## Offene Doku-Luecken
- `claudeCodeCamp/docs/README.md` ist aktuell nur ein Platzhalter.
- `claudeCodeCamp/docs/1_baseline.md` ist leer.
- `claudeCodeCamp/docs/2_capable.md` ist leer.

