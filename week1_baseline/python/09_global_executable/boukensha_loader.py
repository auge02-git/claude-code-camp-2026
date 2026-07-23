"""
BoukenshaLoader resolves which step folder and config directory to use,
then boots the REPL.

Resolution order for each setting:
  1. BOUKENSHA_PATH / BOUKENSHA_DIR environment variable
  2. boukensha_path / boukensha_dir in ~/.boukensharc
  3. Bundled default (this step's own boukensha package / ~/.boukensha)

Examples:
  boukensha                                             # bundled + ~/.boukensha
  BOUKENSHA_PATH=~/…/python/07_the_run_dsl boukensha   # load step 7
  BOUKENSHA_DIR=~/mybot/.boukensha boukensha            # custom config dir
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import yaml

BUNDLED_DIR = Path(__file__).resolve().parent


def rc_file() -> Path:
    return Path.home() / ".boukensharc"


def _load_rc() -> dict[str, Any]:
    rc = rc_file()
    if not rc.exists():
        return {}
    try:
        parsed = yaml.safe_load(rc.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        sys.exit(f"boukensha: invalid YAML in {rc}: {exc}")

    if parsed is None:
        return {}
    if isinstance(parsed, str):
        return {"boukensha_path": parsed}
    if isinstance(parsed, dict):
        return parsed
    sys.exit(f"boukensha: {rc} must contain a YAML mapping")


def _expand_rc_path(raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    return Path(raw).expanduser().resolve()


def resolve() -> Path:
    """Return the step directory to load boukensha from."""
    rc = _load_rc()

    rc_config_dir = _expand_rc_path(rc.get("boukensha_dir"))
    if rc_config_dir and "BOUKENSHA_DIR" not in os.environ:
        os.environ["BOUKENSHA_DIR"] = str(rc_config_dir)

    source = os.environ.get("BOUKENSHA_PATH") or _expand_rc_path(rc.get("boukensha_path"))
    if source is None:
        return BUNDLED_DIR

    step_dir = Path(source).expanduser().resolve()
    candidate = step_dir / "boukensha" / "__init__.py"
    if candidate.exists():
        return step_dir

    sys.exit(
        f"boukensha: no boukensha/__init__.py found at:\n"
        f"       {step_dir}\n"
        f"       Check BOUKENSHA_PATH or {rc_file()}."
    )


def load_and_start_repl() -> None:
    step_dir = resolve()

    if os.environ.get("BOUKENSHA_DEBUG"):
        print(f"[boukensha] loading from: {step_dir}", file=sys.stderr)

    if str(step_dir) not in sys.path:
        sys.path.insert(0, str(step_dir))

    import importlib
    boukensha = importlib.import_module("boukensha")

    if not callable(getattr(boukensha, "repl", None)):
        sys.exit(
            f"boukensha: the step at {step_dir}\n"
            f"       does not support the interactive REPL (added in step 8).\n"
            f"       Point BOUKENSHA_PATH at step 8 or later."
        )

    boukensha.repl()
