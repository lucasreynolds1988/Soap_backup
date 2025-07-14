"""
Monitors heartbeat logs of all agents. If any agent fails to update its
heartbeat log for more than 12 seconds, triggers healer_agent to restore.
"""

import os
import time
from datetime import datetime
from pathlib import Path
import sys

# Allow running as standalone script
CURRENT_DIR = Path(__file__).resolve().parents[1]
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from core.codex_folder_creator import ROOT, log_event
from system_agents.healer_agent import trigger_healing

HEARTBEAT_DIR = ROOT / "logs" / "heartbeat"
AGENTS = ["watson", "father", "arbiter", "soap", "scheduler", "motherboard"]
MAX_INACTIVE_SECONDS = 12


def check_heartbeats() -> None:
    now = datetime.now().timestamp()
    for agent in AGENTS:
        hb_path = HEARTBEAT_DIR / f"{agent}.log"
        if not hb_path.exists():
            log_event(f"[WATCHER] Missing heartbeat: {agent}")
            continue
        last_modified = os.path.getmtime(hb_path)
        if now - last_modified > MAX_INACTIVE_SECONDS:
            log_event(f"[WATCHER] Detected stall in {agent}, triggering healing.")
            trigger_healing(agent)


def run_watcher_loop() -> None:
    while True:
        check_heartbeats()
        time.sleep(4)


if __name__ == "__main__":
    run_watcher_loop()
