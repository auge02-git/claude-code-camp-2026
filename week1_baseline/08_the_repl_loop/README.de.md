# 08 · Die REPL-Schleife (Python-Port)

Python-3-Port von [`ruby/08_the_repl_loop`](../../ruby/08_the_repl_loop/README.md). Gleiches
Design — vollständige Überlegungen sind in der Ruby-README beschrieben. Dieses Dokument
behandelt die Python-spezifische Implementierung und die Unterschiede zur Ruby-Vorlage.

Step 7's `boukensha.run` führt eine einzelne Aufgabe aus und gibt zurück. Step 8 fügt
`boukensha.repl` hinzu — eine interaktive Schleife, die aktiv bleibt, Aufgaben von stdin
liest und den Agenten Turn für Turn ausführt. Der `Context` wird über alle Turns hinweg
geteilt, sodass sich der **Konversationsverlauf ansammelt**: Der Agent sieht das vollständige
Protokoll bei jedem neuen Turn.

|  | `run` | `repl` |
|---|---|---|
| Turns | einer | viele |
| Verlauf | wird verworfen | sammelt sich über Turns an |
| Benutzerinteraktion | keine | stdin-Prompt |

## Neue Dateien (gegenüber Step 7)

| Datei | Zweck |
|---|---|
| `boukensha/repl.py` | `Repl` — die interaktive Sitzungsschleife + eingebaute Befehle |
| `boukensha/version.py` | `VERSION = "0.8.0"` |

## `boukensha.repl(...)`

Gleiche Optionen wie `run`, **ohne `task`** (der Benutzer gibt Aufgaben interaktiv ein).
Tools werden im `setup`-Callback registriert; danach übernimmt die Schleife. Eingebaute
Befehle (werden nicht an den Agenten weitergeleitet):

| Befehl | Wirkung |
|---|---|
| `/quiet` | Logging-Ausgabe unterdrücken (`set_quiet(True)`) |
| `/loud` | Wieder aktivieren (`set_quiet(False)`) |
| `/clear` | Konversationsverlauf löschen (Tools bleiben erhalten) |
| `/help` | Befehlsliste anzeigen |
| `/exit` / `/quit` | REPL beenden |
| Ctrl-D | EOF — REPL beenden |
| Ctrl-C | Unterbrechen — sauber beenden |

## Von Ruby übernommene Änderungen

- **`Agent` speichert die finale Antwort.** Der Agent hängt die abschließende
  Assistenten-Antwort nun bei jedem Beendigungspfad (abgeschlossen / Wind-down / Fallback) an
  den Context an. Einmaliges `run` verwirft den Context, aber die REPL benötigt das vollständige
  Protokoll, damit der nächste Turn den vorherigen Austausch sieht.
- **`Context.clear_messages()`** löscht den Verlauf, während Tools und System-Prompt erhalten
  bleiben (Ruby's `clear_messages!`; Python lässt das `!` weg). Wird von `/clear` genutzt.
- **`Client`** wirft ein verständliches `ApiError("authentication failed (401) …")` bei HTTP 401.
- **`Config._resolve_dir`** prüft in dieser Reihenfolge: `BOUKENSHA_DIR`, dann `./.boukensha`
  im aktuellen Arbeitsverzeichnis, dann `~/.boukensha`.

## Python-spezifische Anpassungen

- Terminal-I/O: `input()` für den Prompt; **Ctrl-D** erscheint als `EOFError` (in der Schleife
  behandelt), **Ctrl-C** als `KeyboardInterrupt` (in der `repl()`-Factory behandelt, wie
  Ruby's `rescue Interrupt`).
- `/quiet` / `/loud` entsprechen `boukensha.set_quiet(True/False)`.
- Wie in Ruby wird `quiet()` derzeit nur *gesetzt* — nichts liest es bisher, um die
  Datei-Protokollierung zu unterdrücken; es ist als Infrastruktur für spätere Schritte
  portiert.
- `repl.py` macht `import boukensha` am Modul-Anfang, greift aber auf `boukensha.set_quiet`
  erst zur Laufzeit zu, sodass der Package/`repl`-Zirkelimport sauber aufgelöst wird.

## Starten

```
bin/python/08_the_repl_loop.sh   # aus week1_baseline/
```

Gibt ein Banner aus, dann einen `boukensha> `-Prompt. Versuche `list the files in .` und
dann `read README.md`. Das Trace jedes Turns landet in `.boukensha/sessions/*.jsonl` (mit
einer `turn`-Zeile je Turn). Führe `bin/08_the_repl_loop_ruby` für die byte-kompatible
Ruby-REPL aus.
