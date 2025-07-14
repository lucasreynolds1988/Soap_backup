#!/usr/bin/env python3
"""Backup Now Trigger.

Runs the ``+FULL_SAVE_NOW+`` trigger to immediately save and upload the
current Soap state. Logs execution to ``~/Soap/logs/backup_now.log`` by default
unless ``BACKUP_LOG_PATH`` is defined in the environment.
"""
import logging
import os
import subprocess
import sys
from pathlib import Path


def get_soap_root() -> Path:
    """Return the Soap root directory."""
    env_path = os.getenv("SOAP_ROOT")
    return Path(env_path).expanduser() if env_path else Path.home() / "Soap"


def setup_logger() -> logging.Logger:
    """Configure file and console logger."""
    default_log = get_soap_root() / "logs/backup_now.log"
    env_log = os.getenv("BACKUP_LOG_PATH")
    log_file = Path(env_log if env_log else default_log).expanduser()

    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("backup_now")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s %(message)s")
    fh = logging.FileHandler(log_file)
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    return logger


def main() -> None:
    logger = setup_logger()
    trigger = get_soap_root() / "triggers/+FULL_SAVE_NOW+"
    logger.info("Backup Now triggered. Using trigger %s", trigger)
    print("🗄️ [BACKUP-NOW] Calling +FULL_SAVE_NOW+ trigger...")
    if not trigger.is_file():
        logger.error("Trigger not found: %s", trigger)
        sys.exit(f"Trigger not found: {trigger}")

    try:
        subprocess.run(["bash", str(trigger)], check=True)
    except subprocess.CalledProcessError as exc:
        logger.error("Backup failed with code %s", exc.returncode)
        print("❌ [BACKUP-NOW] Backup failed.")
        sys.exit(exc.returncode)
    else:
        logger.info("Backup completed successfully.")
        print("✅ [BACKUP-NOW] Backup finished.")


if __name__ == "__main__":
    main()
