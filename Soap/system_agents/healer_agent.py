"""
Triggers restoration process for failed agents or corrupted runtime.
Relies on fusion_restore_v2.py to pull from cloud backup.
"""

import subprocess
import sys
from pathlib import Path

# Allow running as a standalone script
CURRENT_DIR = Path(__file__).resolve().parents[1]
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from core.codex_folder_creator import log_event
from core.snapshot_rotator import save_agent_snapshot


def trigger_healing(agent_name: str) -> None:
    log_event(f"[HEALER] Triggered by agent: {agent_name}. Saving snapshot.")
    save_agent_snapshot(reason=f"healing_{agent_name}")

    try:
        subprocess.run(["python3", "fusion_restore_v2.py"], check=True)
        log_event("[HEALER] Restore process completed.")
    except subprocess.CalledProcessError as e:
        log_event(f"[HEALER] Restore failed: {e}")


if __name__ == "__main__":
    trigger_healing("manual")
