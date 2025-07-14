#!/usr/bin/env python3
"""Master controller for the SOP pipeline.

Scans ~/Soap/agent_queue for tasks and runs them through all five
agents in sequence. Completed SOPs are exported to ~/Soap/overlay/sops/.
"""
import argparse
import json
import time
from pathlib import Path

from agents.watson_phase import run_watson
from agents.father_phase import run_father
from agents.mother_phase import run_mother
from agents.arbiter_phase import run_arbiter
from agents.soap_phase import run_soap
from warm_start_engine import load_vectors
from rag_vectorizer import vectorize


def process_queue(root: Path) -> None:
    """Run all agents once and export completed SOPs."""
    queue_dir = root / "agent_queue"
    output_dir = root / "overlay" / "sops"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not any(queue_dir.glob("*.json")):
        return

    run_watson()
    run_father()
    run_mother()
    run_arbiter()
    run_soap()
    vectorize()

    for path in queue_dir.glob("*.json"):
        data = json.loads(path.read_text())
        if data.get("status") == "soap_complete":
            out = output_dir / path.name
            out.write_text(json.dumps(data, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SOP pipeline")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Continuously watch queue",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Loop sleep seconds",
    )
    parser.add_argument(
        "--warm-start",
        action="store_true",
        help="Load vector store before running",
    )
    args = parser.parse_args()

    root = Path.home() / "Soap"
    if args.warm_start:
        load_vectors()
    while True:
        process_queue(root)
        if not args.loop:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
