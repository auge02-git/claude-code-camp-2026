from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

import boukensha_loader


def _make_step(base: Path, name: str) -> Path:
    base = base.resolve()
    step = base / name
    (step / "boukensha").mkdir(parents=True)
    (step / "boukensha" / "__init__.py").write_text("def repl(): pass\n")
    return step


class BoukenkshaLoaderResolveTests(unittest.TestCase):
    def setUp(self) -> None:
        self._orig_path = os.environ.pop("BOUKENSHA_PATH", None)
        self._orig_dir = os.environ.pop("BOUKENSHA_DIR", None)

    def tearDown(self) -> None:
        if self._orig_path is not None:
            os.environ["BOUKENSHA_PATH"] = self._orig_path
        else:
            os.environ.pop("BOUKENSHA_PATH", None)
        if self._orig_dir is not None:
            os.environ["BOUKENSHA_DIR"] = self._orig_dir
        else:
            os.environ.pop("BOUKENSHA_DIR", None)

    def test_no_config_returns_bundled_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(boukensha_loader, "rc_file", return_value=Path(tmp) / ".boukensharc"):
                result = boukensha_loader.resolve()
        self.assertEqual(result, boukensha_loader.BUNDLED_DIR)

    def test_boukensha_path_env_var_wins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            step = _make_step(Path(tmp), "env-step")
            os.environ["BOUKENSHA_PATH"] = str(step)
            with patch.object(boukensha_loader, "rc_file", return_value=Path(tmp) / ".boukensharc"):
                result = boukensha_loader.resolve()
        self.assertEqual(result, step)

    def test_rc_boukensha_path_is_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            step = _make_step(Path(tmp), "rc-step")
            rc = Path(tmp) / ".boukensharc"
            rc.write_text(f"boukensha_path: {step}\n")
            with patch.object(boukensha_loader, "rc_file", return_value=rc):
                result = boukensha_loader.resolve()
        self.assertEqual(result, step)

    def test_env_var_overrides_rc_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rc_step = _make_step(Path(tmp), "rc-step")
            env_step = _make_step(Path(tmp), "env-step")
            rc = Path(tmp) / ".boukensharc"
            rc.write_text(f"boukensha_path: {rc_step}\n")
            os.environ["BOUKENSHA_PATH"] = str(env_step)
            with patch.object(boukensha_loader, "rc_file", return_value=rc):
                result = boukensha_loader.resolve()
        self.assertEqual(result, env_step)

    def test_rc_boukensha_dir_sets_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_r = Path(tmp).resolve()
            rc = tmp_r / ".boukensharc"
            rc.write_text(f"boukensha_dir: {tmp_r}/myconfig\n")
            with patch.object(boukensha_loader, "rc_file", return_value=rc):
                boukensha_loader.resolve()
            self.assertEqual(os.environ.get("BOUKENSHA_DIR"), str(tmp_r / "myconfig"))
            os.environ.pop("BOUKENSHA_DIR", None)

    def test_boukensha_dir_env_not_overwritten_by_rc(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_r = Path(tmp).resolve()
            os.environ["BOUKENSHA_DIR"] = "/explicit/config"
            rc = tmp_r / ".boukensharc"
            rc.write_text(f"boukensha_dir: {tmp_r}/rc-config\n")
            with patch.object(boukensha_loader, "rc_file", return_value=rc):
                boukensha_loader.resolve()
        self.assertEqual(os.environ["BOUKENSHA_DIR"], "/explicit/config")

    def test_legacy_single_path_string_format(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            step = _make_step(Path(tmp), "legacy-step")
            rc = Path(tmp) / ".boukensharc"
            rc.write_text(f"{step}\n")
            with patch.object(boukensha_loader, "rc_file", return_value=rc):
                result = boukensha_loader.resolve()
        self.assertEqual(result, step)

    def test_missing_boukensha_init_aborts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad_step = Path(tmp) / "no-init"
            bad_step.mkdir()
            os.environ["BOUKENSHA_PATH"] = str(bad_step)
            with patch.object(boukensha_loader, "rc_file", return_value=Path(tmp) / ".boukensharc"):
                with self.assertRaises(SystemExit):
                    boukensha_loader.resolve()


class BoukenkshaLoaderReplTests(unittest.TestCase):
    def setUp(self) -> None:
        self._orig_path = os.environ.pop("BOUKENSHA_PATH", None)

    def tearDown(self) -> None:
        if self._orig_path is not None:
            os.environ["BOUKENSHA_PATH"] = self._orig_path
        else:
            os.environ.pop("BOUKENSHA_PATH", None)

    def test_load_and_start_repl_calls_repl(self) -> None:
        repl_called = []
        with tempfile.TemporaryDirectory() as tmp:
            step = _make_step(Path(tmp), "repl-step")
            (step / "boukensha" / "__init__.py").write_text(
                "def repl(): _repl_called.append(True)\n_repl_called = []\n"
            )
            os.environ["BOUKENSHA_PATH"] = str(step)
            with patch.object(boukensha_loader, "rc_file", return_value=Path(tmp) / ".boukensharc"):
                with patch.object(boukensha_loader, "resolve", return_value=step):
                    import importlib, types
                    fake_mod = types.ModuleType("boukensha")
                    fake_mod.repl = lambda: repl_called.append(True)
                    with patch.dict(sys.modules, {"boukensha": fake_mod}):
                        boukensha_loader.load_and_start_repl()
        self.assertEqual(repl_called, [True])

    def test_load_and_start_repl_aborts_if_no_repl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            step = _make_step(Path(tmp), "no-repl-step")
            with patch.object(boukensha_loader, "resolve", return_value=step):
                import types
                fake_mod = types.ModuleType("boukensha")
                with patch.dict(sys.modules, {"boukensha": fake_mod}):
                    with self.assertRaises(SystemExit):
                        boukensha_loader.load_and_start_repl()


if __name__ == "__main__":
    unittest.main()
