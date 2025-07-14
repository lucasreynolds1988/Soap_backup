"""
Keeps only the latest 6 snapshots per agent or recovery folder.
Also provides emergency snapshot saving for system errors or bloat detection.
Used by rotor_fusion, spin_down, healer, and sentinel agents.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Allow running this module as a standalone script by adjusting sys.path
import sys
CURRENT_DIR = Path(__file__).resolve().parents[1]
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from core.codex_folder_creator import ROOT, SNAPSHOT_AGENTS, log_event

MAX_SNAPSHOTS = 6
SNAPSHOT_ROOT = ROOT / "snapshots"
OUTPUT_PATH = ROOT / "outputs" / "sop_output.txt"
LOGS_ROOT = ROOT / "logs"


def rotate_agent_snapshots() -> None:
    for agent in SNAPSHOT_AGENTS:
        folder = SNAPSHOT_ROOT / agent
        files = sorted(folder.glob("*.json"), key=os.path.getmtime)
        while len(files) > MAX_SNAPSHOTS:
            log_event(f"[ROTATE] Deleting old snapshot: {files[0].name}")
            files[0].unlink()
            files = files[1:]


def save_agent_snapshot(reason: str = "manual") -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = SNAPSHOT_ROOT / "recovery_logs" / f"{timestamp}_{reason}"
    folder.mkdir(parents=True, exist_ok=True)

    # Copy recent logs
    for log_file in LOGS_ROOT.rglob("*.log"):
        try:
            shutil.copy(log_file, folder / log_file.name)
        except Exception as e:
            log_event(f"[WARN] Couldn't copy {log_file.name}: {e}")

    # Copy current SOP output if exists
    if OUTPUT_PATH.exists():
        shutil.copy(OUTPUT_PATH, folder / "sop_output.txt")

    log_event(f"[SNAPSHOT] Saved state to {folder}")


if __name__ == "__main__":
    rotate_agent_snapshots()
    print("[✅] Snapshot rotation complete.")
