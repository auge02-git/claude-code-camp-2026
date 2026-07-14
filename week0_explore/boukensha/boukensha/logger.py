"""Strukturiertes JSONL-Logging (Diagramm-Knoten ``logger.rb``).

Schreibt je Ereignis eine JSON-Zeile nach
``$BOUKENSHA_DIR/logs/<session_id>/<datum>.jsonl``. Diese Logs speisen später
``log_viz`` (menschenlesbare Darstellung) und dienen als nachlaufbarer Verlauf
(analog zum MUD-Session-Log unter ``week0_explore/logs/``).
"""

from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import boukensha_dir

_WEEK0_LOGS_DIR = Path(__file__).resolve().parents[2] / "logs"
_MOVE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|")
_PROMPT_RE = re.compile(r"^\d+H\s+\d+M\s+\d+V")


def latest_mud_session_log() -> Path | None:
    """Liefert die zuletzt geaenderte ``mud-session-*.log`` Datei aus ``week0_explore/logs``."""
    if not _WEEK0_LOGS_DIR.exists():
        return None
    kandidaten = sorted(
        _WEEK0_LOGS_DIR.glob("mud-session-*.log"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return kandidaten[0] if kandidaten else None


class SessionLogger:
    """Ein Logger pro Agenten-Sitzung."""

    def __init__(self, session_id: str | None = None, home: Path | None = None) -> None:
        self.session_id = session_id or uuid.uuid4().hex[:12]
        home = home or boukensha_dir()
        self.dir = home / "logs" / self.session_id
        self.dir.mkdir(parents=True, exist_ok=True)
        datum = datetime.now().strftime("%Y-%m-%d")
        self.path = self.dir / f"{datum}.jsonl"
        self.move_path = _WEEK0_LOGS_DIR / f"mud-session-{datum}.log"
        self._move_count = self._read_existing_move_count()

    def log(self, typ: str, **daten) -> None:
        """Schreibt ein Ereignis als eine JSON-Zeile.

        ``typ`` ist z. B. "observe", "action", "tool", "reflect", "output".
        """
        eintrag = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "session": self.session_id,
            "typ": typ,
            **daten,
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(eintrag, ensure_ascii=False) + "\n")

    def log_move(self, direction: str, output: str) -> None:
        """Haengt eine Bewegung als Tabellenzeile an das markdown Session-Log an."""
        self._ensure_move_log_header()
        self._move_count += 1
        ts = datetime.now().strftime("%H:%M:%S")
        raum = self._extract_room(output)
        ergebnis = self._short_result(output)
        zeile = (
            f"| {self._move_count} | {ts} | `{self._escape(direction)}` | "
            f"{self._escape(raum)} | {self._escape(ergebnis)} |\n"
        )
        with self.move_path.open("a", encoding="utf-8") as fh:
            fh.write(zeile)

    def _ensure_move_log_header(self) -> None:
        self.move_path.parent.mkdir(parents=True, exist_ok=True)
        if self.move_path.exists():
            return
        datum = datetime.now().strftime("%Y-%m-%d")
        inhalt = (
            "# MUD-Session-Log — Midgaard (tbaMUD)\n\n"
            f"- **Datum:** {datum}\n"
            "- **Quelle:** Boukensha Auto-Move Logger\n"
            "- **Hinweis:** Dieses Log erfasst automatisch Bewegungen (`move`).\n\n"
            "---\n\n"
            "## Bewegungen (automatisch)\n\n"
            "| # | Zeit | Kommando | Zielraum | Ergebnis |\n"
            "|---|------|----------|----------|----------|\n"
        )
        self.move_path.write_text(inhalt, encoding="utf-8")

    def _read_existing_move_count(self) -> int:
        if not self.move_path.exists():
            return 0
        last = 0
        with self.move_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                match = _MOVE_ROW_RE.match(line.strip())
                if match:
                    last = max(last, int(match.group(1)))
        return last

    @staticmethod
    def _extract_room(output: str) -> str:
        for line in output.splitlines():
            s = line.strip()
            if not s:
                continue
            if _PROMPT_RE.match(s):
                continue
            if s.lower().startswith("obvious exits"):
                continue
            if s.startswith("[") and "Exits" in s:
                continue
            return s
        return "(unbekannt)"

    @staticmethod
    def _short_result(output: str) -> str:
        text = output.strip().replace("\n", " / ")
        return text[:140] + ("..." if len(text) > 140 else "")

    @staticmethod
    def _escape(text: str) -> str:
        return text.replace("|", "\\|")

