# Finally Fixed Space Issue
# Confirming final git setup
# Finally fixing push issue
# .netrc Fix Commit
# SSH authentication confirmed working
## System Overview

This repository contains the ATI Nexus platform powering Maintenance Docs. The system uses a chain of five protected agents to convert raw maintenance instructions into detailed standard operating procedures (SOPs).

The pipeline operates on tasks placed in `~/Soap/agent_queue/` and outputs completed SOP files to `~/Soap/overlay/sops/`. Various triggers and rotor scripts manage backups, restoration, and cloud synchronization.


## Backup Utilities

- `backup_now.py` - Runs `~/Soap/triggers/+FULL_SAVE_NOW+` for an immediate full save.
  Set `BACKUP_LOG_PATH` to override the default log file location (`~/Soap/logs/backup_now.log`).
`SOAP_ROOT` can point to a custom Soap directory if the default `~/Soap` path differs.
- `restore_now.py` - Restores the system from GCS by running the `+SPIN-UP+` trigger.
  Use `RESTORE_LOG_PATH` to override the default log file (`~/Soap/logs/restore_now.log`).
- `codex_controller.py` - Processes queued SOP tasks through all agents. Use
  `--loop` to continuously monitor `~/Soap/agent_queue` and export completed
  SOPs to `~/Soap/overlay/sops/`. Pass `--warm-start` to load any existing vector store before processing.
- `warm_start_engine.py` loads TF-IDF vectors from `~/Soap/vector_store/` if present.
- `rag_vectorizer.py` updates the vector store from SOPs in `~/Soap/overlay/sops/`.

## Running codex_controller.py

1. Place a JSON task file in `~/Soap/agent_queue/` with at least a `raw_text` field and set `status` to `queued`.
2. Execute `python3 codex_controller.py` to process the queue once.
3. Use `python3 codex_controller.py --loop` for continuous monitoring (default interval is 5 seconds).
4. Completed SOPs will appear under `~/Soap/overlay/sops/`.

