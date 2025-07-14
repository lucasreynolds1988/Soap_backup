#!/usr/bin/env python3
"""
mother_phase.py: Safety conscience for ATI SOP system.
Appends PPE defaults and hazard-specific warnings to SOPs.
"""
import json
import logging
from pathlib import Path

# Configuration
HOME_DIR = Path.home()
QUEUE_DIR = HOME_DIR / "Soap" / "agent_queue"
LOG_DIR = HOME_DIR / "Soap" / "data" / "logs"
LOG_FILE = LOG_DIR / "mother_phase.log"
RULES_FILE = HOME_DIR / "Soap" / "overlay" / "regulatory_rules.json"

# Default safety rules
PPE_DEFAULTS = [
    "Wear safety glasses.",
    "Use mechanic gloves.",
    "Ensure work area is clean and dry."
]
# Keyword-based hazard flags
HAZARD_FLAGS = [
    (
        "brake",
        "⚠️ Brake dust may contain asbestos. Avoid blowing or dry brushing.",
    ),
    ("jack", "⚠️ Always use jack stands. Never rely solely on a jack."),
    ("grease", "⚠️ Use nitrile gloves to avoid chemical exposure."),
    (
        "cotter pin",
        "⚠️ Watch for sharp edges when removing retaining hardware.",
    ),
]

# Minimal regulatory rules per industry
DEFAULT_REG_RULES = {
    "General": [
        {"body": "OSHA", "rule": "29 CFR 1910"},
        {"body": "EPA", "rule": "RCRA"},
    ],
    "Aviation": [
        {"body": "FAA", "rule": "14 CFR Part 43"},
    ],
    "Medical": [
        {"body": "FDA", "rule": "21 CFR Part 820"},
        {"body": "CDC", "rule": "Disinfection Guidelines"},
    ],
}

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


def load_rules() -> dict:
    """Load regulatory rules from JSON file or use defaults."""
    if RULES_FILE.is_file():
        try:
            return json.loads(RULES_FILE.read_text())
        except Exception as exc:
            log(f"Failed to load {RULES_FILE}: {exc}", level=logging.WARNING)
    return DEFAULT_REG_RULES


def apply_safety(sop: dict) -> list:
    """Append default PPE and hazard warnings to SOP data."""
    added = []
    sop.setdefault("safety", [])
    # Add PPE defaults
    for rule in PPE_DEFAULTS:
        if rule not in sop["safety"]:
            sop["safety"].append(rule)
            added.append(rule)
    # Add hazard-specific flags
    for step in sop.get("procedure", []):
        for keyword, warning in HAZARD_FLAGS:
            if keyword in step.lower() and warning not in sop["safety"]:
                sop["safety"].append(warning)
                added.append(warning)
    return added


def apply_regulatory_rules(sop: dict, rules: dict) -> list:
    """Ensure industry regulatory references are present."""
    added = []
    industry = sop.get("industry", "General")
    targets = rules.get(industry, rules.get("General", []))
    sop.setdefault("regulatory_refs", [])
    for item in targets:
        ref = f"{item['body']}: {item['rule']}"
        if ref not in sop["regulatory_refs"]:
            sop["regulatory_refs"].append(ref)
            added.append(ref)
        if ref not in sop.get("safety", []):
            sop.setdefault("safety", []).append(ref)
            added.append(ref)
    if not targets:
        log(f"No regulatory rules found for {industry}", level=logging.WARNING)
    return added


def run_mother():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    rules = load_rules()
    for task in tasks:
        try:
            data = json.loads(task.read_text())
            if data.get("status") != "father_complete":
                continue
            log(f"🛡️ Mother processing: {task.name}")
            # Backup before changes
            data["mother_backup"] = json.loads(json.dumps(data))
            new_rules = apply_safety(data)
            added_refs = apply_regulatory_rules(data, rules)
            if new_rules or added_refs:
                log(
                    f"✅ Added safety info for {task.name}: {new_rules + added_refs}"
                )
            else:
                log(f"🧼 No new safety rules needed for {task.name}")
            data["status"] = "mother_complete"
            task.write_text(json.dumps(data, indent=2))
        except Exception as e:
            log(f"❌ Mother error on {task.name}: {e}", level=logging.ERROR)


if __name__ == "__main__":
    run_mother()
