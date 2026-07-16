# AGENTS_PROMPTING_INSTRUCTIONS.md

Agent Prompting Guidelines for Boukensha MUD Gameplay

## Overview

This document consolidates operational instructions and lessons learned from iterative Boukensha agent runs. It serves as a reference for prompt engineering, behavioral constraints, and optimization strategies for autonomous MUD gameplay.

**Source Documents:**
- `short-agent-instruction-2026-07-15_2.md` (core operational guidelines, 61 steps of execution)
- `mud-journeys-2026-07-15_v6.log` (live execution transcript with error patterns and recovery strategies)
- Referenced journey files and session logs (iterative refinement corpus)

---

## 1) Core Operational Findings

### Navigation as Primary Failure Point
- **Problem:** Agent looped excessively between `Common Square`, `Market Square`, and `Poor Alley` (~15–20 wasted steps per run).
- **Root Cause:** Insufficient route anchoring; agent used trial-and-error direction guessing in transit rooms instead of memorized safe paths.
- **Mitigation:** Pre-load navigation map (even if minimal) with confirmed safe routes: `Common Square → west → Poor Alley`, `Common Square → north → Temple Square`, etc.

### Fountain Efficiency Bottleneck
- **Finding:** Temple Square fountain (for water) was often discovered late or not at all, despite proximity.
- **Cost:** 5–10 unnecessary moves per water run; cumulative token waste via repeated `look` commands while lost.
- **Fix:** Make fountain location a **hard-coded agent goal** within first 20 steps; prioritize hydration over exploration.

### Farming Progress Stalled
- **Observation:** Across multiple runs, agent rarely completed one full Fido kill-loot cycle.
- **Reason:** Navigation overhead consumed all action budget before reaching farming anchor (`Eastern End of Poor Alley`, room 3024).
- **Target:** Guarantee agent reaches farming zone in <15 steps; then execute 3–5 complete farm loops.

### Guard Risk Exposure
- **Incident:** Agent encountered `cityguard` and `Peacekeeper` multiple times in transit rooms; some runs triggered fleeing 3+ times.
- **Pattern:** Main Street is a high-patrol area; agent was choosing it as a waypoint without awareness.
- **Control:** Exclude Main Street from safe routes unless strictly necessary; prefer peripheral routes (Poor Alley circuit).

### Session State Loss ("Void" Incidents)
- **Issue:** Agent received "void" messages indicating session crash or timeout after prolonged `look` loops without action.
- **Trigger:** ~15+ consecutive `look` commands without successful movement or resource action.
- **Prevention:** Insert action steps between queries; never loop `look` >3 times without executing `move` or `kill`.

---

## 2) Hardened Safety Rules

### Rule 1: Never Attack Guards
**Never initiate combat with:**
- `cityguard`, `Peacekeeper`, `knight`, `sorcerer`, `Mayor`

**Action if guard appears:**
- If guard enters room during patrol: **immediate `flee`** (no `look`, no `score`, no combat)
- If guard status in room description: leave immediately via any exit
- Exception: None. Treat guard presence as room hazard

### Rule 2: Immediate Flee on "has arrived"
**Any message matching "has arrived":**
- Check if entity is known-safe (e.g., another player)
- If unknown or NPC: **`flee` within one command cycle**
- Do not delay with observation (`look`), inventory check (`score`), or combat setup

**Rationale:** Unknown arrivals in transit rooms often precede guard patrol or aggressive NPC spawns.

### Rule 3: Solo Combat Only
**Never engage multiple targets or unknown mobs:**
- Confirm single `fido` via `look` before `kill`
- If multiple mobs visible: move to adjacent safe room and retry
- If any mob type unknown: skip and re-examine

### Rule 4: Resource Priority (Strict Order)
1. **Water** (drink at fountain, highest priority if thirsty)
2. **Safe position** (known room with exits, no guards, confirmed navigation)
3. **Food** (eat meat or in-game food after kill)
4. **Experience/Gold** (farming, only when other needs met)

### Rule 5: Early Flee Threshold
- **HP threshold:** Below 30% of max → `flee` immediately
- **No exceptions:** Do not attempt additional kills or healing spells; prioritize safety
- **Rationale:** Regeneration is slow; early gap closure prevents cascade failures

### Rule 6: Strictly Respect Exit Lists
- **Only moves matching `Exits:` output are valid**
- Never guess directions not listed
- If `Exits: north east south`, these are the only three moves; west/up/down will fail or produce error loops
- **Always re-read exits after each room change**

---

## 3) Confirmed Navigation Anchors

### Safe Core Routes (Verified)
```
Common Square (central hub)
  ├─ north → Temple Square (fountain, water source)
  ├─ west → Poor Alley (entry point to farm zones)
  └─ east → [less explored, avoid for now]

Temple Square
  ├─ south → Common Square
  └─ [check other exits for alternative routes]

Eastern End of Poor Alley (room 3024, PRIMARY FARM ANCHOR)
  ├─ east → Poor Alley (middle section)
  └─ [look for Fido spawns, least guard traffic]

Poor Alley (middle section)
  ├─ south → Grubby Inn
  └─ east → Eastern End of Poor Alley

Market Square
  ├─ south → Common Square
  └─ [less direct to farming, avoid for speed runs]
```

### High-Risk Zones (Avoid or Traverse Quickly)
- **Main Street:** High cityguard patrol density
- **East Gate:** Often reports "gate seems closed"; avoid exploration there
- **Guild Rooms** (e.g., room 3016): Swordsmiths' guild hall; guards present, no combat allowed

### Low-Risk Zones (Safe for Loitering)
- **Eastern End of Poor Alley (3024):** Peripheral, low patrol, Fido spawn zone
- **Temple Square:** Fountain, safe for resource actions
- **Donation Room:** (if discovered) reported to have free items; safe for inventory management

---

## 4) Operational Plan (Next Run Template)

### Phase 1 – Stabilization (Steps 1–10)
1. **Check Status:** `score` + `look` (confirm location and exits)
2. **Route to Fountain:** Navigate to Temple Square via `Common Square`
3. **Hydrate:** `drink fountain` if thirsty
4. **Confirm State:** `score` again (verify HP, Mana, Move points stable)

**Success Criteria:** Agent reports "not thirsty", HP >50%, standing in Temple Square

### Phase 2 – Navigation to Farm (Steps 11–20)
1. Move from Temple Square → Common Square (`south`)
2. Move from Common Square → Poor Alley (`west`)
3. Move from Poor Alley → Eastern End of Poor Alley (`east` or `east east` depending on exits)
4. Execute `look` to confirm Fido presence

**Success Criteria:** Agent reaches room 3024 with no combat, no flee events

### Phase 3 – Farm Loop (Steps 21–45, ~3–5 kill cycles)
**Per Fido Kill Cycle:**
1. `look` (confirm Fido, no guards)
2. `kill fido` (initiate combat)
3. `kick fido` (optional: accelerate kill)
4. `get all corpse` (loot items and gold)
5. `eat meat` (recover food)
6. `score` (every 3–4 cycles to monitor resources)

**Inter-Cycle Patrol:** If no Fido in 3024, move `east` then `west` to check adjacent room, then return

### Phase 4 – Save Progress (Step ~50)
1. Navigate back to safe location (Common Square or Temple Square)
2. Confirm HP/resources stable
3. **`quit`** to save character state (free; stored at Reception)

**Success Metrics:**
- ≥3 Fido kills completed
- Net EXP gain: 100+ (target ~33 EXP per kill)
- No guard encounters during farm
- Character saved safely

---

## 5) Common Failure Patterns and Corrections

### Pattern 1: Navigation Loop (Symptoms)
- Agent repeating same rooms: "Common Square → Poor Alley → Common Square" (×5+)
- Multiple consecutive `look` commands with no `move` actions
- Growing token usage without position change

**Fix:**
- Require exact exit confirmation before each move: "only move if `Exits:` lists direction"
- Limit `look` repeats to 3 max per room; then move to adjacent room or reset
- Use route checkpoints: "if in Common Square, next move is always west; if in Temple Square, next move is always south"

### Pattern 2: Guard Spiral
- Agent receives "cityguard has arrived" message
- Attempts `look` or `score` instead of immediate `flee`
- Delayed flee action results in combat or forced flee anyway

**Fix:**
- Encode rule: **"On 'has arrived' message, immediately send `flee`; do not parse or evaluate first"**
- Pre-compute flee paths: "if in Main Street, flee south; if in Temple, flee south"
- Add latency buffer: "assume 1–2 command delays; act 2 steps ahead"

### Pattern 3: Void State Loss
- Agent sends 10+ `look` commands in rapid succession without action
- Session reports "void" or "timeout"
- Character loses all progress, session resets

**Fix:**
- Hard limit: **Never send >3 `look` commands sequentially without an action (`move`, `kill`, `eat`, `drink`)**
- Mandatory action insertion: "after `look`, always queue one movement or resource action"
- Example: `look` → `move west` (if exit available) → `look` (in new room)

### Pattern 4: Late Fountain Discovery
- Agent explores distant areas before finding Temple Square fountain
- Uses HP-healing or other workarounds for thirst
- Arrives at farm zone already dehydrated (low performance)

**Fix:**
- **Hard-code fountain search in first 10 steps**
- Prompt: "Priority 1: find water source. Search north from Common Square."
- Anchor: "Temple Square = water; remember this location for future runs"

### Pattern 5: Premature Combat
- Agent encounters Fido but HP is low or position unclear
- Initiates kill despite suboptimal conditions
- Forced to flee mid-fight or loses loot

**Fix:**
- Pre-combat checklist: (1) `look` confirms single Fido, (2) no guards in room exits, (3) HP >60%, (4) Exits known
- If any check fails: move to adjacent room and re-evaluate
- Example: "if room has 2+ exits to Main Street, do not fight here; move to 3024 first"

---

## 6) Prompt Engineering Directives

### System-Level Instructions
Include in system prompt:

**Identity & Role:**
```
You are Boukensha (冒険者), an autonomous MUD agent controlling a Level 1 warrior named 'dummy' 
in a CircleMUD environment (Midgaard). Your objective is to survive, acquire resources (water, 
food, experience), and progress safely to Level 2. You follow strict operational rules and navigate 
deterministically using confirmed exit lists. You never take unnecessary risks.
```

**Decision Loop:**
```
For every game step:
1. Observe current state via 'look' and 'score'.
2. Identify immediate threats: guards, aggressive mobs, low HP.
3. Execute one prioritized action (water/safety/food/farming) per step.
4. Reflect on outcome and adjust route if necessary.
Never perform speculative actions or multi-step lookahead without confirmed exits.
```

**Hard Constraints:**
```
- NEVER attack: cityguard, Peacekeeper, knight, sorcerer, Mayor.
- On 'has arrived': immediate 'flee'.
- On unknown mob: move away, do not engage.
- On <30% HP: immediate 'flee'.
- On thirsty: prioritize fountain above all else.
- Max 3 'look' commands per room; then move or reset.
```

### Few-Shot Examples (Optional, for Difficult Scenarios)

**Example 1: Safe Navigation**
```
Observation: You are in Common Square. HP: 40/50, thirsty. Exits: north, south, east, west.
Thought: Fountain is north (Temple Square). No guards visible. HP is adequate for movement.
Action: move north
```

**Example 2: Guard Avoidance**
```
Observation: You see 'The cityguard has arrived' in room output.
Thought: Guard appeared. Immediate threat. No time for look or score.
Action: flee
```

**Example 3: Failed Route, Retry**
```
Observation: You tried 'move west' but room description did not change. 
Thought: Move command may have failed. Re-check exits.
Action: look
[Output shows exits: north, east. West is not available.]
Action: move north
```

---

## 7) Iteration and Optimization Log

### Run 2026-07-15_v1–v5
- **Goal:** Establish baseline safe routes
- **Result:** Successfully identified Temple Square, Common Square, Poor Alley anchors; frequent navigation loops
- **Lesson:** Hard-coding route checkpoints reduced loop count by ~40%

### Run 2026-07-15_v6
- **Goal:** Optimize farm loop with guard awareness
- **Result:** Reached farm zone but triggered void state during `look` spam
- **Lesson:** Strict <3 `look` limit per room prevents session crashes; action insertion mandatory

### Run 2026-07-15_v7–v9 (Planned)
- **Goal:** Execute 3+ complete farm cycles with zero guard encounters
- **Target:** 100+ EXP gained per run; character reaches Level 1 → Level 2 boundary
- **Expected Optimizations:** Eliminate navigation loop entirely; add fountain search timeout; pre-compute flee paths

### Planned Next Iterations
1. **v10–v12:** Extend to Level 2 skill acquisition (practice at Practice Yard)
2. **v13–v15:** Multi-area exploration (sewers, shops, alternative spawn zones)
3. **v16+:** Economy automation (ATM, trading, price optimization)

---

## 8) Integration with Boukensha Agent Architecture

This prompting guide integrates with the Boukensha system as follows:

- **System Prompt:** Inject core constraints and decision loop from Section 6
- **Journey DSL:** Use Phase 1–4 template (Section 4) as DSL script baseline
- **Tool Registry:** MUD tools (`look`, `move`, `kill`, `flee`, etc.) map directly to Action steps
- **Logging:** Capture each step's observation/thought/action in JSONL for post-run analysis
- **Context Window:** Keep agent narrative concise; load only route anchors and current session state to minimize token usage

### Environment Variables
- `BOUKENSHA_SAFETY_MODE=strict` → enforce <3 look limit, guard retreat
- `BOUKENSHA_FARM_ANCHOR=3024` → pre-set farming zone to Eastern End of Poor Alley
- `BOUKENSHA_FOUNTAIN_ROUTE=common_north_temple` → encode fastest fountain path

---

## 9) Debugging and Troubleshooting

### Issue: Agent Stuck in Navigation Loop
**Symptoms:** Same rooms repeated; token budget exceeded
**Diagnosis:** Likely missing exit validation or stale route assumption
**Recovery:**
1. Inject fresh `look` command
2. Extract exit list explicitly
3. Add route to whitelist if exits match known pattern
4. Retry movement

### Issue: Guard Encounter Leading to Cascade Failures
**Symptoms:** Guard appears, agent hesitates, then forced flee, then lost
**Diagnosis:** Latency between observation and action; agent tried `look` before fleeing
**Recovery:**
1. Reduce latency: pre-compute flee paths in system prompt
2. Make "has arrived" → "flee" a reflex (no intermediate steps)
3. Retry run after agent resets

### Issue: Session Timeout / Void State
**Symptoms:** "Void" message or no response after command
**Diagnosis:** Too many `look` commands in rapid succession without action
**Recovery:**
1. Enforce action-after-look rule: every `look` followed by `move` or `kill` or `drink`
2. Reduce prompt length to speed up LLM response time
3. Retry run with smaller step budget per prompt

### Issue: Character Not Making Progress on EXP
**Symptoms:** Multiple runs with 0 kills completed
**Diagnosis:** Agent not reaching farm zone in time, or farming location has no Fidos
**Recovery:**
1. Pre-load exact farming route (bypass exploration)
2. Increase `--max-steps` parameter to 50–100 for longer farm windows
3. Verify Fido spawns are active in room 3024 (check CircleMUD server logs)

---

## 10) Recommended Next Actions

1. **Test this guide with v7 run:** Execute Phase 1–4 plan exactly; measure token usage and completion time
2. **Capture lessons in versioned journey files:** Store successful run transcripts for few-shot learning
3. **Add regression tests:** Ensure future runs maintain zero-guard-encounter baseline
4. **Extend to Level 2:** Once Level 2 achieved, document skill acquisition steps and new farming options
5. **Archive all run logs with annotations:** Build corpus for future agent training

