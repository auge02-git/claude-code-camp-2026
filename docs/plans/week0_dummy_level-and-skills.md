# Plan — dummy: leveln, ausrüsten, neue Skills lernen

- **Charakter:** `dummy` (Krieger, Level 1, Swordpupil), zuletzt gesichert in The Reception
- **Status (Stand 2026-07-12):** 236 Exp · 10 Gold · **0 Übungssessions** · nackt (Ausrüstung bei Toden verloren)
- **Basis:** `week0_explore/logs/mud-session-2026-07-12.md` (Route + Monster-Markierungen)

## Kernerkenntnis
Neue Skills sind **erst nach einem Level-Up** möglich (Practice-Sessions gibt es nur
beim Aufstieg). Reihenfolge daher: **ausrüsten → leveln → lernen.**

## Schritt 0 — Ausrüsten ✅ ERLEDIGT (Korrektur!)
`dummy` ist **doch voll ausgerüstet** — die Ausrüstung ging bei den Toden NICHT
verloren, sie wird mit dem Charakter gespeichert und war nach `quit`/Reconnect
wieder da: small sword (wielded), breast plate, Schild, 2 leather rings, cap,
bronze leggings, boots, gloves, sleeves, cape, belt, 2 wristguards, metal staff,
candle (Licht). → Fido-Kills gehen schnell (0 Schaden). Kein Ausrüsten nötig.

## Schritt 1 — Exp farmen bis Level 2 (braucht 1764 Exp)
- **Farm-Ort:** **The Dump** (2× s vom Markt) — peripher, meist **1 einzelner** Fido,
  Kadaver bleibt liegen (Gold + Fleisch).
- ~33 Exp/Fido → viele Kills; auf Hunger/Durst achten (Brunnen Temple Square; Fleisch essen).
- **Wach-Regeln (aus Log, zwingend):**
  - Nie in Gilden-/Wachräumen kämpfen (z. B. Raum 3016).
  - Nur **einzelne** Fidos angreifen.
  - Bei `cityguard`/`Peacekeeper` **"has arrived"** im Kampf → **sofort `flee`** (Latenz beachten!).

## Schritt 2 — Neue Warrior-Skills lernen (nach Level-Up)
- Zum **Practice Yard** (Guild of Swordsmen, Raum 3023): Markt → e → e (3016, NICHT kämpfen)
  → s → e → s. Dort `fighters' guildmaster`.
- `practice` zeigt lernbare Skills; Kandidaten: **bash, rescue, kick verbessern, track, second attack**.
- Pro Session einen Skill mit `practice <skill>` lernen.

## Schritt 3 — Erkundung (kampffrei, parallel)
- Poor Alley (w), Dark Alley (e → Thieves' Guild), Reading Room (w vom Temple),
  Cryogenic Center (n von Reception), Post Office/Bar im Inn, General Store/Pet Shop.
- **Meiden:** Kanalisation (`d` vom The Dump) — stärkere Mobs, für Level 1/nackt riskant.

## Schritt 4 — Sichern
- Regelmäßig zum Rezeptionisten (The Reception) und **`quit`** (Rent ist gratis, speichert alles).

## Abbruchkriterien / Sicherheit
- HP < ~30 % → `flee` + rasten.
- Zweifel an einem Mob → nicht angreifen.
- Nach jedem Level-Up: erst sichern (`quit`/reconnect), dann weiter.

---

## Fortschritts-Log (wird beim Spielen aktualisiert)
- 2026-07-12: Plan angelegt. Ausgangspunkt 236 Exp / 10 Gold / Level 1, in The Reception.
- 2026-07-12: **Korrektur:** dummy ist voll ausgerüstet (Schritt 0 entfällt).
- 2026-07-12: **Fido-Spawns** laut `zon/30.zon`: Räume **3012, 3016, 3024, 3025**
  (max 15 in Zone). 3016 = Peacekeeper → meiden.
- 2026-07-12: **Praktisches Problem:** Fidos wandern und sind oft nicht am Spawn;
  Grind auf Lvl 2 (≈53 Kills) manuell über das laggy MCP-Interface zu teuer.
  → Empfehlung: entweder autonomer **/loop** (Farmen über Zeit) oder Fokus auf
  kampffreie Erkundung (Schritt 3), Leveln als Hintergrundaufgabe.
- Bei Idle wird man **in die Void** gezogen (Puff) — kein Schaden, ein Kommando
  bringt einen zurück; lange Wartezeiten vermeiden.
- **Autonomer /loop eingerichtet** (Job `f40a8f93`, alle 5 Min) zum Fido-Farmen bis Lvl 2.
- **Wichtig — bester Spawn:** Raum **3024 „Eastern End of Poor Alley"** (Common Square → w)
  hatte 3 Fidos, während 3012/Common/Dump leer waren. Dort zuerst suchen! Peripher, kein
  Wächter, oft liegt zusätzlich ein Stück Fleisch am Boden.
- **Iteration 2026-07-12 #2:** 3 Fidos in 3024 erlegt → **Exp 236 → 336**, **Gold 10 → 20**,
  1 Fleisch im Gepäck. Kein Schaden. (Noch ~1664 Exp bis Lvl 2.)
