cd claudeCodeCamp/week1_baseline

uv run python -m unittest discover -s python/07_the_run_dsl/tests -v

mkdir -p python/08_the_repl_loop
cp -R python/07_the_run_dsl/boukensha python/08_the_repl_loop/
cp -R python/07_the_run_dsl/prompts python/08_the_repl_loop/
cp python/07_the_run_dsl/pyproject.toml python/08_the_repl_loop/pyproject.toml

uv run python -m unittest discover -s python/08_the_repl_loop/tests -v

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

class Logger:
    """Schreibt strukturierte JSONL-Events im log_viz-kompatiblen Format."""

    def __init__(
        self,
        *,
        session_id: str | None = None,
        dir: Path | None = None,
        log: Path | None = None,
        snapshot: dict[str, Any] | None = None,
    ) -> None:
        self.session_id = session_id or self._new_session_id()
        self.root_dir = dir or self._default_logs_dir()
        self.session_dir = self.root_dir / self.session_id
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self._subscribers = []

        self.path = log or (self.session_dir / "events.jsonl")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")

        event: dict[str, Any] = {}
        if snapshot is not None:
            event["snapshot"] = snapshot
        self._write("session_start", event)

    def close(self) -> None:
        if not self._fh.closed:
            self._fh.close()

    def subscribe(self, callback) -> None:
        self._subscribers.append(callback)

    def turn(self, n: int) -> None:
        self._write("turn", {"n": n})

    def iteration(self, n: int, max: int) -> None:  # noqa: A002
        self._write("iteration", {"n": n, "max": max})

    def prompt(self, messages: list[Any], tools: dict[str, Any]) -> None:
        self._write(
            "prompt",
            {
                "message_count": len(messages),
                "messages": [m.role for m in messages],
                "tool_count": len(tools),
                "tools": list(tools.keys()),
            },
        )

    # ... existing code ...

    def turn_end(self, *, reason: str, iterations: int, tokens: dict[str, Any]) -> None:
        self._write(
            "turn_end",
            {
                "reason": reason,
                "iterations": iterations,
                "tokens": tokens,
            },
        )

    def _write(self, typ: str, payload: dict[str, Any]) -> None:
        subscriber_event = {
            "typ": typ,
            **payload,
        }

        for callback in self._subscribers:
            callback(subscriber_event)

        event = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "session": self.session_id,
            **subscriber_event,
        }
        self._fh.write(json.dumps(event, ensure_ascii=False) + "\n")
        self._fh.flush()

    @staticmethod
    def _default_logs_dir() -> Path:
        root = Path(os.environ.get("BOUKENSHA_DIR", str(Path.home() / ".boukensha")))
        return root / "logs"
