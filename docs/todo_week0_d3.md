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

