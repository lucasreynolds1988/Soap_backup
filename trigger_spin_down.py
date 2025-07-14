# ~/Soap/trigger_spin_down.py

import subprocess
from pathlib import Path
import time

LOG_PATH = Path.home() / "Soap/logs/trigger_spin_down.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


def main():
    print(
        "🛑 [+SPIN-DOWN+] Finalizing logs, syncing storage, powering down "
        "rotors..."
    )
    log("Spin-Down initiated from trigger.")
    subprocess.run("python3 ~/Soap/spin_down.py", shell=True)
    print("💤 [SPIN-DOWN] Rotor engine is offline.")
    log("Spin-Down complete.")


if __name__ == "__main__":
    main()
