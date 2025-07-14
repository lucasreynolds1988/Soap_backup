# Agents Overview

This repository defines five protected agents for the SOP generation pipeline. Their logic is locked and should not be edited outside official updates.

| Agent File | Purpose |
|------------|---------|
| `watson_phase.py` | Formats raw SOP tasks into structured data. |
| `father_phase.py` | Validates logic and ensures procedural consistency. |
| `mother_phase.py` | Applies safety rules and regulatory checks. |
| `arbiter_phase.py` | Resolves conflicts and finalizes status. |
| `soap_phase.py` | Generates the final explanation and technical notes. |

## Protection Policy

- Users may enable or disable agents via `agent_config.json` and assign different AI models.
- Editing the core agent files is restricted. Use configuration files to adjust behavior instead of modifying code directly.
- A helper script `agent_lock_checker.py` verifies the integrity of these files by comparing SHA256 hashes against a reference list.
