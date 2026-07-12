"""log_viz (Diagramm-Knoten ``log_viz``) — Python-Baseline: FastAPI.

Macht die JSONL-Sitzungslogs aus ``~/.boukensha/logs/<session_id>/*.jsonl``
menschenlesbar. Ersetzt die im Diagramm gezeigte Sinatra-App (Ruby) durch eine
**neue** Python-Variante (kein Ruby-Ersatz im Bestand).

Start (nach ``pip install '.[logviz]'`` bzw. ``uv sync --extra logviz``)::

    uvicorn log_viz.server:app --reload
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "log_viz benötigt FastAPI/uvicorn — installieren mit: uv sync --extra logviz"
    ) from e

import os

app = FastAPI(title="Boukensha log_viz")


def _logs_root() -> Path:
    return Path(os.environ.get("BOUKENSHA_DIR", str(Path.home() / ".boukensha"))) / "logs"


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Listet die verfügbaren Sitzungen auf."""
    root = _logs_root()
    if not root.exists():
        return "<h1>Boukensha log_viz</h1><p>Noch keine Logs.</p>"
    zeilen = [f'<li><a href="/session/{p.name}">{p.name}</a></li>' for p in sorted(root.iterdir())]
    return "<h1>Sitzungen</h1><ul>" + "".join(zeilen) + "</ul>"


@app.get("/session/{session_id}", response_class=HTMLResponse)
def session(session_id: str) -> str:
    """Zeigt die Ereignisse einer Sitzung menschenlesbar."""
    sdir = _logs_root() / session_id
    if not sdir.exists():
        return f"<p>Unbekannte Sitzung: {session_id}</p>"
    rows = []
    for jsonl in sorted(sdir.glob("*.jsonl")):
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            rest = {k: v for k, v in e.items() if k not in {"ts", "session", "typ"}}
            rows.append(
                f"<tr><td>{e.get('ts','')}</td><td><b>{e.get('typ','')}</b></td>"
                f"<td><pre>{json.dumps(rest, ensure_ascii=False)}</pre></td></tr>"
            )
    return (
        f"<h1>Sitzung {session_id}</h1>"
        "<table border=1 cellpadding=4><tr><th>Zeit</th><th>Typ</th><th>Daten</th></tr>"
        + "".join(rows)
        + "</table>"
    )
