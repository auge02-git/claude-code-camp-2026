# Anleitung zur Weiterentwicklung der Boukensha-Journey-Anweisungen

## Zweck

Diese Anleitung beschreibt, wie die Journey-Anweisungen fuer den Boukensha-Agenten
schrittweise verbessert werden.
Sie basiert auf den bisherigen Umsetzungen in den Reports `v3` bis `v7`, den Session-Logs,
den Hand-Agent-Outputs und den dokumentierten Ergebnissen in `docs/todo_week0_d3.md`.

Ziel ist, aus echten Durchlaeufen systematisch bessere, kuerzere, sicherere und
EXP-effizientere Anweisungen abzuleiten.

---

## Zielbild

Jede neue Journey-Version soll:

1. **sicherer** sein als die vorherige
2. **weniger Schleifen und Sackgassen** erzeugen
3. **mehr EXP pro Minute** ermoeglichen
4. **bekannte Fehlerbilder explizit vermeiden**
5. **konkrete, maschinell nutzbare Anweisungen** enthalten
6. **reale Beobachtungen aus Logs** in stabile Regeln umwandeln

---

## Verwendete Eingabequellen

Fuer eine neue Journey-Version werden typischerweise diese Quellen ausgewertet:

### 1. Basis-Report der letzten stabilen Version
Beispiel:
- `week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v6.txt`

Diese Datei liefert die aktuelle Arbeitsgrundlage:
- harte Regeln
- sichere Routen
- bekannte Risiken
- aktuelle Kampf-/Farm-Logik

### 2. Reale Bewegungs- und Welt-Logs
Beispiele:
- `week0_explore/boukensha/journeys/mud-journeys-2026-07-15.log`
- `week0_explore/logs/mud-journeys-2026-07-15_v6.log`

Diese Logs liefern:
- echte Raumfolgen
- funktionierende Wege
- problematische Wege
- neue Points of Interest
- Exits und Raumzusammenhaenge

### 3. Reflektierende Agenten-Logs
Beispiele:
- `week0_explore/logs/hand-agent-output-2026-07-15_8.log`

Diese Logs liefern:
- Denkfehler des Agenten
- falsche Prioritaeten
- wiederkehrende Fehlmuster
- Verbesserungsideen fuer Prompting und Ablauf

### 4. Meta-Dokumentation
Beispiel:
- `docs/todo_week0_d3.md`

Diese Datei dokumentiert:
- was bereits umgesetzt wurde
- welche Versionen angelegt wurden
- welche Struktur eine neue Version haben soll
- welche Verbesserungen bereits erfolgreich waren

---

## Standardprozess fuer eine neue Journey-Version

### Schritt 1 - Letzte stabile Version als Basis festlegen
Nimm immer die letzte brauchbare Journey-Datei als Ausgangspunkt.

Beispiel:
- `v6` als Basis fuer `v7`

Regel:
- nicht bei Null anfangen
- vorhandene sichere Regeln uebernehmen
- nur neue Erkenntnisse ergaenzen oder alte Regeln praezisieren

### Schritt 2 - Neue Logs gezielt gegen die Basis lesen
Vergleiche neue Logs mit der bestehenden Version.

Fragen dabei:
- Welche neuen Fehler sind aufgetreten?
- Welche alten Fehler sind erneut aufgetreten?
- Welche Regeln haben funktioniert?
- Welche Regeln waren unklar oder unvollstaendig?
- Welche neuen sicheren Routen oder Anker wurden beobachtet?
- Gibt es neue Risiko-Zonen?
- Gibt es neue Systemprobleme wie Void, Timeout, fehlende Ausgaben?

### Schritt 3 - Erkenntnisse in Kategorien einordnen
Alle neuen Beobachtungen muessen sauber klassifiziert werden.

Empfohlene Kategorien:
- **Kern-Erkenntnisse**
- **Neue Kern-Erkenntnisse**
- **Harte Regeln**
- **Sichere Navigationsanker / Routen**
- **Farm-Logik**
- **Aggressiver Modus / EXP-Maximierung**
- **Notfall-/Recovery-Strategien**
- **Optionale /btw-Hinweise**

### Schritt 4 - Nur verifizierte Fakten in Regeln ueberfuehren
Wichtig:
- Nur Dinge als feste Regel aufnehmen, die in Logs oder mehreren Runs bestaetigt wurden.
- Vermutungen klar als optional markieren.

Beispiele fuer **verifizierte Regeln**:
- `Common Square -> west -> Eastern End Of Poor Alley` funktioniert
- Main Street ist Wachen-Risiko
- `has arrived` -> sofort `flee`
- Void braucht Recovery-Sequenz

Beispiele fuer **nicht-harte Regeln / optional**:
- Pet Shop koennte situativ interessant sein
- Bank/ATM spaeter verwenden
- aggressiver leveln nur wenn HP-Puffer stabil ist

### Schritt 5 - Konkrete Agenten-Ziele formulieren
Die Journey muss operative Schritte enthalten, nicht nur Analyse.

Gute Form:
- klare Ueberschrift
- kurze Begruendung
- konkrete Sequenz

Beispiel:
- `score`
- `look`
- `drink fountain`
- `kill fido`
- `kick fido`
- `get all corpse`
- `eat meat`
- `quit`

Regel:
- Jede Anweisung muss fuer einen Agenten direkt ausfuehrbar oder interpretierbar sein.

### Schritt 6 - Neue Fehlerbilder explizit als Vermeidungsregeln schreiben
Nicht nur ergaenzen, was getan werden soll, sondern auch, was vermieden werden muss.

Typische Fehlerbilder aus den bisherigen Laeufen:
- Schleifen auf `Main Street`
- Sackgassen am `East Gate`
- Pet-Shop-Leerlauf
- Wachen-Pinning
- Void-Zustaende
- API-Timeouts durch zu schnelle Folgekommandos
- zu viele `look`-Serien ohne Folgeaktion
- unbestaetigte Richtungen raten

### Schritt 7 - Optionale aggressive Strategie getrennt halten
Schnelleres Leveln ist sinnvoll, aber darf die Sicherheitslogik nicht zerstoeren.

Deshalb:
- aggressiven Modus als **eigene Sektion** schreiben
- harte Abbruchbedingungen explizit nennen
- klare Voraussetzungen definieren

Beispiel:
- nur in wachfreien Raeumen
- nur mit HP-Puffer
- nur mit sicherem Fluchtweg
- `kill` + `kick` als Beschleuniger
- bei `has arrived` sofort Rueckschaltung auf Sicherheitsmodus

### Schritt 8 - Neue Version als neue Datei ablegen
Dateimuster:
- `erfahrung_durchlaeufe_v3.md`
- `erfahrung_durchlaeufe_v4.txt`
- `erfahrungen_durchlaeufe_v5.txt`
- `erfahrung_durchlaeufe_v6.txt`
- `erfahrung_durchlaeufe_v7.txt`

Empfehlung:
- kuenftig moeglichst konsistent `erfahrung_durchlaeufe_vX.txt` verwenden
- neue Version nie alte Version ueberschreiben
- immer neue Nummer vergeben

---

## Empfohlene Struktur einer neuen Journey-Datei

Eine neue Journey-Datei sollte nach diesem Muster aufgebaut sein:

1. **Kopfbereich**
   - Quelle
   - Stand
   - Ziel

2. **Kern-Erkenntnisse**
   - wichtigste neuen Learnings aus dem Lauf

3. **Neue Kern-Erkenntnisse**
   - neue Themenblöcke wie Void, ATM, Pet Shop, Timeout, aggressiver Modus

4. **Harte Regeln**
   - nicht verhandelbare Sicherheits- und Ablaufregeln

5. **Sichere Navigationsrouten / Anker**
   - verifizierte Wege und Raumpunkte

6. **Operativer Standard-Ablauf**
   - Start
   - Wasser
   - Farmgebiet
   - Kampfzyklus
   - Pendel-/Fallback-Logik

7. **Optionale aggressive Strategie**
   - fuer schnelleres Leveln
   - immer klar begrenzt

8. **Notfall / Recovery**
   - Void
   - Timeout
   - Wachen-Pinning
   - unklare Exits

9. **/btw-Hinweise**
   - optionale Alternativen
   - keine Pflichtlogik

---

## Konkretes Verfahren fuer die Ableitung von v(N+1)

Wenn bereits `vN` existiert, dann:

1. Lies `vN` komplett.
2. Lies die neue Hand-Agent-Datei komplett.
3. Lies die neuen Bewegungs-/Journey-Logs komplett oder gezielt die relevanten Bereiche.
4. Notiere nur die Deltas gegen `vN`.
5. Ordne jedes Delta einer Kategorie zu.
6. Streiche schwache Vermutungen oder markiere sie als optional.
7. Formuliere daraus eine neue `v(N+1)`.
8. Pruefe, ob die neue Version:
   - sicherer ist
   - kuerzer navigiert
   - klarere Recovery-Anweisungen hat
   - fuer den Agenten direkt nutzbar ist

---

## Spezifische Lessons Learned aus der bisherigen Umsetzung

### Bewaehrte Inhalte
- `Temple Square`, `Common Square`, `Eastern End Of Poor Alley`, `Grubby Inn` sind starke Anker.
- Die Route zum Brunnen muss immer explizit bleiben.
- Wachenregeln muessen weit oben und eindeutig stehen.
- `kill -> loot -> eat -> score` ist ein brauchbarer Basiszyklus.

### Bewaehrte Erweiterungen spaeterer Versionen
- Anti-Pinning-Regeln
- Pet-Shop-Falle explizit benennen
- Exits als primaere Navigationsmatrix behandeln
- aggressiver Modus nur optional
- Void-Recovery als feste Sequenz
- API-Timeouts als systemisches Problem dokumentieren
- ATM/Bank nur als Spaetphase und nicht als Kernziel

### Typische Denkfehler des Agenten, die in Anweisungen abgefangen werden muessen
- zu langes Hoffen auf neue Information ohne Raumwechsel
- zu viel Gewicht auf Main Street / East Gate
- Exploration statt Rueckkehr auf bekannte sichere Route
- Kampfdenken in unsicheren Raeumen
- fehlende Trennung zwischen Standardmodus und aggressivem Modus

---

## Minimal-Checkliste vor dem Speichern einer neuen Version

- [ ] Letzte stabile Version als Basis verwendet
- [ ] Neue Logs wirklich ausgewertet
- [ ] Nur verifizierte Erkenntnisse als harte Regeln formuliert
- [ ] Neue Risiken explizit als Vermeidungsstrategie dokumentiert
- [ ] Standardmodus und aggressiver Modus klar getrennt
- [ ] Notfall-/Recovery-Sektion enthalten
- [ ] Navigationsanker aktualisiert
- [ ] Datei als neue Versionsnummer gespeichert

---

## Beispiel aus der letzten dokumentierten Umsetzung

Aus `docs/todo_week0_d3.md`:

- Basis: `erfahrung_durchlaeufe_v6.txt`
- Zusatzquellen:
  - `mud-journeys-2026-07-15.log`
  - `mud-journeys-2026-07-15_v6.log`
  - `hand-agent-output-2026-07-15_8.log`
- Ergebnis: `week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v7.txt`

Die dabei neu aufgenommenen Themen waren:
- Void-Zustand
- Bank/ATM
- neue Navigationspunkte
- erweiterte harte Regeln
- sichere Navigationsrouten A-E
- Void-Verhinderung
- sichere Basis-Route
- aggressiver Modus
- Notfall-/Void-Recovery
- /btw-Hinweise

---

## Kurzformel fuer kuenftige Weiterentwicklung

**Basis lesen -> neue Logs vergleichen -> Deltas extrahieren -> Regeln/Routen/Recovery aktualisieren -> neue Version speichern.**

