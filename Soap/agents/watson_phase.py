#!/usr/bin/env python3
"""
watson_phase.py: Formatting engine for ATI SOP system.
Reads queued raw SOP JSON tasks, structures content per Watson style, and updates status.
"""
import json
import logging
from pathlib import Path

# Configuration
HOME_DIR = Path.home()
QUEUE_DIR = HOME_DIR / "Soap" / "agent_queue"
LOG_DIR = HOME_DIR / "Soap" / "data" / "logs"
LOG_FILE = LOG_DIR / "watson_phase.log"

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


def structure_sop(raw_text: str) -> dict:
    """Parse raw text into a structured SOP format."""
    # Basic example; replace with improved parsing logic as needed
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    return {
        "title": lines[0] if lines else "Untitled SOP",
        "purpose": "Describe the purpose.",
        "scope": "Define the scope here.",
        "tools": [],
        "materials": [],
        "safety": [],
        "procedure": lines[1:],
        "watson_backup": None  # will be set after deep copy
    }


def run_watson():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    for task in tasks:
        try:
            data = json.loads(task.read_text())
            if data.get("status") != "queued":
                continue
            log(f"🧠 Watson processing: {task.name}")
            structured = structure_sop(data.get("raw_text", ""))
            # Deep copy backup
            structured["watson_backup"] = json.loads(json.dumps(structured))
            data.update(structured)
            data["status"] = "watson_complete"
            task.write_text(json.dumps(data, indent=2))
            log(f"✅ Watson complete: {task.name}")
        except Exception as e:
            log(f"❌ Watson error on {task.name}: {e}", level=logging.ERROR)


if __name__ == "__main__":
    run_watson()
