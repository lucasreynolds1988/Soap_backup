#!/usr/bin/env python3
"""Spin-reset trigger wrapper."""
import subprocess
from pathlib import Path
import time

LOG_PATH = Path.home() / "Soap/logs/trigger_spin_reset.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("♻️ [+SPIN-RESET+] Purging temp files and caches...")
    log("Spin-reset trigger fired")
    subprocess.run("python3 ~/Soap/spin_reset.py", shell=True)
    log("Spin-reset complete")


if __name__ == "__main__":
    main()
