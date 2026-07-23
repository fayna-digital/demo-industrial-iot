"""Odoo XML-RPC client — pushes machine production events to Odoo MRP."""

from __future__ import annotations

import logging
import xmlrpc.client
from typing import Any, cast

from config import settings

logger = logging.getLogger(__name__)

_LOG_MODEL = "fayna.iot.machine.log"


class OdooAPI:
    """Thin XML-RPC client: authenticates once, then writes IoT log records."""

    def __init__(self) -> None:
        self._common = xmlrpc.client.ServerProxy(f"{settings.ODOO_URL}/xmlrpc/2/common")
        self._models = xmlrpc.client.ServerProxy(f"{settings.ODOO_URL}/xmlrpc/2/object")
        self._uid = self._authenticate()

    def _authenticate(self) -> int:
        uid = self._common.authenticate(
            settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {}
        )
        if not uid:
            raise RuntimeError("Odoo authentication failed — check BRIDGE_ODOO_* env vars")
        return cast(int, uid)

    def push_log(self, machine_id: str, units: int, state: str) -> int:
        """Create one record in `fayna.iot.machine.log`. Returns the new record id."""
        values: dict[str, Any] = {
            "workcenter_id": machine_id,
            "units_delta": units,
            "state": state,
        }
        try:
            new_id = self._models.execute_kw(
                settings.ODOO_DB,
                self._uid,
                settings.ODOO_PASSWORD,
                _LOG_MODEL,
                "create",
                [values],
            )
        except xmlrpc.client.Fault as exc:
            logger.error("Odoo push failed for %s: %s", machine_id, exc)
            raise
        return cast(int, new_id)
