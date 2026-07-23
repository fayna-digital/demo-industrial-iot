"""Industrial IoT Bridge — orchestrator.

Polls the configured shop-floor machines, checks connectivity, and (in a
full deployment) forwards production counters to Odoo MRP via `OdooAPI`.
Run with `python -m src.bridge.main`.
"""

from __future__ import annotations

import logging
import sys

from config import settings
from src.bridge.machine_tester import MachineTester

logger = logging.getLogger(__name__)

MONITORED_ASSETS = ("Heidelberg-XL-106", "HP-Indigo-6k")


def run(assets: tuple[str, ...] = MONITORED_ASSETS) -> int:
    """Check connectivity for every monitored asset. Returns a process exit code."""
    tester = MachineTester(demo_mode=settings.DEMO_MODE)
    had_error = False
    for asset_id in assets:
        if tester.check_status(asset_id):
            logger.info("%s: data stream active, ready to sync with Odoo MRP", asset_id)
        else:
            logger.error("%s: critical error, machine unreachable", asset_id)
            had_error = True
    return 1 if had_error else 0


def main() -> int:
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
        format=settings.LOG_FORMAT,
    )
    logger.info("Fayna Digital Industrial IoT Bridge — starting")
    return run()


if __name__ == "__main__":
    sys.exit(main())
