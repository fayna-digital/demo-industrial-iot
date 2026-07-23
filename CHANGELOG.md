# Changelog

Format — [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning — [SemVer](https://semver.org/).

## [0.1.0] — 2026-07-23

### Added

- Public showcase extraction of the **Industrial IoT Bridge** demo (Modbus
  TCP scanner, connectivity heartbeat, Odoo XML-RPC push, SQLite buffer,
  bundled PLC simulator).
- Repository brought to Fayna **REPO_STANDARD**: README with problem →
  solution → result → stack, MIT LICENSE, `docs/TZ.md`, `tests/`,
  `.pre-commit-config.yaml`, CI (lint + tests).
- `no-ai-signature` guard (pre-commit) — blocks AI attribution in code and
  commits going forward.
- Config moved fully to environment variables (`BRIDGE_ODOO_*`,
  `BRIDGE_PLC_*`, `BRIDGE_DEMO_MODE`, ...) — no credentials or endpoints
  hard-coded anywhere in the repo.
- Restructured into an installable package (`src/bridge/`, `config/`) with
  full type hints, specific exception handling, and `logging` in place of
  ad-hoc `print()` calls.
- Unit tests for the SQLite buffer and the connectivity heartbeat.

### Notes

- Re-extracted from an internal working repository via the **showcase
  promotion** procedure. Deliberately **not carried over**: the prior git
  history (which mixed AI-assisted commits into the trail), any
  client-identifying configuration, and a stray malformed filename
  (`db_handler.py)`) from the original working tree.
- `requests` was listed as a dependency in the original README but never
  actually imported — the Odoo client uses stdlib `xmlrpc.client`. Dropped
  from `requirements.txt`; only `pymodbus` remains.
