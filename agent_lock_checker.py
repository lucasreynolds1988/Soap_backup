#!/usr/bin/env python3
"""Verify agent file integrity by comparing SHA256 hashes."""
import hashlib
import json
import logging
import os
from pathlib import Path

AGENTS = [
    "watson_phase.py",
    "father_phase.py",
    "mother_phase.py",
    "arbiter_phase.py",
    "soap_phase.py",
]


def get_soap_root() -> Path:
    env = os.getenv("SOAP_ROOT")
    return Path(env).expanduser() if env else Path.home() / "Soap"


def load_reference(root: Path) -> dict:
    ref_path = root / "overlay" / "agent_hashes.json"
    if not ref_path.is_file():
        raise FileNotFoundError(f"Reference hash file missing: {ref_path}")
    return json.loads(ref_path.read_text())


def compute_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def check_agents() -> int:
    root = get_soap_root()
    ref = load_reference(root)
    mismatches = []
    for name in AGENTS:
        file_path = root / "agents" / name
        current = compute_hash(file_path)
        if ref.get(name) != current:
            mismatches.append(name)
    if mismatches:
        logging.error(
            "Agent integrity check failed: %s", ", ".join(mismatches)
        )
        return 1
    logging.info("All agent hashes verified.")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(check_agents())
