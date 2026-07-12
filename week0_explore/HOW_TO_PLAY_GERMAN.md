## Den CircleMUD starten

Wir können den CircleMUD auf Port `4000` mit einem einfachen `docker compose up` starten:

```sh
cd week0_explore/infrastructure
docker compose up --build
```

Ein paar weitere nützliche Docker-Befehle, die man kennen sollte:
```sh
docker compose up --build -d # im Hintergrund ausführen
docker compose logs -f # den Logs folgen
docker compose down # herunterfahren
docker compose down -v # herunterfahren und das persistente virtuelle Volume löschen
docker volume rm infrastructure_circlemud-lib # das Volume manuell löschen (der Container muss vorher gestoppt sein)
```

*Die Docker-VSC-Extension bietet Click-Ops zum Verwalten laufender Container — die Installation ist sehr zu empfehlen.*

## Verbindung zum CircleMUD herstellen

Du kannst dich mit telnet oder nc zum MUD verbinden:

```sh
telnet localhost 4000
nc localhost 4000
```

## Admin-Charakter erstellen

Der erste Charakter, den du erstellst, wird dein Admin-Charakter.
Betrachte ihn wie dein AWS-Root-Konto. Du sollst das Spiel nicht mit diesem Charakter spielen.

Der Admin-Charakter hat die folgenden Eigenschaften:
- Level 34
- Bekannt als der Implementor
- Höchste Administrator-Rolle

Ich würde empfehlen, dies auf `admin` / `password` zu setzen.

Nachdem du deinen Admin-Charakter erstellt hast:

Bestätige mit `score`, dass du Admin bist:

```txt
> score
You are 17 years old.
  It's your birthday today.
You have 500(500) hit, 100(100) mana and 82(82) movement points.
Your armor class is 40/10, and your alignment is 0.
You have scored 7000000 exp, and have 0 gold coins.
You have been playing for 0 days and 0 hours.
This ranks you as Admin the Implementor (level 34).
You are standing.
```

Bestätige mit `wizhelp`, dass du die Admin-Befehle sehen kannst.

Probiere ein paar nicht-destruktive Admin-Befehle aus: `where` und `users`:

```txt
> where
Players
-------
Admin - [1204] The Immortal Board Room
```

```txt
> users
Num Class   Name         State          Idl Login@   Site
--- ------- ------------ -------------- --- -------- ------------------------
  1 [34 Mu] Admin        Playing            16:33:48 [172.19.0.1]

1 visible sockets connected.
```

Verlasse das MUD, damit wir mit dem Erstellen unseres Hauptcharakters fortfahren können.

## Hauptcharakter erstellen

Erstelle einen neuen Charakter, empfohlen: `dummy` und `helloworld`.
Wähle eine beliebige Klasse und ein Geschlecht.

## Grundlegende Befehle kennenlernen

```sh
help time
help score
help info
help weather
help where
help who
help look
help exaxime
help exits
help consider
```

## Über deinen Charakter lernen

```sh
help quests
help inventory
help equipment
help experience # lerne, wie Erfahrung funktioniert
help ac # lerne über die Rüstungsklasse (armour class)
help warrior # lerne über deine Klasse
help practice # lerne über das Üben einer Fertigkeit oder eines Zaubers
help spells # lerne über Zauber
```

## Erste Schritte

> Ich würde Stift und Papier nehmen und aufzeichnen, wo du dich befindest.

- The Temple of Midgaard – prüfe den Kontostand deines Bankkontos
- The Reading Room – hinterlasse eine Nachricht am großen Anschlagbrett
- By The Temple of Altar – untersuche den Altar (`examine altar`)
- Temple Square – trinke am Temple Square
- Finde deine Gilde:
  - Clerics Guild: westlich vom Temple Square
  - Thieves Guild: südlich von The Dark Alley
  - Warrior Guild: östlich der Main Street auf der Südseite
  - Mages Guild: West Main Street auf der Südseite
- Übe in deiner Gilde, z. B. `practice kick`
- Suche nach schwachen Gegnern, die du besiegen kannst, z. B. `consider`, um ihre Stärke zu ermitteln
  - Sieh dich in Midgaard um, ohne die Stadt zu verlassen.
  - Sammle die Leiche ein: `get all corpse`
- Prüfe deine Trefferpunkte (HP) mit `score` und heile dich durch `rest` oder `sleep`; prüfe regelmäßig, bis du vollständig geheilt bist.

### Was, wenn ich mich verlaufe?

Wenn du das Spiel verlässt und wieder betrittst, startest du erneut bei By The Temple of Altar. Du musst `offer` und `rent` an der Rezeption eines Inns benutzen, um dich nach dem Verlassen und erneuten Betreten des Spiels an deinem Ort zu persistieren.

- [World Data](https://github.com/Yuffster/CircleMUD/tree/master/lib/world)