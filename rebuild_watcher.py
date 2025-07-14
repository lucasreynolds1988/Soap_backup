#!/usr/bin/env python3
"""Watch for .trigger.rebuild file and run restore."""
import time
from pathlib import Path
import subprocess

FLAG = Path.home() / "Soap/.trigger.rebuild"
TRIGGER = Path.home() / "Soap/restore_now.py"


def main() -> None:
    while True:
        if FLAG.exists():
            print("🔁 [.trigger.rebuild] Detected. Restoring...")
            FLAG.unlink(missing_ok=True)
            subprocess.run(["python3", str(TRIGGER)], check=False)
        time.sleep(5)


if __name__ == "__main__":
    main()
