cd claudeCodeCamp/week1_baseline

uv run python -m unittest discover -s python/07_the_run_dsl/tests -v

mkdir -p python/08_the_repl_loop
cp -R python/07_the_run_dsl/boukensha python/08_the_repl_loop/
cp -R python/07_the_run_dsl/prompts python/08_the_repl_loop/
cp python/07_the_run_dsl/pyproject.toml python/08_the_repl_loop/pyproject.toml
cp python/07_the_run_dsl/boukensha/logger.py python/08_the_repl_loop/boukensha/logger.py

uv run python -m unittest discover -s python/08_the_repl_loop/tests -v

from __future__ import annotations

from pathlib import Path

from .config import Config


def run_step8(config_dir: Path | None = None) -> int:
    import boukensha

    config = Config(directory=config_dir)

    print("=== BOUKENSHA Step 8: The REPL Loop ===")
    print()
    print(f"Config: {config}")
    print()

    base_dir = Path(__file__).resolve().parents[1]

    def setup(t) -> None:
        @t.tool(
            "read_file",
            description="Read the contents of a file from disk",
            parameters={"path": {"type": "string", "description": "The file path to read"}},
        )
        def read_file(path: str) -> str:
            return Path(base_dir / path).read_text(encoding="utf-8")

        @t.tool(
            "list_directory",
            description="List the files in a directory",
            parameters={"path": {"type": "string", "description": "The directory path to list"}},
        )
        def list_directory(path: str) -> str:
            return ", ".join(
                p.name for p in (base_dir / path).iterdir() if not p.name.startswith(".")
            )

    return boukensha.repl(setup=setup, config_dir=config_dir)


def main() -> None:
    raise SystemExit(run_step8())

### Tests:

week1_baseline % uv run python -m unittest discover -s python/07_the_run_dsl/tests -v
test_turn_and_subscribe_emit_original_event (test_logger_subscribe.LoggerSubscribeTests.test_turn_and_subscribe_emit_original_event) ... ERROR
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/unittest/case.py:650: ResourceWarning: unclosed file <_io.TextIOWrapper name='/var/folders/cr/fz0nsdvs6tl0pt_7zj1ccbg80000gn/T/tmp450cbl6u/sess-1/events.jsonl' mode='a' encoding='utf-8'>
with outcome.testPartExecutor(self):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
test_run_wires_setup_and_writes_snapshot_log (test_run_api.RunApiTests.test_run_wires_setup_and_writes_snapshot_log) ... ok
test_run_step7_with_mocked_dsl_run (test_run_step7.RunStep7Tests.test_run_step7_with_mocked_dsl_run) ... ok

======================================================================
ERROR: test_turn_and_subscribe_emit_original_event (test_logger_subscribe.LoggerSubscribeTests.test_turn_and_subscribe_emit_original_event)
----------------------------------------------------------------------
Traceback (most recent call last):
File "/Users/Andre.Wolff/Documents/005___data/git/001_podman_runtime/claudeCodeCamp/week1_baseline/python/07_the_run_dsl/tests/test_logger_subscribe.py", line 20, in test_turn_and_subscribe_emit_original_event
logger.subscribe(events.append)
^^^^^^^^^^^^^^^^
AttributeError: 'Logger' object has no attribute 'subscribe'

----------------------------------------------------------------------
Ran 3 tests in 0.009s

FAILED (errors=1)

-------

test_turn_and_subscribe_emit_original_event ... ok
test_run_wires_setup_and_writes_snapshot_log ... ok
test_run_step7_with_mocked_dsl_run ... ok
