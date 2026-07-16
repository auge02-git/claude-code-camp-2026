# Guide for Evolving the Boukensha Journey Instructions

## Purpose

This guide describes how the journey instructions for the Boukensha agent
should be improved step by step.
It is based on the previous implementations in reports `v3` through `v7`, the session logs,
the hand-agent outputs, and the documented results in `docs/todo_week0_d3.md`.

The goal is to systematically derive better, shorter, safer, and more
EXP-efficient instructions from real playthroughs.

---

## Target Outcome

Each new journey version should:

1. be **safer** than the previous one
2. create **fewer loops and dead ends**
3. enable **more EXP per minute**
4. **explicitly avoid known failure patterns**
5. contain **concrete, machine-usable instructions**
6. transform **real observations from logs** into stable rules

---

## Input Sources Used

The following sources are typically evaluated for a new journey version:

### 1. Base report of the last stable version
Example:
- `week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v6.txt`

This file provides the current working baseline:
- hard rules
- safe routes
- known risks
- current combat/farming logic

### 2. Real movement and world logs
Examples:
- `week0_explore/boukensha/journeys/mud-journeys-2026-07-15.log`
- `week0_explore/logs/mud-journeys-2026-07-15_v6.log`

These logs provide:
- actual room sequences
- working routes
- problematic routes
- new points of interest
- exits and room relationships

### 3. Reflective agent logs
Examples:
- `week0_explore/logs/hand-agent-output-2026-07-15_8.log`

These logs provide:
- agent reasoning mistakes
- wrong priorities
- recurring failure patterns
- ideas for improving prompting and flow

### 4. Meta-documentation
Example:
- `docs/todo_week0_d3.md`

This file documents:
- what has already been implemented
- which versions were created
- what structure a new version should have
- which improvements have already been successful

---

## Standard Process for a New Journey Version

### Step 1 - Use the last stable version as the baseline
Always take the last usable journey file as the starting point.

Example:
- `v6` as the basis for `v7`

Rule:
- do not start from scratch
- keep the existing safe rules
- only add new findings or refine old rules

### Step 2 - Read new logs against the baseline
Compare new logs with the existing version.

Questions to ask:
- What new errors occurred?
- Which old errors happened again?
- Which rules worked?
- Which rules were unclear or incomplete?
- Which new safe routes or anchors were observed?
- Are there new risk zones?
- Are there new system-level problems such as void, timeout, or missing output?

### Step 3 - Classify findings into categories
All new observations must be cleanly categorized.

Recommended categories:
- **Core Findings**
- **New Core Findings**
- **Hard Rules**
- **Safe Navigation Anchors / Routes**
- **Farm Logic**
- **Aggressive Mode / EXP Maximization**
- **Emergency / Recovery Strategies**
- **Optional /btw Hints**

### Step 4 - Turn only verified facts into rules
Important:
- Only promote things to hard rules if they were confirmed in logs or across multiple runs.
- Clearly mark assumptions as optional.

Examples of **verified rules**:
- `Common Square -> west -> Eastern End Of Poor Alley` works
- Main Street is a guard-risk area
- `has arrived` -> flee immediately
- Void requires a recovery sequence

Examples of **non-hard rules / optional**:
- Pet Shop may be situationally interesting
- Bank/ATM can be used later
- level more aggressively only when HP buffer is stable

### Step 5 - Formulate concrete agent goals
The journey must contain operational steps, not just analysis.

Good format:
- clear heading
- short justification
- concrete sequence

Example:
- `score`
- `look`
- `drink fountain`
- `kill fido`
- `kick fido`
- `get all corpse`
- `eat meat`
- `quit`

Rule:
- Every instruction must be directly executable or clearly interpretable by an agent.

### Step 6 - Explicitly write new failure patterns as avoidance rules
Do not only add what should be done, but also what must be avoided.

Typical failure patterns from previous runs:
- loops on `Main Street`
- dead ends at `East Gate`
- Pet Shop idle loops
- guard pinning
- void states
- API timeouts caused by command bursts that are too fast
- too many `look` sequences without a follow-up action
- guessing unconfirmed directions

### Step 7 - Keep the optional aggressive strategy separate
Leveling faster is useful, but it must not destroy the safety logic.

Therefore:
- write aggressive mode as its **own section**
- state hard abort conditions explicitly
- define clear prerequisites

Example:
- only in guard-free rooms
- only with an HP buffer
- only with a safe escape route
- `kill` + `kick` as an accelerator
- immediately switch back to safety mode when `has arrived` appears

### Step 8 - Save the new version as a new file
Filename pattern:
- `erfahrung_durchlaeufe_v3.md`
- `erfahrung_durchlaeufe_v4.txt`
- `erfahrungen_durchlaeufe_v5.txt`
- `erfahrung_durchlaeufe_v6.txt`
- `erfahrung_durchlaeufe_v7.txt`

Recommendation:
- use `erfahrung_durchlaeufe_vX.txt` as consistently as possible going forward
- never overwrite the old version
- always assign a new version number

---

## Recommended Structure of a New Journey File

A new journey file should follow this structure:

1. **Header**
   - source
   - date/status
   - goal

2. **Core Findings**
   - the most important new learnings from the run

3. **New Core Findings**
   - new topic blocks such as void, ATM, Pet Shop, timeout, aggressive mode

4. **Hard Rules**
   - non-negotiable safety and execution rules

5. **Safe Navigation Routes / Anchors**
   - verified paths and room anchors

6. **Operational Standard Flow**
   - start
   - water
   - farm area
   - combat cycle
   - pendulum/fallback logic

7. **Optional Aggressive Strategy**
   - for faster leveling
   - always clearly bounded

8. **Emergency / Recovery**
   - void
   - timeout
   - guard pinning
   - unclear exits

9. **/btw Hints**
   - optional alternatives
   - not mandatory logic

---

## Concrete Procedure for Deriving v(N+1)

If `vN` already exists, then:

1. Read `vN` completely.
2. Read the new hand-agent file completely.
3. Read the new movement/journey logs completely or focus on the relevant sections.
4. Record only the deltas against `vN`.
5. Assign each delta to a category.
6. Remove weak assumptions or mark them as optional.
7. Formulate a new `v(N+1)` from that.
8. Check whether the new version:
   - is safer
   - navigates more directly
   - has clearer recovery instructions
   - is directly usable by the agent

---

## Specific Lessons Learned from the Previous Implementation

### Proven content
- `Temple Square`, `Common Square`, `Eastern End Of Poor Alley`, and `Grubby Inn` are strong anchors.
- The route to the fountain must always remain explicit.
- Guard rules must appear high in the document and be unambiguous.
- `kill -> loot -> eat -> score` is a workable baseline cycle.

### Proven extensions in later versions
- anti-pinning rules
- explicitly naming the Pet Shop trap
- treating exits as the primary navigation matrix
- aggressive mode only as optional
- void recovery as a fixed sequence
- documenting API timeouts as a systemic issue
- ATM/bank only as a late-phase feature, not a core objective

### Typical agent reasoning mistakes that the instructions must guard against
- waiting too long for new information without changing rooms
- putting too much weight on Main Street / East Gate
- exploration instead of returning to a known safe route
- combat thinking in unsafe rooms
- failing to clearly separate standard mode from aggressive mode

---

## Minimal Checklist Before Saving a New Version

- [ ] Used the last stable version as the baseline
- [ ] Actually evaluated the new logs
- [ ] Turned only verified findings into hard rules
- [ ] Documented new risks explicitly as avoidance strategies
- [ ] Clearly separated standard mode and aggressive mode
- [ ] Included an emergency/recovery section
- [ ] Updated navigation anchors
- [ ] Saved the file as a new version number

---

## Example from the Last Documented Implementation

From `docs/todo_week0_d3.md`:

- Base: `erfahrung_durchlaeufe_v6.txt`
- Additional sources:
  - `mud-journeys-2026-07-15.log`
  - `mud-journeys-2026-07-15_v6.log`
  - `hand-agent-output-2026-07-15_8.log`
- Result: `week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v7.txt`

The newly added topics were:
- void state
- bank/ATM
- new navigation points
- expanded hard rules
- safe navigation routes A-E
- void prevention
- safe base route
- aggressive mode
- emergency/void recovery
- /btw hints

---

## Short Formula for Future Evolution

**Read the baseline -> compare new logs -> extract deltas -> update rules/routes/recovery -> save the new version.**

