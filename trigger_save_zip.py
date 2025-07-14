#!/usr/bin/env python3
"""Save zip trigger wrapper."""
import subprocess
from pathlib import Path
import time

LOG_PATH = Path.home() / "Soap/logs/trigger_save_zip.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("📦 [+SAVE-ZIP+] Zipping Soap directory locally...")
    log("Save-zip trigger fired")
    subprocess.run("python3 ~/Soap/save_zip.py", shell=True)
    log("Save-zip complete")


if __name__ == "__main__":
    main()
