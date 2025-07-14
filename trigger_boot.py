#!/usr/bin/env python3
"""Boot trigger wrapper."""
import subprocess
from pathlib import Path
import time

LOG_PATH = Path.home() / "Soap/logs/trigger_boot.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main() -> None:
    print("🚀 [+BOOT+] Starting full start sequence...")
    log("BOOT trigger fired")
    root = Path.home() / "Soap/triggers"
    for trig in ["+ATTENTION+", "+CODE-RED+", "+SPIN-UP+"]:
        subprocess.run(["bash", str(root / trig)], check=False)
    log("BOOT sequence completed")


if __name__ == "__main__":
    main()
