# Boukensha Agent Running Instructions
## MUD Session Plan v9 - Midgaard (tbaMUD)

---

## Purpose

This document structures the work instructions so that an agent can execute them deterministically. 

**Goal:** Faster leveling (reach next level), more experience per minute, fewer dead ends, safer progress.

---

## Inputs (Read Before Starting)

1. `journeys/erfahrungen_durchlaeufe_v5.txt` — experiential learnings from run v5
2. `journeys/erfahrung_durchlaeufe_v6.txt` — experiential learnings from run v6
3. `../../logs/mud-session-2026-07-15.log` — map and actual movement history
4. `../../logs/hand-agent-output-2026-07-15_8.log` — optional `/btw` workarounds only; not mandatory

---

## Output Contract

- **Each output line = exactly one agent goal (one step budget)**
- **Each line contains exactly one clear action or decision**
- **Safety rules always take priority over experience/leveling goals**
- **Exits must be strictly evaluated: only use directions shown in `Exits:` output**

---

## Hard Safety Rules (Non-Negotiable)

1. **Never attack:** `cityguard`, `Peacekeeper`, `knight`, `sorcerer`, `Mayor`
2. **On "has arrived":** Immediate `flee` (no `look`, no `score`, no `kick` first)
3. **No combat on Main Street** or in obvious patrol transit rooms
4. **Before every combat:** `look` → guard check → read exits → plan escape route
5. **Priority order:** Water > Safe position > Food > Gold/Experience
6. **Exits are binding:** Never guess directions not confirmed in `Exits:` output

---

## Navigation Anchors (Validated from Logs)

### Safe Core Hubs
- **Temple Square** — central, fountain for water source
- **Common Square** — central hub, good orientation point

### Farm Anchors
- **Eastern End of Poor Alley (Room 3024)** — primary farm zone, Fido spawns, low patrol density
- **Poor Alley (Room 3012 vicinity)** — secondary farm area

### Risk Zones
- **East Gate** — may report "gate seems closed", exploration risk
- **Main Street** — high guard patrol density
- **Water Shop** — possible, but less reliable than Temple fountain

---

## Standard Loop (Low-Risk Path)

### Phase A — Stabilization (First 10 steps)

1. Execute `score` — check current status
2. Execute `look` — confirm current room and exits
3. **If thirsty:** Navigate to Temple Square and execute `drink fountain`
4. **If position unclear:** Stabilize room-by-room via known anchors (execute `look` after each move)

**Success Criteria:** Agent reports "not thirsty", HP > 50%, standing in Temple Square or Common Square

---

### Phase B — Safe Route to Farm (Steps 11–20)

1. From Temple/Common Square, move toward Poor Alley
2. Execute `look` after each room change
3. **If guard present in room:** Skip combat, change rooms (do not engage)

**Route Example:**
```
Common Square → west → Poor Alley → east → Eastern End of Poor Alley (Room 3024)
```

**Success Criteria:** Agent reaches farm zone (Room 3024) with zero combat, no flee events

---

### Phase C — Farm Cycle (Steps 21–45, Repeat 3–5 times)

**Per Fido Kill Cycle:**

1. Execute `look` — confirm single Fido, no guards
2. **If target available (Fido preferred) and room safe:**
   - `kill fido` — initiate combat
   - `kick fido` (optional) — accelerate kill only if situation remains safe
   - `get all corpse` — loot items and gold
   - `eat meat` — restore food stat
3. **Every 3–4 kills:** Execute `score` to monitor resources
4. **If no target:** Brief patrol between adjacent safe rooms, then `look` again

**Resource Check:**
- HP should remain > 40%
- Hunger/Thirst should be addressed before accumulating (drink/eat immediately when needed)

---

### Phase D — Emergency Protocol

**Triggers:** "has arrived", guard spotted, HP dropping rapidly, exits unclear

**Actions:**
1. Immediately: `flee`
2. Then: `look` (re-evaluate position)
3. Stabilize to known anchor and reassess

---

## Anti-Deadlock Rules

- **Closed gates:** Do not spam "open gate" or test repeatedly. Read the output.
- **Exit validation:** Always execute `look` + `score` first, then test only listed alternative exits
- **No extended experiments** at closed gates or unclear areas
- **Rapid recovery:** Return quickly to safe route (`Temple` → `Common` → `Poor Alley`)

---

## ATM Rule (Money Management)

Only use ATM when safe conditions are met (no active combat, no guard in room, known route back):

- `balance` — check account
- `withdraw <amount>` — only if specific purchase needed
- `deposit <amount>` — secure excess gold after looting

**Principle:** Do not interrupt farm cycle for non-critical banking.

---

## Planning Rule Per Step

**Always think ahead 3–5 actions (mini-route), don't just react to last output.**

**Example sequence:**
```
look → west → look → kill fido → kick fido → get all corpse → eat meat → score
```

This pre-planning reduces wasted commands and improves efficiency.

---

## /btw Rule (Optional Workarounds)

- Insights from `mud-journeys-2026-07-15.log` are **optional alternatives only**
- `/btw` suggestions may replace main plan **only if clearly safer or more efficient**
- Default to the structured phases above unless compelling reason to deviate

---

## End-of-Run Protocol

### Summary Output
1. Execute `score` — get final status
2. Output short status: (location, HP/Mana, hunger/thirst, experience progress, gold, risks)
3. Execute `quit` to save progress at safe location (Reception)

### Restart
- Begin new loop with `/loop` command
- Each new iteration should be shorter, safer, and more experience-efficient than previous

---

## Step Budget Allocation

| Phase | Steps | Goal |
|-------|-------|------|
| A (Stabilization) | 1–10 | Confirm position, hydrate |
| B (Route to Farm) | 11–20 | Reach room 3024 safely |
| C (Farm Cycles) | 21–45 | 3–5 Fido kills, 100+ Exp |
| D (Emergency/End) | 46–50 | Save progress, evaluate |
| **Total** | **50** | **Safe leveling run** |

---

## Key Metrics to Track

- **Experience gained:** Target 100+ per run (33 Exp/Fido × 3–5 kills)
- **Guard encounters:** Target 0 (safety metric)
- **Death events:** Target 0
- **Inventory management:** Meat, water, gold
- **Token efficiency:** Aim for <1000 tokens input/output per phase

---

## Common Failure Patterns and Fixes

| Pattern | Cause | Fix |
|---------|-------|-----|
| Navigation loop | Unclear exits, missing checkpoints | Use `look` before every move; memorize 3 safe routes |
| Guard ambush | Delayed flee response | Immediate flee on "has arrived" (reflex, not decision) |
| Farm stall | Farming location unreachable | Enforce Phase B time limit; restart if not at 3024 by step 20 |
| Void state loss | 15+ `look` commands without action | Max 3 `look` per room; mandatory action insertion |
| HP crisis | Low HP before flee | Flee at <30% HP threshold (don't wait for combat loss) |

---

## Configuration & Prerequisites

### Environment Setup
```bash
# Set API credentials
export ANTHROPIC_API_KEY=sk-ant-...
export ANTHROPIC_LLM_MODEL=claude-haiku-4-5

# Start infrastructure
cd week0_explore/infrastructure
docker compose up -d

# Navigate to agent
cd ../boukensha
```

### Expected Files
- `~/.boukensha/settings.yml` — agent configuration
- `credentials.json` — MUD login credentials
- `logs/` directory — for session logging

---

## Prompting Notes for Agent Implementation

When encoding this into a system prompt, emphasize:

- **Decision loop:** Observe → Identify threats → Execute prioritized action → Reflect
- **Reflex constraints:** "has arrived" → flee (no deliberation)
- **Route memory:** Pre-load known safe paths to reduce token waste
- **Exit strictness:** Never use unconfirmed directions

---

## Quick Reference Checklists

### Pre-Run Checklist
- [ ] API key configured
- [ ] Infrastructure running (docker compose status)
- [ ] Agent config loaded
- [ ] MUD connection test successful

### Mid-Run Checklist (Every 5 steps)
- [ ] Position confirmed via `look`
- [ ] No guards in immediate vicinity
- [ ] HP/Thirst/Hunger status acceptable
- [ ] Exit list updated

### Post-Run Checklist
- [ ] Final `score` recorded
- [ ] Progress saved (`quit` executed)
- [ ] Logs archived
- [ ] Metrics captured for next iteration

---

## Glossary

| Term | Definition |
|------|-----------|
| **MUD** | Multi-User Dungeon (text-based game) |
| **Fido** | Weak dog mob; primary farm target |
| **Corpse** | Dropped loot after mob death |
| **Flee** | Emergency escape command |
| **Look** | Observation command; returns room description + exits |
| **Score** | Status command; returns HP, Mana, experience, level |
| **Exits** | Available movement directions in current room |

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| v9 (Original) | 2026-07-15 | Consolidated learnings from runs v1–v8 |
| v9 (English) | 2026-07-16 | Translated to English for documentation |

---

**For questions or updates, refer to `explore_architecture/AGENTS_PROMPTING_INSTRUCTIONS.md` for operational context and `EXPLORATION.md` for architecture details.**

