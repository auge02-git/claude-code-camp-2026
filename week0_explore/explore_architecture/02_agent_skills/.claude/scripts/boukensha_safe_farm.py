#!/usr/bin/env python3
"""Hilfsskript für den Boukensha-Safe-Farm-Plan.

Gibt vorbereitete, konservative Befehlsfolgen aus, die aus den dokumentierten
Erkenntnissen der Datei `erfahrung_durchlaeufe_v3.md` abgeleitet sind.

Standardmäßig druckt das Skript nur die Kommandos und automatisiert keinen
Live-Lauf. So bleibt die taktische Entscheidung beim Agenten oder Benutzer.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable

PLANS: dict[str, dict[str, object]] = {
    "start-check": {
        "description": "Standort und Zustand pruefen.",
        "commands": ["score", "look"],
    },
    "to-fountain-from-donation": {
        "description": "Sicherer Weg vom Donation Room zum Brunnen.",
        "commands": ["west", "south", "drink fountain"],
    },
    "to-fountain-from-market": {
        "description": "Sicherer Weg vom Market Square zum Brunnen.",
        "commands": ["north", "drink fountain"],
    },
    "to-farm-from-center": {
        "description": "Vom Zentrum Richtung Poor Alley / Farmgebiet.",
        "commands": ["south", "west", "look"],
    },
    "farm-cycle": {
        "description": "Ein einzelner konservativer Farm-Zyklus.",
        "commands": ["look", "kill fido", "get all corpse", "eat meat"],
    },
    "farm-cycle-with-score": {
        "description": "Farm-Zyklus mit zusaetzlicher Zustandspruefung.",
        "commands": ["look", "kill fido", "get all corpse", "eat meat", "score"],
    },
    "pendulum": {
        "description": "Kurzes Pendeln zwischen benachbarten Raeumen zum Respawn-Check.",
        "commands": ["east", "look", "west", "look"],
    },
    "danger-reset": {
        "description": "Sofortreaktion bei Risiko oder unklarem Output.",
        "commands": ["flee", "look"],
    },
    "safe-quit": {
        "description": "Fortschritt an sicherer Stelle beenden.",
        "commands": ["quit"],
    },
    "full-run-donation": {
        "description": "Kompletter konservativer Startlauf ab Donation Room.",
        "commands": [
            "score",
            "look",
            "west",
            "south",
            "drink fountain",
            "south",
            "west",
            "look",
            "kill fido",
            "get all corpse",
            "eat meat",
            "score",
        ],
    },
    "full-run-market": {
        "description": "Kompletter konservativer Startlauf ab Market Square.",
        "commands": [
            "score",
            "look",
            "north",
            "drink fountain",
            "south",
            "west",
            "look",
            "kill fido",
            "get all corpse",
            "eat meat",
            "score",
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="boukensha_safe_farm",
        description="Gibt sichere Boukensha-Farm-Kommandosequenzen aus.",
    )
    parser.add_argument("plan", nargs="?", help="Name des Plans")
    parser.add_argument(
        "--list",
        action="store_true",
        help="Verfuegbare Plaene mit Beschreibung anzeigen",
    )
    parser.add_argument(
        "--format",
        choices=("lines", "json", "bash"),
        default="lines",
        help="Ausgabeformat der Kommandos (Standard: lines)",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Plan mehrfach hintereinander ausgeben (Standard: 1)",
    )
    return parser.parse_args()


def repeated_commands(commands: Iterable[str], repeat: int) -> list[str]:
    result: list[str] = []
    for _ in range(repeat):
        result.extend(commands)
    return result


def print_plan_list() -> int:
    for name, meta in PLANS.items():
        print(f"{name}: {meta['description']}")
    return 0


def print_commands(commands: list[str], output_format: str) -> int:
    if output_format == "json":
        print(json.dumps(commands, ensure_ascii=False, indent=2))
        return 0

    if output_format == "bash":
        for command in commands:
            print(command)
        return 0

    for command in commands:
        print(command)
    return 0


def main() -> int:
    args = parse_args()

    if args.list:
        return print_plan_list()

    if not args.plan:
        print("Fehler: Bitte einen Plan angeben oder --list verwenden.", file=sys.stderr)
        return 2

    if args.plan not in PLANS:
        print(f"Fehler: Unbekannter Plan '{args.plan}'.", file=sys.stderr)
        print("Tipp: --list zeigt alle verfuegbaren Plaene.", file=sys.stderr)
        return 2

    if args.repeat < 1:
        print("Fehler: --repeat muss mindestens 1 sein.", file=sys.stderr)
        return 2

    plan = PLANS[args.plan]
    commands = repeated_commands(plan["commands"], args.repeat)
    return print_commands(commands, args.format)


if __name__ == "__main__":
    raise SystemExit(main())

