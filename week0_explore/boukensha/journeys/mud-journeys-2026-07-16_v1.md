# MUD-Session-Plan v9 - Midgaard (tbaMUD)

## Zweck
Diese Datei strukturiert die Arbeitsanweisungen so, dass ein Agent sie deterministisch ausfuehren kann.
Ziel: schnelleres Leveln (naechstes Level), mehr EXP pro Minute, weniger Sackgassen, sicherer Fortschritt.

## Eingaben (vor Start lesen)
1. `../../../docs/plans/week0_dummy_level-and-skills.md` (Leveling-Plan, Skill-Lernreihenfolge, Grundlagen)
2. `references/commands.md` (Funktionen und Befehle im Spiel)
3. `journeys/mud-journeys-2026-07-15_v11.md` (Grundregel und Erfahrungen)
3. `journeys/erfahrung_durchlaeufe_v10.txt` (Zusammenfassung Erkenntnisse, letztes)
4. `journeys/mud-journeys-2026-07-15_v1.log` (Karte / reale Bewegungshistorie)
5. `../../logs/mud-journeys-2026-07-16_v4.log` (nur als optionale Auswege, als subagents nutzen `/btw`, nicht als Pflichtplan)

## Ausgabe-Vertrag
- Jede Ausgabezeile = genau ein Agenten-Ziel (ein Schritt-Budget).
- Jede Zeile enthaelt genau eine klare Aktion oder Entscheidung.
- Sicherheitsregeln haben immer Vorrang vor EXP-Zielen.
- Exits strikt auswerten: nur Richtungen nutzen, die bei `Exits:` angezeigt werden.

## Harte Sicherheitsregeln (nicht verhandelbar)
1. Niemals angreifen: `cityguard`, `Peacekeeper`, `knight`, `sorcerer`, `Mayor`.
2. Bei `has arrived` sofort `flee` (kein `look`, kein `score`, kein `kick` davor).
3. Keine Kaempfe auf Main Street oder in offensichtlichen Patrouillen-Transitraeumen.
4. Vor jedem Kampf: `look` -> Wachencheck -> Exits lesen -> Fluchtweg festlegen.
5. Prioritaet: Wasser > sichere Position > Hunger > Gold/EXP.
6. Exits sind bindend. Keine unbestaetigten Richtungen raten.

## Navigationsanker (aus Log validiert)
- Sichere Basis: Temple Square / Common Square.
- Farm-Anker: Eastern End Of Poor Alley (3024), Poor Alley (3012/Umfeld).
- Risiko-Zonen: East Gate (geschlossenes Tor moeglich), Main Street (Wachen).
- Water Shop ist moeglich, aber nicht zuverlaessiger als Temple-Fountain.

## Standard-Loop (Pfad mit geringem Risiko)
### Phase A - Stabilisieren
1. `score`
2. `look`
3. Falls durstig: zum Temple Square navigieren und `drink fountain`.
4. Wenn Position unklar: nur ueber bekannte Anker raeumeweise stabilisieren (`look` nach jedem Schritt).

### Phase B - Sicher zur Farm
1. Ueber Common Square Richtung Poor Alley bewegen.
2. Nach jedem Raumwechsel `look`.
3. Bei Wache im Raum: kein Kampf, Raum wechseln.

### Phase C - Farm-Zyklus
1. `look`
2. Wenn genaues, kontrollierbares Ziel da (bevorzugt `fido`) und Raum wachfrei:
   - `kill fido`
   - optional beschleunigen: `kick fido` (nur wenn Lage weiter sicher)
   - `get all corpse`
   - `eat meat`
3. Alle 3-4 Kaempfe `score`.
4. Wenn kein passendes Ziel da: nur kurz zwischen benachbarten sicheren Raeumen pendeln, dann erneut `look`.

### Phase D - Notfall
1. Trigger: `has arrived`, Wache sichtbar, HP fallen schnell, Exits unklar.
2. Sofort: `flee`
3. Dann: `look`
4. Neu stabilisieren und auf sichere Route zurueck.

## Anti-Sackgasse-Regeln
- Bei `The gate seems to be closed` nicht spammen.
- Erst `look` + `score`, dann nur gelistete Alternativ-Exits testen.
- Keine langen Experimente an geschlossenen Toren.
- Schnell zur sicheren Route Temple -> Common -> Poor Alley zurueck.

## ATM-Regel (Geld sichern)
- ATM nutzen, sobald eine sichere Phase erreicht ist (kein Kampf, keine Wache im Raum, Route bekannt).
- ATM-Befehle zum pruefen (balance), abzuheben (withdraw <summe>) dann Geld einzahlen (deposit <summe>).
- Nur abheben, wenn ein konkreter Kauf ansteht.

## Planungsregel pro Schritt
- Immer 3-5 Aktionen vorausdenken (Mini-Route), nicht nur auf letzte Zeile reagieren.
- Beispiel: `look -> west -> look -> kill fido -> kick fido -> get all corpse -> eat meat -> score`.

## /btw-Regel (optionale Auswege)
- Erkenntnisse aus `mud-journeys-2026-07-15.log` nur als optionale Alternative verwenden.
- `/btw` darf den Hauptplan nur ersetzen, wenn er sicherer oder klar effizienter ist.

## Abschluss pro Lauf
1. `score`
2. Kurzstatus ausgeben (Ort, HP/MV, Hunger/Durst, EXP-Fortschritt, Gold, Risiken).
3. Fortschritt an sicherer Stelle sichern (`quit`).

## Neustart
- Ablauf erneut mit `/loop` starten.
- Wenn es keine Optionen mehr gibt benutzte die Informationen aus `references/commands.md` um weiter Befehl und Aktionen zu erhalten und versuche deren Verwendung zu lernen und zu nutzen.
- Wenn du in einer undefinierten Situation bist, lade die Daten aus `../../logs/.logging_data/*` und versuche mit dem Informationen aus `world.md` zu navigieren.
- Jede neue Schleife soll kuerzer, sicherer und EXP-effizienter sein als die vorherige.

