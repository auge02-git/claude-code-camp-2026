# Arbeitsanweisung fuer Boukensha-Agent (dummy, Level 1)

- Quelle: `../../logs/hand-agent-output-2026-07-15_2.log` (61 Schritte)
- Stand: 2026-07-15
- Ziel: Stabil ueberleben, effizient farmen, Schleifen vermeiden

## Kern-Erkenntnisse

- Navigation war das groesste Problem: viele Schleifen zwischen `Common Square`, `Market Square` und `Poor Alley`.
- Kritischer Engpass: Brunnen wurde trotz Naehe oft nicht effizient erreicht.
- Farm-Fortschritt blieb aus: kein gesicherter `fido`-Kill im Lauf.
- Wachen-Risiko war hoch: mehrfach `cityguard`/`Peacekeeper` in Transitraeumen.
- `Void`-artige Zustandsverluste traten auf, vermutlich durch falsche Bewegungssequenzen bzw. Leerlauf.

## Gesicherte Navigationsanker

- `Common Square` -> `west` -> `Poor Alley` (Eingang)
- `Common Square` -> `north` -> `Temple Square` (Brunnen)
- `Eastern End Of Poor Alley` (3024) ist der wichtigste Farm-Anker
- `Poor Alley` -> `south` -> `Grubby Inn`

## Harte Sicherheitsregeln

1. Nie Wachen angreifen (`cityguard`, `Peacekeeper`, `knight`, `sorcerer`, `Mayor`).
2. Bei Meldung `has arrived` und Gefahr sofort `flee`.
3. Kaempfe nur gegen einzelne, schwache Ziele (`fido`) in peripheren Raeumen.
4. Prioritaet: Wasser > Hunger > Gold/Exp.
5. Bei niedrigem HP-Puffer frueh ausweichen (`flee`), nicht spaet.

## Operativer Plan fuer den naechsten Lauf

### Phase 1 - Stabilisieren

1. `score` und `look` fuer Standort + Zustand.
2. Schnell zum Brunnen:
   - wenn `Donation Room`: `west` -> `south` -> `Temple Square` -> `drink fountain`
   - wenn `Market Square`: `north` -> `Temple Square` -> `drink fountain`
   - wenn schon `Temple Square`: direkt `drink fountain`
3. Danach Richtung Farmgebiet:
   - `Temple/Market` -> `south` -> `Common Square` -> `west` -> `Eastern End Of Poor Alley`

### Phase 2 - Farm-Loop in 3024

- Zyklus je Begegnung:
  1. `look`
  2. `kill fido` (nur wenn sicher)
  3. `loot_corpse`
  4. `eat meat`
  5. alle 3-4 Zyklen `score`
- Wenn kein `fido`: zwischen `Eastern End Of Poor Alley` und benachbartem `Poor Alley` kurz pendeln (`east/west`) und erneut `look`.
- Bei Wache/unsicherem Output: sofort raus (`flee`) und zurueck nach 3024.

### Phase 3 - Fortschritt sichern

- Nach einigen sicheren Kills/Exp-Delta Spielstand sichern (`quit` bei sicherer Rueckkehr).
- Skill-Training erst nach Level-Up in `Practice Yard`.

## Fehlerbild aus dem Lauf (vermeiden)

- Kein zufaelliges Richtungsraten in Transitraeumen.
- Keine langen `look`-Serien ohne Folgeaktion.
- Keine langen Umwege im Zentrum.
- Kein `west`-Spam von unklaren Positionen nahe Wachenpfaden.

## Kurz-Checkliste (maschinell nutzbar)

- [ ] Start: `score` + `look`
- [ ] Brunnen erreicht und `drink fountain` bestaetigt
- [ ] `Eastern End Of Poor Alley` erreicht
- [ ] Mindestens ein kompletter Farm-Zyklus (`kill` -> `loot` -> `eat`)
- [ ] Bei Gefahr korrekt `flee`
- [ ] Fortschritt per `quit` gesichert

