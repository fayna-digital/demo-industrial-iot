"""Connectivity heartbeat for shop-floor machines.

In demo mode (default, no hardware required) the result is simulated so the
full bridge flow can be exercised end-to-end with `plc_simulator.py`. Outside
demo mode it performs a real ICMP ping via the system `ping` binary.
"""

from __future__ import annotations

import logging
import random
import subprocess
from dataclasses import dataclass

logger = logging.getLogger(__name__)

_PING_TIMEOUT_S = 1


@dataclass(frozen=True, slots=True)
class MachineTester:
    """Checks whether a machine on the shop floor is reachable."""

    demo_mode: bool = True

    def check_status(self, machine_id: str, host: str = "127.0.0.1") -> bool:
        """Return True if `machine_id` (at `host`) is reachable."""
        online = self._simulate() if self.demo_mode else self._ping(host)
        if online:
            logger.info("%s: online", machine_id)
        else:
            logger.warning("%s: unreachable", machine_id)
        return online

    @staticmethod
    def _simulate() -> bool:
        return random.choice([True, True, False])

    @staticmethod
    def _ping(host: str) -> bool:
        try:
            result = subprocess.run(
                ["ping", "-c", "1", host],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=_PING_TIMEOUT_S + 1,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
            logger.error("ping failed for %s: %s", host, exc)
            return False
        return result.returncode == 0
