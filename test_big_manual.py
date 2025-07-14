#!/usr/bin/env python3
"""End-to-end test with a large manual input."""
import json
from pathlib import Path

from agents.watson_phase import run_watson
from agents.father_phase import run_father
from agents.mother_phase import run_mother
from agents.arbiter_phase import run_arbiter
from agents.soap_phase import run_soap


def generate_manual() -> str:
    """Return a large text string ~10k words."""
    base = "Step: Inspect code for security risks."
    return " ".join([base] * 10000)


def main() -> None:
    home = Path.home()
    soap_dir = home / "Soap"
    queue_dir = soap_dir / "agent_queue"
    logs_dir = soap_dir / "data" / "logs"
    queue_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # clear old tasks
    for path in queue_dir.glob("*.json"):
        path.unlink()

    task = {
        "raw_text": generate_manual(),
        "status": "queued",
    }
    task_path = queue_dir / "big_manual.json"
    task_path.write_text(json.dumps(task, indent=2))

    run_watson()

    # inject minimal required fields
    data = json.loads(task_path.read_text())
    data["tools"] = ["security scanner"]
    data["materials"] = []
    data["industry"] = "General"
    data["procedure"] = ["Check code for security risks"]
    task_path.write_text(json.dumps(data, indent=2))

    run_father()
    run_mother()
    run_arbiter()
    run_soap()

    result = json.loads(task_path.read_text())
    print(json.dumps({"status": result.get("status")}, indent=2))
    if result.get("status") != "soap_complete":
        raise SystemExit("Big manual test failed")
    print("\u2714 big manual test passed")


if __name__ == "__main__":
    main()
