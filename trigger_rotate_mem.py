#!/usr/bin/env python3
"""Rotate memory trigger wrapper."""
import subprocess
from pathlib import Path
import time

LOG_PATH = Path.home() / "Soap/logs/trigger_rotate_mem.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("🔁 [+ROTATE-MEM+] Playing zip logs...")
    log("Rotate-mem trigger fired")
    subprocess.run("python3 ~/Soap/rotate_mem.py", shell=True)
    log("Rotate-mem complete")


if __name__ == "__main__":
    main()
