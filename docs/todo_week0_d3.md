## Weitere Schritt um Agent zu entwickeln

❯ /plugin marketplace add anthropics/skills                                                                                                                                                                                        
⎿  Successfully added marketplace: anthropic-agent-skills

├───────────────────────┼───────────────────────────────┤                                                                                                                                                                        
│ web-artifacts-builder │ Web-Artefakte                 │                                                                                                                                                                        
└───────────────────────┴───────────────────────────────┘

1. Welchen möchtest du installieren? Mit /plugin install <name> kannst du einen davon hinzufügen. 
```/plugin install skill-creator```

läde die Plugins und Skills neu
```
/reload-plugins 
/reload-skills
```

Diese werden im Verzeichnis `/Users/awo/.claude/skills` abgelegt. Dort kannst du die Skills auch direkt bearbeiten.

Usage:                                                                                                                                                                                                                    
6     uv run --directory ../../mud-mcp python mud_player.py                                                                                                                                                                 
7     python mud_player.py                    # if mud-mcp is on PYTHONPATH                                                                                                                                                 
8     python mud_player.py look               # run single command and exit                                                                                                                                                 
9     python mud_player.py look "score" who   # run multiple commands and exit

Update(.claude/scripts/mud_player.py)                                                                                                                                                                                            
⎿  Added 2 lines, removed 1 line                                                                                                                                                                                                 
15  from pathlib import Path                                                                                                                                                                                                 
16                                                                                                                                                                                                                           
17  # Make mud-mcp importable when running directly from this directory.                                                                                                                                                     
18 -MUD_MCP_SRC = Path(__file__).resolve().parents[3] / "mud-mcp"                                                                                                                                                            
18 +# Script lives at .claude/scripts/ → parents[4] = week0_explore/                                                                                                                                                         
19 +MUD_MCP_SRC = Path(__file__).resolve().parents[4] / "mud-mcp"                                                                                                                                                            
20  sys.path.insert(0, str(MUD_MCP_SRC))                           

---------

Weitere Optimierungen durch bessere Anweisungen, die auf Reflektionen der vorherige Durchläufe nbasieren.

[week0_tests 5f120c9] AWO: optimized, better promting and lerning from before steps.
6 files changed, 791 insertions(+)
create mode 100644 week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v3.md
create mode 100644 week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v4.txt
create mode 100644 week0_explore/explore_architecture/02_agent_skills/.claude/scripts/boukensha_safe_farm.py
create mode 100644 week0_explore/explore_architecture/02_agent_skills/.claude/skills/boukensha-safe-farm/SKILL.md
create mode 100644 week0_explore/logs/short-agent-instruction-2026-07-15_2.md
create mode 100644 week0_explore/logs/short-agent-instruction-2026-07-15_2.txt

[week0_tests 37be942] AWO: fix, better promting by architecture 2 and runnings.
2 files changed, 172 insertions(+)
create mode 100644 week0_explore/boukensha/journeys/erfahrungen_durchlaeufe_v5.txt

----------

Andre.Wolff@MB-J3XNPGKM94 boukensha % uv run boukensha --llm-base-url http://localhost:1234 --model google/gemma-4-12b-qat --max-steps 30 --dsl ./journeys/mud-journeys-2026-07-15_v6.log

---------

[week0_tests a4801bb] AWO: add, more reports and docs to plugins and skills from video and data of next running.
4 files changed, 219 insertions(+), 1 deletion(-)
create mode 100644 docs/todo_week0_d3.md
create mode 100644 week0_explore/explore_architecture/02_agent_skills/.claude/scripts/mud_player.py
create mode 100644 week0_explore/explore_architecture/02_agent_skills/.claude/skills/mud-play/SKILL.md

--------

[week0_tests 5f120c9] AWO: optimized, better promting and lerning from before steps.
6 files changed, 791 insertions(+)
create mode 100644 week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v3.md
create mode 100644 week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v4.txt
create mode 100644 week0_explore/explore_architecture/02_agent_skills/.claude/scripts/boukensha_safe_farm.py
create mode 100644 week0_explore/explore_architecture/02_agent_skills/.claude/skills/boukensha-safe-farm/SKILL.md
create mode 100644 week0_explore/logs/short-agent-instruction-2026-07-15_2.md
create mode 100644 week0_explore/logs/short-agent-instruction-2026-07-15_2.txt

[week0_tests 37be942] AWO: fix, better promting by architecture 2 and runnings.
2 files changed, 172 insertions(+)
create mode 100644 week0_explore/boukensha/journeys/erfahrungen_durchlaeufe_v5.txt

[week0_tests 40ad7b9] AWO: fix, logs output to file and using to create now-how-reports.
7 files changed, 79 insertions(+), 13 deletions(-)

[week0_tests c321261] AWO: fix, logs output to file and using to create now-how-reports and update journey v8.
2 files changed, 422 insertions(+)
create mode 100644 week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v6.txt
create mode 100644 week0_explore/boukensha/journeys/erfahrungen_durchlaeufe_v6.txt

[week0_tests 6346f7c] AWO: add, new optimized journey v9 and compose duning for faster rambup on agent.
8 files changed, 240 insertions(+)
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v2.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v3.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v4.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v5.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v6.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v7.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v8.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v9.md

[week0_tests f5da7d0] AWO: add, new optimized journey v9 and compose duning for faster rampup on agent.

[week0_tests 830e568] AWO: fix, documentations to frame of bootcamp as stub.
4 files changed, 551 insertions(+), 31 deletions(-)
create mode 100644 week0_explore/explore_architecture/AGENTS.md
create mode 100644 week0_explore/explore_architecture/AGENTS_GERMAN.md
create mode 100644 week0_explore/explore_architecture/AGENTS_PROMPTING_INSTRUCTIONS.md
create mode 100644 week0_explore/explore_architecture/EXPLORATION.md

[week0_tests 4cb9abc] AWO: fix, documentations to frame of bootcamp as stub.
update explore_extracs.md
2 files changed, 164 insertions(+), 33 deletions(-)

[week0_tests 07f7566] AWO: fix, documentations to frame of bootcamp as stub.
3 files changed, 167 insertions(+), 1 deletion(-)
create mode 100644 docs/explore_extracts.md
rename docs/{explore_extracs.md => explore_extracts_german.md} (100%)

[week0_tests 7113fee] AWO: fix, documentations to frame of bootcamp as commit-datas.
2 files changed, 291 insertions(+)
create mode 100644 docs/boukensha_running_instructions.md

[week0_tests dcd058f] AWO: fix, documentations to frame of bootcamp as commit-datas.
3 files changed, 809 insertions(+), 1 deletion(-)
create mode 100644 docs/plans/implementation_instructions_v2.md
create mode 100644 docs/plans/umsetzung_v2.md