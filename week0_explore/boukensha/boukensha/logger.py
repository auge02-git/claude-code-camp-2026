"""Strukturiertes JSONL-Logging (Diagramm-Knoten ``logger.rb``).

Schreibt je Ereignis eine JSON-Zeile nach
``$BOUKENSHA_DIR/logs/<session_id>/<datum>.jsonl``. Diese Logs speisen später
``log_viz`` (menschenlesbare Darstellung) und dienen als nachlaufbarer Verlauf
(analog zum MUD-Session-Log unter ``week0_explore/logs/``).
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import boukensha_dir


class SessionLogger:
    """Ein Logger pro Agenten-Sitzung."""

    def __init__(self, session_id: str | None = None, home: Path | None = None) -> None:
        self.session_id = session_id or uuid.uuid4().hex[:12]
        home = home or boukensha_dir()
        self.dir = home / "logs" / self.session_id
        self.dir.mkdir(parents=True, exist_ok=True)
        datum = datetime.now().strftime("%Y-%m-%d")
        self.path = self.dir / f"{datum}.jsonl"

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
