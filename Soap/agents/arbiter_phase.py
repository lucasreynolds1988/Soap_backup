#!/usr/bin/env python3
"""
arbiter_phase.py: Conflict resolution and orchestration agent for ATI SOP system.
Resolves logical or safety conflicts and finalizes SOP status.
"""
import json
import logging
from pathlib import Path

# Configuration
HOME_DIR = Path.home()
QUEUE_DIR = HOME_DIR / "Soap" / "agent_queue"
LOG_DIR = HOME_DIR / "Soap" / "data" / "logs"
LOG_FILE = LOG_DIR / "arbiter_phase.log"

# Setup logging
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger()

def log(message, level=logging.INFO):
    print(message)
    logger.log(level, message)


def resolve_conflicts(sop: dict) -> bool:
    """Check for logic_issues or missing safety and mark conflicts."""
    conflicts = []
    # Check for unresolved logic issues
    if sop.get("logic_issues"):
        conflicts.extend(sop["logic_issues"])
    # Check safety completeness
    if not sop.get("safety"):
        conflicts.append("Missing safety procedures.")

    # Mark conflict flag in SOP data
    if conflicts:
        sop["conflict_fields"] = conflicts
        return False
    return True


def run_arbiter():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    for task in tasks:
        try:
            data = json.loads(task.read_text())
            status = data.get("status")
            if status not in {"father_complete", "mother_complete", "needs_human_review"}:
                continue
            log(f"⚖️ Arbiter processing: {task.name}")
            # Backup before changes
            data["arbiter_backup"] = json.loads(json.dumps(data))
            if resolve_conflicts(data):
                data["status"] = "arbiter_complete"
                log(f"✅ Arbiter: No conflicts for {task.name}")
            else:
                data["status"] = "arbiter_conflict"
                log(f"⚠️ Arbiter: Conflicts found in {task.name}: {data.get('conflict_fields')}")
            task.write_text(json.dumps(data, indent=2))
        except Exception as e:
            log(f"❌ Arbiter error on {task.name}: {e}", level=logging.ERROR)


if __name__ == "__main__":
    run_arbiter()
