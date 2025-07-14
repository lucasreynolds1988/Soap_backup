#!/usr/bin/env python3
"""Spin-Up trigger wrapper."""
import subprocess
from pathlib import Path
import time

LOG_PATH = Path.home() / "Soap/logs/trigger_spin_up.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("🔄 [+SPIN-UP+] Restoring from cloud and relaunching rotors...")
    log("Spin-Up trigger fired")
    subprocess.run("python3 ~/Soap/spin_up.py", shell=True)
    log("Spin-Up complete")


if __name__ == "__main__":
    main()
