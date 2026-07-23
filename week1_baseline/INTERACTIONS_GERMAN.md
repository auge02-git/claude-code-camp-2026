# Was ist das Ziel fuer Woche 1?

Wir wollen einen Baseline-Agenten bauen, der alle gaengigen Komponenten enthaelt, um jede Art von Agenten zu erstellen. Er sollte enthalten:
- eine einfache agentische Schleife
- ein Tool-Registry zusammen mit Tools
- Unterstuetzung fuer mehrere Backends
- Logging-Faehigkeit
- eine DSL, damit wir den Agenten wie ein SDK nutzen koennen
- globale Binary-Ausfuehrung, damit wir ueber die CLI interagieren koennen
- eine CLI-Option fuer das Modell
- Kontextverwaltung und Nachrichten-Komprimierung bei erreichtem Limit
- ein eigenes Konfigurationsverzeichnis

Ein weiterer Punkt:
- Log-Visualizer, damit wir Logs im Browser besser ansehen koennen.

## Was sollte der Baseline-Agent koennen?
Er sollte MUD spielen koennen, auch wenn wir ihm konkrete Befehle geben muessen.

## Was wird er nicht koennen?
Er wird eine schwache Wahrnehmung haben, da ihm Memory-Management, Entscheidungsfindung und Token-Effizienz fehlen.

## Technische Design-Ueberlegungen
- Wir verwenden REST-APIs direkt, damit wir verstehen, wie einfach die Interaktion mit Managed APIs ist und wie stark sie sich unterscheiden.
- Manche SDKs, selbst offizielle, legen nicht alle Features offen; REST-APIs geben vollen Zugriff auf Feature-Sets.
- Wir verwenden Ruby, aber Endnutzer koennen auf andere Sprachen portieren.
- Wir muessen den Ruby `MudManager` fuer die MUD-Interaktion verwenden.
- Wir sollten moeglichst die Standard Library (STD) nutzen und Drittanbieter-Bibliotheken vermeiden.

### Was sollten wir nicht verwenden?

- Wir sollten keine Agent-SDKs verwenden, da diese bereits Features implementieren, die wir selbst von Grund auf bauen wollen.
  - Sie koennen auch einschranken, was wir exakt umsetzen koennen.
  - z. B. kein OpenRouter, kein Amazon Strands, kein OcreAgent, kein LangChain
- Wir sollten den Coding-Harness nicht zur Steuerung des Agenten nutzen, da er nicht fuer diese Agentenaufgabe gedacht ist.

## Strukturansatz erklaert

Der Ordner `ruby/` enthaelt die schrittweisen Iterationen unseres Agenten.

### Ueberlegungen
- Wir werden manuelle Anpassungen brauchen, da der urspruengliche Code im Ruby-Unterordner nicht vorhanden war.
- KI hat handgeschriebenen Code beeinflusst; wir markieren Teile, die neu geschrieben werden sollten, lassen aber evtl. manches unangetastet, um spaetere Layer nicht zu stoeren.
- Wir koennen und werden den Code nach Python portieren; dabei muessen wir sicherstellen, dass die Ruby-Version des MudManager mit Ruby und Python funktioniert.

## Vorgehensweisen fuer Studierende
Als Student hast du etwas Flexibilitaet, wie du durch diese Woche gehst.
- Du kannst exakt mitgehen und die Ruby-Aenderungen machen.
  - Du kannst die Ruby-Implementierung als Hauptimplementierung behandeln.
- Wenn du kein Interesse an der Python-Portierung hast, kannst du diese Videos komplett ignorieren.
- Du kannst alle Videos schauen und dann nur die letzte Ruby-Iteration in deine Zielsprache portieren.
- Du musst Ruby nicht portieren, aber du wirst es in Woche 2 brauchen, wenn wir zusaetzliche Faehigkeiten implementieren.

## Baseline-MUD-Agent
**Was dir die Baseline gibt:**

Der Baseline-MUD-Agent ist ein voll funktionsfaehiger MUD-Agent, der sich mit einem tbaMUD-Server verbinden, sich als Charakter einloggen und diesen ueber natuerliche Sprache steuern kann.

**Was dir die Baseline gibt:**

- Eine persistente TCP-Session zum MUD-Server, die ueber Tool-Calls hinweg verbunden bleibt
  - technisch haelt `MudManager` die Verbindung persistent
- Fuenf austauschbare LLM-Backends (Anthropic, OpenAI, Gemini, Ollama, Ollama Cloud) hinter einer normalisierten Request/Response-Form, pro Task in `settings.yaml` konfigurierbar
  - Andrew implementiert 5 Backends; als Student kannst du nur eines oder mehrere nutzen
- MUD-Tools fuer alle Kernaktionen: Bewegung, Kampf, Wahrnehmung, Inventar, Magie und Kommunikation
  - `MudManager` implementiert zentrale Aktionen, aber einige fehlen (z. B. Diebes-Kommandos, Rest-Kommandos). Das sollte spaetestens Ende Woche 1 oder in Woche 2 adressiert werden.
- Eine Standard-Tool-Library fuer Datei-I/O und Shell-Befehle, damit der Agent auch lokalen Zustand lesen/schreiben kann
  - Diese Tools spiegeln die `MudManager`-Tools und brauchen vermutlich Ueberarbeitung (passiert in Woche 1)
- Eine Multi-Turn-REPL fuer eine laufende Konversation waehrend der Agent spielt
- Vollstaendige Konversationshistorie ueber Turns hinweg, damit der Agent sich erinnert, was er gesehen und getan hat
  - Das sind die Session-Log-Dateien; man koennte fruehere Gesprache laden, aber diese Features sind im MUD noch nicht umgesetzt.
- Farbige, strukturierte Logs fuer jeden API-Call, Tool-Dispatch und jede Antwort
  - Technisch gibt es etwas Farbgebung; der Browser-Logger liefert mehr Informationen.

**Was noch fehlt** (kommt in spaeteren Iterationen):
- Langzeitgedaechtnis ueber das aktuelle Konversationsfenster hinaus
- Ein Weltmodell oder eine Karte aus Exploration
- Zielplanung, taktisches Denken oder autonomes Verhalten
- Charakterfortschritt-Tracking oder Strategie

Fuer viele Schritte haben wir eine Klasse pro Thema, z. B. `Configuration` in `config`, REPL in `repl.rb`.

### 0 Konfiguration
`Boukensha::Config` und das Verzeichnis `~/.boukensha` speichern alle Konfigurationsdaten inklusive Secrets, Prompts, Logging (Sessions) und Settings-Datei.
Wir haben die Umgebungsvariable `BOUKENSHA_DIR`, mit der man den Standardpfad (Home-Verzeichnis) ueberschreiben kann.
Wir nutzen den `.dotenv`-Standard fuer Secrets und brauchen die `dotenv`-Bibliothek.
> Wenn wir einen Agenten bauen, der auf mehreren Servern laeuft, ist ein Konfigurationsverzeichnis sinnvoll.

### 1 Das Struct-Skelett
Definiere `Boukensha::Tool`, `Boukensha::Message` und `Boukensha::Context` als einfache Datencontainer. Noch keine Logik, nur die Datenformen.

Wir definieren damit die zentrale Datenstruktur fuer den Datentransport.

### 2 Das Tool-Registry
Das Tool-Registry verwaltet eine Tabelle moeglicher Tools und dispatcht Tools bei Aufruf.
Mit anderen Worten: Es matched einen Prompt-Aufruf mit dem passenden Tool.
> Es wurde festgestellt, dass die KI die Implementierung spaeter regressiv veraendert hat und `Context` weiterhin Tools verwaltet. Das ist nicht korrekt; `tools[]` sollte ins Tool-Registry verschoben werden.

### 3 Der Prompt-Builder
Da wir mehrere Backends per direkten REST-API-Requests ansprechen, muessen wir ihre Schema-Strukturen exakt kennen.
Also muessen wir diese erwarteten Strukturen bauen.
Ausserdem muss der Prompt-Builder Antworten auf ein einheitliches Format normalisieren.
> Denk-Optionen der Modelle muessen beachtet werden: Manche Modelle haben Thinking standardmaessig aktiv, andere nicht, manche koennen es nicht deaktivieren. Es gibt weitere Parameter fuer Fine-Tuning, aber in den Videos war dafuer wenig Zeit.

### 4 Der API-Client
Der API-Client ist ein Low-Level-HTTP-Client, der direkte REST-API-Calls ausfuehrt.
> Wir haben am Ende den OpenSSL-Pfad hart codiert; der unterscheidet sich je nach Windows, macOS oder Linux. Ein Drittanbieter-HTTP-Client wie HTTPParty oder Faraday wuerde das loesen, abstrahiert aber mehr und verdeckt Teile des Ablaufs. Daher wurde der Code fuer die Laufumgebung direkt angepasst.

### 5 Die Agenten-Schleife
`Boukensha::Agent` - die zentrale agentische Schleife. Ruft die API auf, prueft `stop_reason`, dispatcht Tool-Calls ins Registry, haengt Ergebnisse an den Kontext an und wiederholt, bis `end_turn` oder `MAX_ITERATIONS` erreicht ist. Fuegt `Boukensha::Errors` (`LoopError`, `ApiError`) hinzu und verbindet alles in `Boukensha.run`.
Zusatzlich werden OpenAI-, Gemini- und Ollama-Cloud-Backends neben Anthropic und Ollama aktiviert. Jedes implementiert `parse_response`, um rohe Antworten in eine normalisierte Form `{stop_reason:, content:}` zu bringen, damit `Agent` den Provider nicht kennen muss.
> Wie zuvor erwaehnt, brauchen wir die Normalisierung der Antworten im Prompt-Backend; hier passiert das vermutlich im Prompt-Builder und den jeweiligen Backends.

### 6 Der Logger

Wir erstellen einen Logger, der Session-Logs in `~/.boukensha/sessions/<date>-<session_id>.json` speichert.
> Es gibt eine `log_viz`-App (einfache Sinatra-App) zur Visualisierung der Sessions. Langfristig sollten wir sie nach TypeScript portieren und in Echtzeit faehig machen.

Wir speichern explizit Modell, Provider und Kosten, um moeglichst viele Details pro Aufruf zu erfassen und waehrend einer Konversation auch den Agenten wechseln zu koennen (auch wenn dafuer in der CLI noch Befehle fehlen).

### 7 Die Run-DSL
Bis hierhin muessen viele Klassen instanziiert werden; das wird schnell unuebersichtlich.
Darum implementieren wir einen einzigen `.run`-Aufruf, der die Komplexitaet abstrahiert und eine SDK-aehnliche Schnittstelle bietet.

`Boukensha::RunDSL` - das Objekt, das innerhalb eines `Boukensha.run { }`-Blocks zu `self` wird. Es bietet eine einzelne `tool`-Methode, damit Aufrufer ad-hoc Tools inline neben der Aufgabe registrieren koennen. So bleibt die DSL klein und die Signatur von `Boukensha.run` sauber.

### 8 Die REPL-Schleife

Sie ermoeglicht eine interaktive Schleife im Terminal.
`Boukensha::Repl` - eine interaktive Session, die ueber Turns hinweg aktiv bleibt. Liest Nutzereingaben, fuehrt den Agenten aus, gibt Antworten aus und springt zum Prompt zurueck. Ein einzelner `Context` wird fuer alle Turns geteilt, damit der Agent die komplette Historie sieht. Eingebaute Befehle: `/quiet`, `/loud`, `/clear` (Historie loeschen, Tools behalten), `/exit`, `/quit`, `/help`.
Fuegt `Boukensha::VERSION` hinzu.

### 9 Global Executable

Damit koennen wir `boukensha` von ueberall im Terminal aufrufen.
> Hier kommt `.boukensharc` dazu, womit Konfigurationspfad und aktueller Gem-Pfad fuer das Laden der `boukensha`-Binary gesetzt werden koennen; diesen Code tragen wir in spaeteren Schritten weiter.

Alles wird als installierbares Gem verpackt, sodass der Befehl `boukensha` systemweit verfuegbar ist. Hinzu kommen `boukensha.gemspec`, `bin/boukensha` und `lib/boukensha_loader.rb`.
Der Loader bestimmt den zu nutzenden Step-Ordner in Prioritaetsreihenfolge: `BOUKENSHA_PATH`-Umgebungsvariable, `~/.boukensharc`-Datei, dann gebuendelter Standard.
`BOUKENSHA_DEBUG=1` zeigt beim Start den aufgeloesten Pfad.

```sh
cd @9_global_executable

gem build boukensha.gemspec

gem install boukensha-0.9.0.gem

BOUKENSHA_PATH=/Sites/boukensha/@9_global_executable boukensha
```

Ab hier liefert jeder Schritt sein eigenes Gem auf die gleiche Weise (`gem build boukensha.gemspec && gem install boukensha-<version>.gem`) - setze `BOUKENSHA_PATH` auf den jeweiligen Step-Ordner, den du ausfuehren willst.
> Diesen Schritt ueberspringen wir bei der Python-Portierung. Unklar, ob das eine schlechte Idee war, aber so wurde es gemacht.

### 10 Standard Tool Library - MCP Host

Wir implementieren ein Tool-Mapping fuer den Agenten aus dem MudManager.
Beim Port nach Python gab es jedoch keinen Zugriff der Python-App auf die Ruby-Version des MudManager, daher wurde MCP implementiert.

> Die MCP-Implementierung ist ein 2-Stunden-Video und sehenswert, aber nicht zwingend nachzubauen; empfohlen wird, MudManager und `10_standard_tool_library` aus dem Omenking-Repo zu uebernehmen.
> Wegen der grossen Codeaenderungen musste viel Code weitergetragen werden, was den Ruby-Schritt aufwendiger macht.

Dieser Schritt lieferte urspruenglich drei eingebaute Tool-Module (`Tools::FileSystem`, `Tools::Shell`, `Tools::Mud`).
Dieser Code wurde inzwischen **geloescht und ersetzt** durch einen MCP-Host-Rewrite, der auch fuer alle folgenden Schritte gilt. Das Verzeichnis behaelt nur den Namen `10_standard_tool_library`, damit Reihenfolge und bestehende Pfade weiterhin stimmen.

### 11 Terminal UI
TUI ist im Grunde eine bessere REPL mit erweiterten Anzeige-Features im Terminal.
> In Ruby nutzen wir Charm's BubbleTea fuer die TUI. Die KI ging davon aus, dass BubbleTea fuer Python nicht verfuegbar ist, und verwendete daher Textual. Mit `log_viz` brauchen wir eigentlich keine TUI; in der urspruenglichen Implementierung kam `log_viz` spaeter.

Fuegt eine vollwertige Terminal-UI (TUI) ueber dem MCP-Host-Toolmodell hinzu, gebaut auf dem [charm](https://github.com/charm-ruby/charm)-Gem (bubbletea + lipgloss + bubbles). Die einfache REPL bleibt ueber `tui: false` erhalten.

- **`Boukensha::Tui`** - kapselt eine `Repl` und ersetzt rohe `puts`/`gets` durch eine Vier-Zonen-Anzeige: scrollbarer Konversationsbereich, Live-Fortschrittszeile (Spinner, Iterationszaehler, Laufzeit, Token-Anzahl, Tool-Call-Anzahl), Eingabefeld und dauerhafte Statuszeile (Version, Modell, verwendete/maximale Kontext-Token, Tool-Anzahl, Uhrzeit). Der Agent laeuft in einem Hintergrund-Thread, damit die UI waehrend eines Turns reaktionsfaehig bleibt.

- Tastaturkuerzel: `Enter` senden, `Esc` laufenden Turn unterbrechen, `Ctrl+L` Historie loeschen, `PgUp`/`PgDn` scrollen, `Ctrl+C`/`Ctrl+D` beenden.

### 12 Context Management

Beim direkten LLM-Aufruf gibt es keine automatische Komprimierung - fuer das Kontextfenster bist du selbst verantwortlich.
Dieser Schritt fuegt sauberes Token-Tracking, visuelle Warnungen und automatische Komprimierung auf Basis des MCP-Host-Toolmodells und der TUI aus Schritten 10-11 hinzu.
> Es sollten Settings verfuegbar sein, um z. B. das 600er-Limit auf 60.000 anzuheben; der aktuelle Wert ist sehr niedrig. In Woche 1 wurde das nicht getestet, aber es ist vermutlich anpassbar.

- **Praezises Token-Tracking** - `Context` verfolgt jetzt `context_window` (maximale Eingabekapazitaet des Modells aus `Boukensha::Models.context_window(model)`) getrennt von `current_tokens` (tatsaechliche Nutzung aus der letzten API-Antwort). Damit wird eine fruehere Anzeige korrigiert, die Output-Token-Budget und Kontextfenster vermischt hat und eine kumulative Session-Summe ungebremst wachsen liess, selbst nach `/clear`.

- **`Boukensha::Models`** - eine statische Modell-zu-Faehigkeiten-Tabelle aus den Modelllisten aller Backends, damit `Context` korrekt dimensioniert werden kann, bevor ein Backend konstruiert wird. Unbekannte Modelle fallen auf einen konservativen Default zurueck, statt ein riesiges Fenster anzunehmen.

- **Auto-Kompaktierung** - zu Beginn jedes Turns, wenn die Nutzung `agent.compaction_threshold` (Default `0.85`) ueberschreitet, entfernt `Context#compact_messages!` die aeltesten `40%` der Nachrichten (mindestens 2 bleiben erhalten), bevor der naechste API-Call startet. `/compact` triggert das manuell aus REPL oder TUI. Es wird ein `Logger#compaction`-Event erzeugt, das die TUI als Hinweis in der Konversationsansicht darstellt.

- **Zweiter Circuit Breaker** - `Agent` beendet einen Turn jetzt bei dem zuerst ausloesenden Limit: `max_iterations` (Tool-Call-Anzahl) oder `max_turn_tokens` (kumulierte Input+Output-Token in diesem Turn). Beide Werte kommen aus dem `agent:`-Block in `settings.yaml`.

- **Normalisierte Reasoning-Bloecke** - jedes Backend liefert provider-spezifische `thinking`-Ausgaben (Anthropic `thinking` / `redacted_thinking`, Gemini `thought` / `thoughtSignature`, Ollama `message["thinking"]`) als einheitlichen Content-Block `{"type" => "reasoning", ...}`, geloggt via `Logger#reasoning`.

- **OpenAI-Backend nach `/v1/responses` verschoben** - `gpt-5.x` lehnt `reasoning effort` + Tools auf `/v1/chat/completions` ab. Nachrichten werden zu `input`-Items, der System-Prompt zu einer top-level `instructions`-Zeichenkette, und Tool-Ergebnisse laufen als `function_call_output`-Items mit passender `call_id` zurueck.

- **`Boukensha.run` / `.repl`** - das Keyword `context_window:` ersetzt `token_budget:`; Standard ist `Models.context_window(model)`.
- **`Logger#response` Kosten-Metadaten** - jedes Response-Event traegt jetzt Provider, Modell und Kosten.

## Noch nicht gebaut

Folgende Punkte wurden in einer frueheren Version dieses Dokuments als Roadmap skizziert, aber noch nicht begonnen - es gibt in `ruby/` bislang keinen Orchestrator, keinen Turn-Counter-Wrapper und keinen Memory-Store-Code:
- Eine Orchestrator-Schicht um die bestehende Agenten-Schleife (Turn-Zaehlung, ein `orchestrator.run_turn()` als "Executor"-Stage)
- Persistente Memory-Stores - Welt, Charakter, Episodisch, Semantisch - ueber das aktuelle Konversationsfenster hinaus

## Architecture — Final Baseline (Step 12)

```
                         ┌───────────────────────┐
                         │    Boukensha::Tui     │  viewport / progress
                         │    (or plain Repl)    │  / input / status line
                         └───────────┬───────────┘
                                     │ run_turn(input)
                                     ▼
                         ┌───────────────────────┐
                         │   Boukensha::Agent    │  max_iterations
                         │    the agent loop     │  max_turn_tokens
                         └───────────┬───────────┘  compaction_threshold
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
          ┌────────────────┐┌────────────────┐┌────────────────┐
          │    Context     ││    Client      ││   Registry     │
          │  messages      ││ → Backends::   ││  dispatch()    │
          │  tools         ││   Anthropic    │└───────┬────────┘
          │  current_tokens││   OpenAI       │        │
          │  context_window││   Gemini       │        ▼
          │  compact_msgs! ││   Ollama       │┌────────────────┐
          └────────────────┘│   OllamaCloud  ││  Tools::Mcp    │
                            └────────────────┘│  (prefix: ns)  │
                                              └───────┬────────┘
                                                      │ stdio
                                                      ▼
                                            ┌───────────-────────────┐
                                            │      Mcp::Client       │
                                            │ spawn / handshake /    │
                                            │ tools_list / tools_call│
                                            └─────┬─────────────┬────┘
                                                  ▼             ▼
                                        ┌───────────────┐┌───────────────┐
                                        │ mud-manager   ││ filesystem /  │
                                        │ --mcp         ││ shell / other │
                                        │ (CircleMUD)   ││ MCP servers   │
                                        └───────────────┘└───────────────┘

   Logger#subscribe leitet jedes Ereignis (Iteration, tool_call, tool_result, 
   response, compaction, reasoning) gleichzeitig an zwei Orte weiter: 
   die Live-Fortschrittszeile der TUI und eine JSONL-Datei auf der Festplatte.
```