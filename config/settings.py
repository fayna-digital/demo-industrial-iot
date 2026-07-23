"""Runtime configuration for the Industrial IoT Bridge.

Every value can be overridden via an environment variable, so the same code
runs unchanged against a demo Odoo instance and a client's production
database — no credentials are ever hard-coded in this repository.
"""

from __future__ import annotations

import os


def _env_bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


# Odoo connection (XML-RPC)
ODOO_URL = os.getenv("BRIDGE_ODOO_URL", "https://your-odoo-instance.com")
ODOO_DB = os.getenv("BRIDGE_ODOO_DB", "your_database")
ODOO_USER = os.getenv("BRIDGE_ODOO_USER", "admin@example.com")
ODOO_PASSWORD = os.getenv("BRIDGE_ODOO_PASSWORD", "")

# Modbus TCP (shop-floor machines / plc_simulator.py)
PLC_HOST = os.getenv("BRIDGE_PLC_HOST", "127.0.0.1")
PLC_PORT = int(os.getenv("BRIDGE_PLC_PORT", "5020"))
REGISTER_COUNT = int(os.getenv("BRIDGE_REGISTER_COUNT", "100"))

# Local SQLite buffer (queues events while Odoo is unreachable)
DB_PATH = os.getenv("BRIDGE_DB_PATH", "production_buffer.db")

# Machine connectivity check: demo mode simulates results so the full flow
# runs without physical hardware; disable for a real ICMP heartbeat.
DEMO_MODE = _env_bool("BRIDGE_DEMO_MODE", True)

# Logging
LOG_LEVEL = os.getenv("BRIDGE_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"

# Privacy (RODO/GDPR): this bridge carries production counters only —
# machine id, unit counts, status. No personal data is generated or stored
# by design. If a future integration adds operator identifiers, treat them
# as personal data: opt-in only, documented retention, access controls.
