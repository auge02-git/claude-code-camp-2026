# Architektur-Exploration: Erkenntnisse aus den Teilschritten

## Ziel
Die Teilschritte definieren einen schlanken Agenten-Workflow mit klarer Sprach- und Kontextsteuerung, um Tokenverbrauch zu reduzieren und Off-Task-Verhalten zu vermeiden.

## Teilschritte (konsolidiert)
1. Modellwahl nach dem Start:
   - `bedrock/eu.anthropic.claude-haiku-4-5-20251001-v1:0` (Default)
   - alternativ `bedrock/eu.anthropic.claude-sonnet-4-6`
2. Kontextspezifische Datei lesen: `docs/explore_architectures.md`.
3. Alle Ausgaben und Systemmeldungen auf Deutsch halten.
4. Agenten-Datei mit Referenzen auf zentrale Wissensquellen pflegen, z. B.:
   - `AGENTS.md`
   - `docs/**/*.md`
   - `docs/CLAUDE.md`
5. Ausgabe kompakt halten (minimierte Output-Tokens).

## Beobachtungen und Erkenntnisse
- Der Coding-Harness liest lokale Dateien auch dann, wenn sie nicht zum aktuellen Loop gehoeren.
  - Effekt: Kontextdrift, unnoetiger Tokenverbrauch, geringere Zielgenauigkeit.
- Agenten haben temporaere Socket-Skripte erzeugt, um MUD-Kommandos auszufuehren.
  - Effekt: fragiles Verhalten, hoher Overhead, inkonsistente Ausfuehrung.
- Bei Login-Fehlern in starren Skripten wurde Off-Task nach Konfigurationsdateien gesucht.
  - Effekt: Fehlereskalation statt kontrollierter Recovery im eigentlichen Ablauf.

## Abgeleitete Architektur-Empfehlungen
- Eine persistente, gemeinsame Schnittstelle fuer MUD-Zugriffe verwenden (z. B. `mud_manager`).
- Login-/Session-Handling zentral kapseln statt pro Agent neu zu skripten.
- Kontextzugriffe strikt begrenzen: nur Dateien laden, die fuer den aktuellen Schritt notwendig sind.
- Fuer kleine Modelle robuste, fehlertolerante Standardpfade bereitstellen (statt rigider Einmal-Skripte).

## Praktische Leitlinie fuer Agent-Runs
- Erst Modell und Sprache fixieren, dann nur notwendige Dateien laden.
- Bei Verbindungs-/Login-Fehlern auf gemeinsame Session-API fallbacken.
- Antworten kurz halten und nur entscheidungsrelevante Informationen ausgeben.

