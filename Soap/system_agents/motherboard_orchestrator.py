"""
Master orchestrator that runs all rotor-timed agents in sequence every 4 seconds.
It handles heartbeat writing, agent execution, and monitoring coordination.
"""

import time
from datetime import datetime
import sys
from pathlib import Path

# Allow running as a standalone script
CURRENT_DIR = Path(__file__).resolve().parents[1]
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from core.codex_folder_creator import ROOT, log_event
from core.snapshot_rotator import rotate_agent_snapshots
from agents.watson_phase import run_watson
from agents.father_phase import run_father
from agents.arbiter_phase import run_arbiter
from agents.soap_phase import run_soap

HEARTBEAT_PATH = ROOT / "logs" / "heartbeat" / "motherboard.log"


def pulse() -> None:
    HEARTBEAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HEARTBEAT_PATH, "a") as hb:
        hb.write(f"[{datetime.now()}] heartbeat\n")


def orchestrate_cycle() -> None:
    log_event("[MOTHERBOARD] Starting SOP generation cycle.")

    print(run_watson())
    time.sleep(4)
    rotate_agent_snapshots()

    print(run_father())
    time.sleep(4)
    rotate_agent_snapshots()

    print(run_arbiter())
    time.sleep(4)
    rotate_agent_snapshots()

    print(run_soap())
    time.sleep(4)
    rotate_agent_snapshots()

    pulse()
    log_event("[MOTHERBOARD] Cycle complete.")


def run_loop() -> None:
    while True:
        orchestrate_cycle()


if __name__ == "__main__":
    run_loop()
