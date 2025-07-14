"""
Creates the required folder architecture for the ATI Oracle Engine.
Ensures snapshot folders, system agent directories, heartbeat logs, and manifest entries exist.
Protects all critical directories from deletion.
"""

from pathlib import Path
import json
from datetime import datetime

ROOT = Path.home() / "Soap"
SNAPSHOT_AGENTS = ["watson", "father", "arbiter", "soap", "streamkeeper", "healer"]
LOG_PATH = ROOT / "logs" / "codex_init.log"
MANIFEST_PATH = ROOT / "overlay" / "manifest.json"

FOLDERS = [
    ROOT / "agents",
    ROOT / "system_agents",
    ROOT / "overlay",
    ROOT / "logs" / "heartbeat",
    ROOT / "relay",
    ROOT / "chunks",
    ROOT / "outputs",
    ROOT / "snapshots" / "recovery_logs"
] + [ROOT / "snapshots" / agent for agent in SNAPSHOT_AGENTS]


def ensure_folder(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("# Keep folder for Git")


def log_event(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")


def update_manifest() -> None:
    manifest = {}
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text())
        except json.JSONDecodeError:
            log_event("[ERROR] Corrupt manifest.json, regenerating.")

    manifest["protected_folders"] = sorted(str(p.relative_to(ROOT)) for p in FOLDERS)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    log_event("[OK] Updated manifest.json with protected folders.")


def ensure_all_folders() -> None:
    for folder in FOLDERS:
        ensure_folder(folder)
        log_event(f"[CREATE] {folder}")
    update_manifest()


if __name__ == "__main__":
    ensure_all_folders()
    print("[✅] Folder structure created and manifest updated.")
