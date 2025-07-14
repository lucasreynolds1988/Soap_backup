#!/usr/bin/env python3
"""Run all triggers in sequence for testing."""
import subprocess
from pathlib import Path

TRIGGERS = [
    "+ATTENTION+",
    "+CODE-RED+",
    "+FULL_SAVE_NOW+",
    "+SPIN-DOWN+",
    "+SPIN-UP+",
]


def main() -> None:
    root = Path.home() / "Soap/triggers"
    for trig in TRIGGERS:
        path = root / trig
        print(f"⚡ Running {trig} ...")
        subprocess.run(["bash", str(path)], check=False)


if __name__ == "__main__":
    main()
