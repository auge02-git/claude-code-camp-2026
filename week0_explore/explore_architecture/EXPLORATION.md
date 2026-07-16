# Boukensha Architecture Exploration (Consolidated Overview)

## Scope and Source Relationship
This document consolidates architecture insights from:
- `docs/explore_architectures.md` (base architecture intent)
- `docs/todo_week0_d1.md` (implementation steps, module build-out, runtime hardening)
- `docs/todo_week0_d3.md` (iterative optimization, skill/plugin workflows, operational refinements)

`todo_week0_d1.md` and `todo_week0_d3.md` are treated as implementation derivatives of `explore_architectures.md`.

## 1) Architecture Goals
- Build a lean agent workflow with low token usage and low context drift.
- Keep execution robust under unstable login/session conditions.
- Centralize MUD access and session handling instead of ad-hoc per-run scripts.
- Keep output operationally concise and decision-focused.
- Maintain additive evolution: extend with Python modules without rewriting stable legacy parts.

## 2) Guiding Decisions
- **Model strategy**: Claude Haiku 4.5 as cost-efficient default, with optional Sonnet/local-LLM overrides.
- **Context discipline**: Load only files needed for the current step to avoid off-task behavior.
- **Single session interface**: Reuse a shared `mud_manager`/session layer rather than temporary socket scripts.
- **Language split**: User-facing/system messages can remain localized, while code identifiers stay Python-idiomatic.
- **Additive migration**: New architecture is introduced as new Python modules; existing Ruby assets stay untouched.

## 3) Implemented Architecture (from the derivative todo files)
The implementation in `week0_explore/boukensha/` forms a modular baseline:

- `boukensha/cli.py`: entrypoint for interactive and scripted runs.
- `boukensha/repl.py`: interactive loop.
- `boukensha/run_dsl.py`: scripted journeys from text files.
- `boukensha/agent.py`: core control loop, tool orchestration, usage logging.
- `boukensha/backends/anthropic.py`: Anthropic backend integration with prompt-caching support.
- `boukensha/mud.py`: MUD session/interaction wrapper.
- `boukensha/config.py`: config + model override handling via environment variables/flags.
- `boukensha/tools/*`: tool abstractions and concrete MUD tools.
- `log_viz/server.py`: FastAPI service for session log visualization.

This structure maps the baseline architecture into runnable Python components while preserving legacy boundaries.

## 4) Runtime and Cost Controls
- **Prompt caching** is implemented on content blocks (system prompt, tools, latest user message) via ephemeral cache control.
- **Usage telemetry** captures input/output plus cache read/write metrics per step for measurable optimization.
- **Step limits** (`--max-steps`) are introduced to avoid unbounded tool loops.
- **Flexible backend wiring** supports cloud endpoints and local LLM endpoints for cheaper experimentation.

## 5) Operational Learnings from Iterative Runs
- Unscoped file loading causes context drift and avoidable token burn.
- Temporary one-off socket scripts are fragile and increase failure variance.
- Login failures should trigger controlled recovery through shared session APIs, not broad config hunting.
- Farming/navigation loops improve when using route circuits instead of single-room checks.
- Safety-first combat heuristics (early flee, guard avoidance, room constraints) significantly improve run stability.

## 6) Guardrails and Constraints
- Do not modify `.boukensha/`.
- Do not modify/translate existing Ruby implementation (especially `week0_explore/mud_manager/`).
- Place new architecture work in `week0_explore/boukensha/` as additive Python code.
- Preserve reproducibility through journey/versioned run files and structured logs.

## 7) Current Maturity Snapshot
- Core modular Python baseline is in place.
- Logging, replayable journeys, and visualization support iterative tuning.
- Caching and model override mechanisms are integrated.
- Architecture is now ready for deeper optimization (loop quality, safety policies, and adaptive farming logic).

## 8) Recommended Next Steps
1. Standardize one production-safe farming loop (including fallback paths and explicit risk thresholds).
2. Add regression checks for login recovery and reconnect behavior.
3. Add scenario tests for tool-loop limits, cache metrics, and journey determinism.
4. Extend route intelligence incrementally (safe sewer usage, dynamic spawn circuiting) behind explicit safety gates.
5. Keep architecture docs synchronized with implementation deltas after each optimization cycle.

## 9) Implementations Across `week0_explore/`
To reflect the full implementation scope of this directory, the architecture also includes these subsystems:

- **`infrastructure/`**: Docker-based CircleMUD runtime (core dependency for live agent runs).
- **`mud_manager/`**: Stable Ruby session layer (legacy boundary, intentionally preserved).
- **`mud-mcp/`**: Python MCP bridge exposing MUD actions (`connect`, `login`, `send`, `read`, `status`, `disconnect`).
- **`boukensha/`**: Autonomous LLM-driven orchestration engine (agent loop, tools, CLI/DSL, logging, backend abstraction).
- **`circlemud-world-parser/`**: Structured parser pipeline for CircleMUD world files to JSON datasets.
- **`preview/`**: World-data visualization surface backed by parsed JSON outputs.
- **`boukensha/log_viz/`**: FastAPI-based replay and log-inspection endpoint for JSONL session traces.
- **`bin/`**: Utility scripts for log maintenance and world conversion workflows.
- **`logs/` + `boukensha/journeys/`**: Replay corpus for iterative tuning, regression checks, and prompt/loop optimization.

## 10) High-Level Runtime/Data Flow
```text
CircleMUD runtime (infrastructure)
  -> mud-mcp session/tools (Python bridge)
  -> boukensha agent loop (LLM + tools)
  -> JSONL logs (logger)
  -> log_viz (inspection/replay)

CircleMUD world files
  -> circlemud-world-parser
  -> preview data/web visualization
```

## 11) Integration Boundaries (Explicit)
- `infrastructure/` must be running for live `mud-mcp` and `boukensha` gameplay.
- `mud_manager/` remains the compatibility anchor and is not rewritten.
- New behavior is primarily added in Python layers (`mud-mcp`, `boukensha`, parser/preview tooling).
- Logs and journey files are first-class architecture artifacts for controlled iteration.
