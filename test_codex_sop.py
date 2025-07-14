#!/usr/bin/env python3
"""End-to-end SOP pipeline test for the core agents."""
import json
from pathlib import Path

from agents.watson_phase import run_watson
from agents.father_phase import run_father
from agents.mother_phase import run_mother
from agents.arbiter_phase import run_arbiter
from agents.soap_phase import run_soap


def main() -> None:
    home = Path.home()
    soap_dir = home / "Soap"
    queue_dir = soap_dir / "agent_queue"
    logs_dir = soap_dir / "data" / "logs"

    queue_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Clear old tasks
    for path in queue_dir.glob("*.json"):
        path.unlink()

    # Sample SOP text
    sample = {
        "raw_text": "Remove wheel. Torque bolts. Grease bearing.",
        "status": "queued"
    }
    task_path = queue_dir / "sample_task.json"
    task_path.write_text(json.dumps(sample, indent=2))

    # Run Watson phase first
    run_watson()

    # Inject required fields so later phases can succeed
    data = json.loads(task_path.read_text())
    data["tools"] = ["socket", "torque wrench"]
    data["materials"] = ["grease"]
    data["industry"] = "General"
    data["procedure"] = [
        "Remove wheel", "Grease bearing", "Torque bolts"
    ]
    task_path.write_text(json.dumps(data, indent=2))

    # Continue through remaining agents
    run_father()
    run_mother()
    run_arbiter()
    run_soap()

    # Load result
    result = json.loads(task_path.read_text())
    print(json.dumps(result, indent=2))

    # Basic validation
    if result.get("status") != "soap_complete":
        raise SystemExit("Test failed: final status not soap_complete")
    print("\N{white heavy check mark} SOP pipeline test passed")


if __name__ == "__main__":
    main()
