# Schritt 10 — Eine Standard-Tool-Bibliothek

Die Standard-Tool-Bibliothek ist **MCP**.

Boukensha liefert **keine eigenen Tools**. Es ist ein MCP-*Host*: Jedes Tool,
das der Agent aufrufen kann, kommt von einem MCP-Server, der in `settings.yaml`
deklariert ist. Dateizugriff gewuenscht? Einen Filesystem-Server einbinden. Ein
MUD spielen? `mud-manager --mcp` einbinden. Ein Agent mit leerem
`mcp_servers:`-Block kann nur reden.

> Das Verzeichnis heisst noch immer `10_standard_tool_library`, weil dieser
> Schritt frueher eingebaute `read_file`- / `list_directory`-Tools in
> `examples/example.py` mitbrachte. Die sind weg. Der Name bleibt, damit die
> Schritt-Nummerierung und alle Pfade, die hierauf zeigen, weiterhin aufgeloest
> werden.

## Was neu ist

### `boukensha.mcp.client.Client`

Ein minimaler MCP-over-stdio-Client: Server starten, Handshake, `tools/list`,
`tools/call`. Er ist server-agnostisch — `command` / `args` / `env` ist die
Standard-stdio-Transport-Konfiguration, das gleiche Tripel, das jeder MCP-Host
verwendet.

### `boukensha.tools.mcp`

Das einzige verbliebene Tool-Registrierungs-Modul. Registriert die vom Server
entdeckten Tools in einer Registry und beschraenkt deren Namen optional mit
einem `prefix`.

```python
from boukensha.tools import mcp as tools_mcp

tools_mcp.register(
    registry, "mud-manager", args=["--mcp"],
    env={"MUD_HOST": "localhost"},
    prefix="tbamud",          # look des Daemons wird als tbamud__look registriert
)
```

Das Praefixieren erfolgt **clientseitig**: Der Server sieht auf dem Draht
weiterhin `look`. Es existiert, damit zwei Server sich nicht stillschweigend
die Namen ueberschreiben koennen — eine Kollision wirft einen Fehler und
benennt den Fix.

### `mcp_servers:` in `settings.yaml`

Eine Faehigkeit hinzufuegen ist eine Konfigurationsaenderung, keine
Code-Aenderung:

```yaml
mcp_servers:
  mud:
    command: mud-manager
    args:    [--mcp]
    prefix:  tbamud
    env:                     # Zugangsdaten eines stdio-Servers werden per Umgebung uebergeben
      MUD_HOST:     your.mud.host
      MUD_NAME:     Gandalf
      MUD_PASSWORD: secret

  filesystem:
    command:  npx
    args:     [-y, "@modelcontextprotocol/server-filesystem", /tmp]
    prefix:   fs
    required: false          # Kann nicht starten? Warnung und weitermachen
```

| Schluessel | Standard | Bedeutung |
|------------|---------|-----------|
| `command` | — | Auszufuehrendes Programm. Wird vom Betriebssystem aufgeloest; ein relativer Pfad haengt vom cwd ab — es wird nicht selbstaendig nach einer Binaerdatei gesucht. |
| `args` | `[]` | Dessen argv. |
| `env` | `{}` | Zusaetzliche Umgebung. Server erben die Umgebung von boukensha; diese Schluessel ueberschreiben sie. |
| `prefix` | keiner | Schraenkt entdeckte Namen ein (`fs` → `fs__read_file`). |
| `required` | `true` | `false` stuft einen Startfehler auf eine Warnung herab. |

### Was weggefallen ist

| Weg | Ersetzt durch |
|-----|---------------|
| `read_file` / `list_directory` (registriert via `configure=` in `examples/example.py`) | einen Filesystem-MCP-Server. Kompromiss: benoetigt `npx`, und sein Root ist in `args:` festgelegt statt `working_dir` zu verfolgen. |
| Der HTTP-401-Sonderfall in `Client.call()` | die generische Nicht-2xx-Fehlermeldung, passend zum eigenen Schritt-9-Revert von Ruby. |
| Den cwd-`.boukensha`-Fallback in `Config._resolve_dir()` | eine strikte `BOUKENSHA_DIR` → `~/.boukensha`-Prioritaet, passend zum eigenen Schritt-9-Revert von Ruby. |

`working_dir` bleibt auf `boukensha.run` / `.repl` erhalten, aber nur als
`Context`-Metadaten: Es registriert nichts.

## Demo ausfuehren

```sh
# Offline, kein API-Key, kein Live-MUD — verwendet das eingebaute Fake-MUD des Daemons:
python examples/mcp_mud_demo.py --dry

# Vollstaendiger Lauf — benoetigt ANTHROPIC_API_KEY und einen mcp_servers: mud-Eintrag.
# Vom Repo-Root aus starten, damit der relative Pfad der Beispiel-Konfiguration aufgeloest wird:
BOUKENSHA_DIR=.boukensha python week1_baseline/python/10_standard_tool_library/examples/example.py

# Oder ueber den Launcher, der standardmaessig auf das .boukensha des Repo-Roots zeigt:
./week1_baseline/bin/python/10_standard_tool_library
```

## Tests

```sh
python -m unittest discover -s test -t .
```

Die MCP-Tests starten den echten `mud-manager`-Daemon aus dem Geschwister-
Checkout `week0_explore/mud_manager` (der mit seinem eigenen eingebauten
Fake-MUD kommuniziert, kein Netzwerk noetig) und werden automatisch uebersprungen,
wenn dieser Checkout — oder ein `ruby`-Interpreter, um ihn auszufuehren — nicht
vorhanden ist.

## Technische Anmerkungen

Das sind Beobachtungen, keine sofort zu behebenden Bugs — sie werden hier
festgehalten, damit spaetere Schritte sie nicht versehentlich wieder einfuehren.

- Es koennte vorkommen, dass ein Benutzer, dessen Sitzung bereits in Verwendung
  ist, mit Ja oder Nein zum Beenden der Sitzung aufgefordert wird, und
  Agent/mud_manager hat keine Moeglichkeit, diesen Fall zu behandeln.
- Es scheint, dass mehr Tool-Arbeit benoetigt wird, da moeglicherweise nicht
  genug Tools vorhanden sind, um Aufgaben effizient zu erledigen, und die
  meisten dasselbe Primitive mappen.
- Server werden **eifrig** beim Start gespawnt: Jeder Eintrag kostet einen
  Subprozess und einen Handshake, auch wenn der LLM ihn nie aufruft. Bei zwei
  Servern in Ordnung; ab mehr neu ueberlegen.
- Nicht-Text-MCP-Inhaltsbl&ouml;cke (Bilder, eingebettete Ressourcen) werden
  verworfen statt gerendert — sie liefern einen leeren String, keine Ausnahme.
  Kein MUD-Tool kann das ausloesen.
- Die Backends deklarieren jeden aufgelisteten Parameter als erforderlich, was
  fuer Drittanbieter-Server mit genuinen optionalen Parametern falsch ist. Die
  Behebung erfordert, `inputSchema["required"]` durch `boukensha.tool.Tool`
  durchzureichen, was alle Tools beruehrt.
