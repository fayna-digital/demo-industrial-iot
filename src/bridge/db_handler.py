"""SQLite buffer for production events pending sync to Odoo.

Machines are polled more often than Odoo can reliably be reached (network
blips, maintenance windows). Every read is written here first and marked
synced only after a confirmed push, so no production event is lost.
"""

from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import TracebackType

logger = logging.getLogger(__name__)

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS production_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id TEXT NOT NULL,
    units INTEGER NOT NULL,
    status TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    synced INTEGER NOT NULL DEFAULT 0
)
"""


@dataclass(frozen=True, slots=True)
class ProductionLog:
    """One buffered production event."""

    id: int
    machine_id: str
    units: int
    status: str
    timestamp: str
    synced: bool


class DBHandler:
    """Local SQLite buffer that queues production events until Odoo is reachable."""

    def __init__(self, db_path: str | Path = "production_buffer.db") -> None:
        self._db_path = Path(db_path)
        self._conn = sqlite3.connect(self._db_path)
        self._create_table()

    def _create_table(self) -> None:
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    def log_production(self, machine_id: str, units: int, status: str = "running") -> None:
        """Persist one production event locally."""
        self._conn.execute(
            "INSERT INTO production_logs (machine_id, units, status, timestamp) "
            "VALUES (?, ?, ?, ?)",
            (machine_id, units, status, datetime.now(timezone.utc).isoformat()),
        )
        self._conn.commit()
        logger.info("buffered %d unit(s) from %s", units, machine_id)

    def get_unsynced_logs(self) -> list[ProductionLog]:
        """Return all production events not yet pushed to Odoo."""
        cursor = self._conn.execute(
            "SELECT id, machine_id, units, status, timestamp, synced "
            "FROM production_logs WHERE synced = 0"
        )
        return [
            ProductionLog(
                id=row[0],
                machine_id=row[1],
                units=row[2],
                status=row[3],
                timestamp=row[4],
                synced=bool(row[5]),
            )
            for row in cursor.fetchall()
        ]

    def mark_as_synced(self, log_id: int) -> None:
        """Flag one event as pushed to Odoo."""
        self._conn.execute("UPDATE production_logs SET synced = 1 WHERE id = ?", (log_id,))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> DBHandler:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
