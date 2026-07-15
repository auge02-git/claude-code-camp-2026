---
name: boukensha-safe-farm
description: Stabilize a low-level Boukensha run in Midgaard, reach the fountain, farm fido safely at Eastern End Of Poor Alley, and avoid dangerous guard encounters. Use when the user wants a reproducible early-game survival and farming loop for the dummy character.
---

# Boukensha Safe Farm

Hilft bei einem stabilen, risikoarmen Frühspiel-Lauf für `dummy` im CircleMUD/tbaMUD.
Die Skill überführt die Erkenntnisse aus `week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v3.md`
in eine direkt nutzbare Spielanweisung.

Sie ergänzt die bestehende Skill `mud-play` und fokussiert auf:
- sichere Orientierung in Midgaard
- schnelles Erreichen des Brunnens
- konservatives Farming von `fido`
- Vermeidung von Wachen und Endlosschleifen
- sauberes Sichern des Fortschritts

## Voraussetzungen

- Der MUD läuft auf `localhost:4000`
- Login mit `dummy` / `helloworld`
- Für Verbindung und Roh-Kommandos kann die bestehende Skill `mud-play` verwendet werden
- Optionales Hilfsskript: `week0_explore/explore_architecture/02_agent_skills/.claude/scripts/boukensha_safe_farm.py`

## Gesicherte Navigationsanker

Nutze diese Punkte als harte Referenz:

- `Common Square` -> `west` -> `Poor Alley`
- `Common Square` -> `north` -> `Temple Square`
- `Eastern End Of Poor Alley` ist der wichtigste Farm-Anker
- `Poor Alley` -> `south` -> `Grubby Inn`

## Harte Sicherheitsregeln

1. Niemals Wachen oder Hochrisiko-NPCs angreifen:
   - `cityguard`
   - `Peacekeeper`
   - `knight`
   - `sorcerer`
   - `Mayor`
2. Wenn im Output `has arrived` auftaucht und Gefahr möglich ist: sofort `flee`.
3. Kämpfe nur gegen einzelne, schwache Ziele wie `fido`.
4. Priorität immer: Wasser -> Hunger -> Überleben -> Gold/Exp.
5. Bei knappem HP-Puffer früh `flee`, nicht erst im roten Bereich.
6. Keine zufälligen Bewegungsfolgen in zentralen Räumen.
7. Kein Richtungs-Spam aus unklarer Position.

## Standard-Startsequenz

Beginne jeden Lauf mit:

```text
score
look
```

Ziel dieser Sequenz:
- Standort bestätigen
- HP/Move prüfen
- unmittelbare Gefahr erkennen

## Brunnen schnell erreichen

Verwende nur bestätigte Wege:

### Wenn du im `Donation Room` startest

```text
west
south
drink fountain
```

### Wenn du auf `Market Square` bist

```text
north
drink fountain
```

### Wenn du bereits auf `Temple Square` bist

```text
drink fountain
```

## Vom Zentrum ins Farmgebiet

Sobald Wasser gesichert ist, gehe Richtung Farm-Anker:

```text
south
west
```

Das Ziel ist `Eastern End Of Poor Alley`.
Wenn der Raumname noch nicht passt, prüfe mit `look` und korrigiere konservativ statt zu raten.

## Farm-Loop in `Eastern End Of Poor Alley`

Arbeite pro Begegnung in genau dieser Reihenfolge:

```text
look
kill fido
get all corpse
eat meat
```

Optional alle 3–4 Zyklen zusätzlich:

```text
score
```

### Wenn kein `fido` da ist

Nur kurz pendeln und sofort neu prüfen:

```text
east
look
west
look
```

Keine langen Suchläufe durch die Stadt.

## Gefahrenreaktion

Wenn Wachen, unklarer Output oder mehrere Gegner auftauchen:

```text
flee
look
```

Danach nur dann zurück zum Farmen, wenn die Lage wieder eindeutig ist.

## Fortschritt sichern

Wenn mehrere sichere Kills erfolgt sind oder ein spürbarer Exp-Fortschritt erreicht wurde:

```text
quit
```

Nur an einem sicheren Zeitpunkt beenden — nicht mitten in Gefahr oder direkt nach chaotischem Raumwechsel.

## Empfohlene Arbeitsweise mit `mud-play`

Die Skill `mud-play` kümmert sich um Verbindung und Login.
Diese Skill liefert die Taktik.

Typischer Ablauf:
1. Verbinden und einloggen
2. `score` + `look`
3. Brunnen erreichen und `drink fountain`
4. Zu `Eastern End Of Poor Alley`
5. `fido`-Farm-Loop ausführen
6. Bei Gefahr `flee`
7. Bei gutem Fortschritt `quit`

## Hilfsskript

Das Skript `boukensha_safe_farm.py` liefert vorbereitete Befehlsfolgen als Referenz,
ohne blind zu automatisieren.

Beispiele:

```sh
python3 week0_explore/explore_architecture/02_agent_skills/.claude/scripts/boukensha_safe_farm.py --list
python3 week0_explore/explore_architecture/02_agent_skills/.claude/scripts/boukensha_safe_farm.py start-check
python3 week0_explore/explore_architecture/02_agent_skills/.claude/scripts/boukensha_safe_farm.py full-run-market --format json
```

## Kurz-Checkliste

- [ ] `score` und `look` zu Beginn ausgeführt
- [ ] Brunnen erreicht und `drink fountain` bestätigt
- [ ] `Eastern End Of Poor Alley` erreicht
- [ ] Mindestens ein kompletter Zyklus: `kill` -> `get all corpse` -> `eat meat`
- [ ] Bei Gefahr korrekt `flee`
- [ ] Fortschritt an sicherer Stelle mit `quit` gesichert

## Anti-Pattern

Vermeide konsequent:
- Schleifen zwischen `Common Square`, `Market Square` und `Poor Alley`
- Serien aus `look` ohne Folgeaktion
- langes Herumlaufen im Zentrum
- zufälliges `west`-Spamming nahe Wachenpfaden
- Kampfaufnahme ohne bestätigtes Einzelziel

