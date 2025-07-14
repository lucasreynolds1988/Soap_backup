#!/usr/bin/env python3
"""Code-Red trigger wrapper."""
import subprocess
from pathlib import Path
import time

LOG_PATH = Path.home() / "Soap/logs/trigger_code_red.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("🔥 [+CODE-RED+] Uploading and purging bloat...")
    log("Code-Red trigger fired")
    subprocess.run("python3 ~/Soap/code_red.py", shell=True)
    log("Code-Red complete")


if __name__ == "__main__":
    main()
