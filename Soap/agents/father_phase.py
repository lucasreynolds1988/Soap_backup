#!/usr/bin/env python3
"""
father_phase.py: Composition engine for ATI SOP system.
Validates logical consistency of structured SOPs and marks issues.
"""
import json
import logging
from pathlib import Path

# Configuration
HOME_DIR = Path.home()
QUEUE_DIR = HOME_DIR / "Soap" / "agent_queue"
LOG_DIR = HOME_DIR / "Soap" / "data" / "logs"
LOG_FILE = LOG_DIR / "father_phase.log"

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


def validate_logic(sop: dict) -> list:
    """Check SOP steps for clear action verbs and required fields."""
    issues = []
    if not sop.get("tools"):
        issues.append("Missing tool list.")
    proc = sop.get("procedure", [])
    if not isinstance(proc, list) or not proc:
        issues.append("Procedure steps are missing or invalid.")
    else:
        actions = ["install", "remove", "check", "clean", "torque", "grease"]
        for idx, step in enumerate(proc, 1):
            if not any(verb in step.lower() for verb in actions):
                issues.append(f"Step {idx} may lack a clear action: '{step}'")
    return issues


def run_father():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    for task in tasks:
        try:
            data = json.loads(task.read_text())
            if data.get("status") != "watson_complete":
                continue
            log(f"🛠️ Father processing: {task.name}")
            # Backup before changes
            data["father_backup"] = json.loads(json.dumps(data))
            issues = validate_logic(data)
            if issues:
                data["logic_issues"] = issues
                data["status"] = "needs_human_review"
                log(f"⚠️ Logic issues in {task.name}: {issues}")
            else:
                data["status"] = "father_complete"
                log(f"✅ Logic validated for {task.name}")
            task.write_text(json.dumps(data, indent=2))
        except Exception as e:
            log(f"❌ Father error on {task.name}: {e}", level=logging.ERROR)


if __name__ == "__main__":
    run_father()
