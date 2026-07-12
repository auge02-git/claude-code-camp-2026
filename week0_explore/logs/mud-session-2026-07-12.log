# MUD-Session-Log — Midgaard (tbaMUD)

- **Datum:** 2026-07-12
- **Charakter:** `dummy` (Login: `dummy` / `helloworld`), Klasse **Krieger** ("Swordpupil"), Level 1
- **Server:** localhost:4000 (Docker-Container `circlemud`)
- **Zugriff:** MCP-Server `mud` (Tools `mud_connect`, `mud_send`, `mud_read`, ...)
- **Ziele:** Wasser trinken · etwas essen · Skill **kick** lernen · Marktplatz finden

> **Zweck dieses Logs:** Die Route ist Raum für Raum nachlaufbar. Monster sind als
> 🟢 **SCHWACH** (gefahrlos tötbar) oder 🔴 **STARK** (niemals angreifen) markiert.

---

## ⚠️ WICHTIGSTE WARNUNG (aus zwei Toden gelernt)

In allen **Gilden- und Wach-Räumen** steht ein 🔴 **Peacekeeper**. Er greift
sofort **jeden** an, der in seinem Raum ein Monster (auch einen schwachen Fido)
attackiert — *"The Peacekeeper jumps to the aid of ..."* — und tötet einen
Level-1-Charakter in wenigen Runden. **Niemals in einem Raum mit Peacekeeper/
Wache kämpfen.** Fidos nur in Räumen töten, in denen KEINE Wache steht.

---

## Monster-Legende

| Symbol | Monster | Einschätzung | Beute / Hinweis |
|--------|---------|--------------|-----------------|
| 🟢 SCHWACH | **beastly fido** | ~19 HP, richtet kaum Schaden an, in ~4 Runden tot (mit Waffe, 0 Schaden genommen) | **~10 Gold + ein Stück Fleisch** (Fleisch = Essen!). Beste Gold-/Essensquelle für Neulinge. Kadaver **sofort** looten — ein anderer Fido frisst ihn sonst. |
| 🔴 STARK | **Peacekeeper** | Tödlich: ~5–8 Schaden/Treffer, tötet Level-1 in Sekunden. Hilft JEDEM Monster, das man in seinem Raum angreift. | Nicht angreifbar. Auslöser für beide Tode. |
| 🔴 STARK | **cityguard** | Stadtwache, stark, beschützend | Nicht angreifen. |
| 🔴 STARK | **a knight** (Gildenwache 3021) | Wächter der Krieger-Gilde | Nicht angreifen. |
| 🔴 STARK | **a sorcerer** (Magier-Gilde) | blockiert Süd-Ausgang der Magier-Gilde | Nicht angreifen. |
| ⚪ neutral | **janitor, waiter, wizard (Shop), baker, kind soul** | NPCs/Händler, harmlos | Händler nicht angreifen. `janitor` sammelt herumliegende Items ein! |
| 🟡 unklar | **green gelatinous blob**, **the Mayor** | wandernd, nicht getestet | Im Zweifel meiden. |

---

## Route (nachlaufbar, Richtungsangaben)

Startpunkt nach Login = **The Entrance To The Mages' Guild** (Raum 3017).
Ausgänge n,s — **Süd blockiert** die 🔴 sorcerer-Wache.

| # | Kommando | Zielraum | Notizen / Monster |
|---|----------|----------|-------------------|
| 1 | `north` | Main Street (Ende, 3012) | 🟢 beastly fido(s). n=Magic Shop (Sackgasse), w=Stadttor, s=Magier-Gilde |
| 2 | `east` | Main Street (3013) | n=**Bakery**, s=Armory, e=Markt |
| 3 | `east` | **Market Square** (3014) | ⭐ **MARKTPLATZ** — "the famous Square of Midgaard". n=Temple, s=Common, e/w=Main St |
| 4 | `north` | **Temple Square** (3005) | 💧 **Brunnen** (Fountain)! w=Clerics-Gilde, e=Grunting Boar Inn, n=Temple. 🔴 Peacekeeper, ⚪ janitor |
| — | `drink fountain` | — | ✅ **Wasser** — "You don't feel thirsty any more." (kostenlos, beliebig oft) |
| 5 | `south` | Market Square | zurück |
| 6 | `west` | Main Street (3013) | Bakery im Norden |
| 7 | `west` | Main Street (Ende, 3012) | 🟢 beastly fido(s) — **hier gefahrlos kämpfen (keine Wache)** |
| — | `kill fido` → `get all corpse` → `eat meat` | — | ✅ **10 Gold + Fleisch**; Fleisch gegessen ✅ **Essen** erledigt |

### Bäckerei-Preise (Bakery, `north` von Raum 3013, dann `list`)
| Ware | Preis |
|------|-------|
| A danish pastry | 7 Gold |
| A bread | 14 Gold |
| A waybread | 74 Gold |

*(Mit den 10 Gold aus dem Fido ließe sich ein Danish kaufen — dank Fleisch nicht nötig.)*

---

## Weg zur Krieger-Gilde (Skill **kick** lernen)

Die Krieger-Gilde heißt hier **"Guild of Swordsmen"**. Der **fighters' guildmaster**
(Mob 3023) steht im **Practice Yard** (Raum 3023). Ermittelt aus den Weltdateien
(`infrastructure/lib/world/wld/30.wld`, `zon/30.zon` Zeile 127).

| # | Kommando | Zielraum | Monster |
|---|----------|----------|---------|
| 1 | von Market Square `east` | Main Street (3015) | general store n, pet shop s |
| 2 | `east` | Main Street (3016) | 🔴 **Peacekeeper** + 🟢 fidos — **HIER NICHT KÄMPFEN!** s=Guild of Swordsmen |
| 3 | `south` | Entrance Hall Guild of Swordsmen (3021) | 🔴 knight, 🔴 cityguard, ATM |
| 4 | `east` | Bar of Swordsmen (3022) | ⚪ waiter |
| 5 | `south` | **Tournament & Practice Yard** (3023) | ⭐ **guildmaster** ("standing here sharpening an axe") |
| — | `practice` | — | "1 practice session remaining", `kick (not learned)` |
| — | `practice kick` | — | ✅ **kick gelernt** → `kick (bad)` |

Verifikation: `kick fido` →
*"Your beautiful full-circle kick misses the beastly fido by a mile."*
→ Skill wird ausgeführt (Treffer verfehlt wg. niedriger Proficiency "bad").

---

## ☠️ Fehler-Protokoll (nicht wiederholen)

1. **Kick-Test in Raum 3016** (mit Peacekeeper): Fido angegriffen → Peacekeeper
   sprang bei → Tod (Flucht kam durch Puffer-Latenz zu spät). Ausrüstung fiel in
   die Leiche.
2. **Bergung im selben Raum**: nackt/barhändig erneut einen Fido angegriffen →
   Peacekeeper kehrte zurück → **zweiter Tod**. Originale (getunte) Ausrüstung
   von einem Fido gefressen → vermutlich verloren.
3. **Respawn:** Temple of Midgaard (Recall-Raum), 1 HP, nackt. Nebenan Osten =
   **Donation Room** (kostenlose Ausrüstung für Nackte, gefahrlos).

**Regeln fürs nächste Mal:**
- Nur in wachfreien Räumen kämpfen (z. B. Raum 3012 Main-Street-Ende).
- Fido-Kadaver sofort looten (`get all corpse`), sonst frisst ihn ein anderer Fido.
- Bei `flee` die Latenz einkalkulieren — früh fliehen, nicht erst bei niedrigen HP.

---

## Technischer Hinweis: MCP-Login-Bug

`mud_login` ist defekt: `mud_connect` konsumiert den Namens-Prompt (server.py:53),
`session.login()` wartet danach erneut darauf (session.py:209) → Timeout.
**Workaround:** Login manuell über `mud_send` treiben — `mud_send("dummy")`,
dann `mud_send("helloworld")`.
