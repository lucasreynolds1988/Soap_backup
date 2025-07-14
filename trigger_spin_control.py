#!/usr/bin/env python3
"""Spin-control trigger wrapper."""
import subprocess
from pathlib import Path
import time

LOG_PATH = Path.home() / "Soap/logs/trigger_spin_control.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("⚙️ [+SPIN-CONTROL+] Checking critical directories...")
    log("Spin-control trigger fired")
    subprocess.run("python3 ~/Soap/spin_control.py", shell=True)
    log("Spin-control complete")


if __name__ == "__main__":
    main()
