# 09 · Globale Executable (Python-Port)

Python-3-Port von [`ruby/09_global_executable`](../../ruby/09_global_executable/README.md). Gleiches
Design — die vollständigen Überlegungen stehen im Ruby-README. Dieses Dokument behandelt die
Python-spezifische Implementierung.

Dieser Schritt verpackt BOUKENSHA als **globalen `boukensha`-Befehl**. Die Bibliothek selbst bleibt
unverändert (ein Versions-Bump und ein paar kleine Rücknahmen); neu ist ein *Loader*, der den
auszuführenden Schritt-Ordner auflöst und die REPL startet.

## Was dieser Schritt hinzufügt

| Datei | Zweck |
|---|---|
| `bin/boukensha` | Die ausführbare Datei — macht den Loader importierbar und übergibt an ihn |
| `boukensha_loader.py` | Eigenständiges Modul: löst auf, *welchen Schritt* geladen wird, und startet die REPL |
| `pyproject.toml` `[project.scripts]` | `pip install .` → `boukensha` auf `$PATH` (das pip-Äquivalent des Gems) |

Der Loader ist ein **Top-Level-Modul, bewusst außerhalb des `boukensha/`-Pakets** — spiegelt
Rubys `lib/boukensha_loader.rb` wider, das außerhalb von `lib/boukensha/` liegt — sodass er
das `boukensha`-Paket eines *anderen* Schritts namentlich importieren kann.

## Wie ein Schritt ausgewählt wird

Der Loader löst in dieser Reihenfolge auf:

| Priorität | Quelle | Beispiel |
|---|---|---|
| 1 | Umgebungsvariable `BOUKENSHA_PATH` | `BOUKENSHA_PATH=~/…/python/07_the_run_dsl boukensha` |
| 2 | Datei `~/.boukensharc` | `echo ~/…/python/08_the_repl_loop > ~/.boukensharc` |
| 3 | Eingebetteter Standard | einfach `boukensha` ausführen (eigenes Paket dieses Schritts) |

`BOUKENSHA_PATH` muss auf einen Schritt-Ordner zeigen, der eine `boukensha/__init__.py` enthält.
**„Einen Schritt laden"** bedeutet in Python: dieses Verzeichnis in `sys.path` einfügen und dann
`import boukensha` ausführen.

Das Konfigurationsverzeichnis (`settings.yaml`, `.env`, `system.md`) ist davon getrennt — gesteuert
durch `BOUKENSHA_DIR` (Standard: `~/.boukensha`).

## Ausführen

```bash
bin/09_global_executable_python                     # von week1_baseline/ — eingebetteter Standard
BOUKENSHA_DEBUG=1 bin/09_global_executable_python   # gibt "[boukensha] loading from: …" aus
```

Oder installieren, damit `boukensha` von überall funktioniert:

```bash
cd week1_baseline/python/09_global_executable
pip install .        # macht das `boukensha`-Console-Script verfügbar
boukensha            # führt die REPL des eingebetteten Schritts aus
BOUKENSHA_PATH=$PWD/../07_the_run_dsl boukensha   # stattdessen Schritt 7 ausführen
```

Ein Schritt, der älter als die REPL ist (vor Schritt 7), hat kein `repl` — der Loader bricht dann
mit einem Hinweis ab, `BOUKENSHA_PATH` auf Schritt 7 oder neuer zu zeigen.

## Änderungen gegenüber Schritt 8

- `VERSION` → `0.9.0`.
- `Config._resolve_dir` kehrt zu `BOUKENSHA_DIR` || `~/.boukensha` zurück (entfernt die cwd-Suche aus Schritt 8).
- `Client` behandelt HTTP 401 nicht mehr als Sonderfall.
- Das REPL-Banner wurde vereinfacht: keine API-Key-/Verzeichnis-Prüfungen; nur noch einfache `config`- / `provider`- / `model`-Zeilen.
- Kein `examples/`-Ordner — der Einstiegspunkt ist jetzt `bin/boukensha`.
