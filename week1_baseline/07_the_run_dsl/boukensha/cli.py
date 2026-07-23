from __future__ import annotations

from pathlib import Path

from .config import Config


def run_step7(config_dir: Path | None = None) -> int:
    import boukensha

    config = Config(directory=config_dir)

    print("=== BOUKENSHA Step 7: The Boukensha.run DSL ===")
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

    result = boukensha.run(
        task="Read the README.md file and summarise what this MUD player assistant framework can do.",
        setup=setup,
        config_dir=config_dir,
    )

    print("=== FINAL RESPONSE ===")
    print(result)
    return 0


def main() -> None:
    raise SystemExit(run_step7())

