"""Unit tests for the local SQLite production buffer."""

from __future__ import annotations

from pathlib import Path

from src.bridge.db_handler import DBHandler


def test_log_and_fetch_unsynced(tmp_path: Path) -> None:
    with DBHandler(tmp_path / "buffer.db") as db:
        db.log_production("Heidelberg-XL-106", units=42, status="running")
        pending = db.get_unsynced_logs()

        assert len(pending) == 1
        assert pending[0].machine_id == "Heidelberg-XL-106"
        assert pending[0].units == 42
        assert pending[0].synced is False


def test_mark_as_synced_removes_from_pending(tmp_path: Path) -> None:
    with DBHandler(tmp_path / "buffer.db") as db:
        db.log_production("HP-Indigo-6k", units=10)
        [log] = db.get_unsynced_logs()

        db.mark_as_synced(log.id)

        assert db.get_unsynced_logs() == []


def test_multiple_machines_are_isolated(tmp_path: Path) -> None:
    with DBHandler(tmp_path / "buffer.db") as db:
        db.log_production("Heidelberg-XL-106", units=5)
        db.log_production("HP-Indigo-6k", units=7)

        pending = {log.machine_id: log.units for log in db.get_unsynced_logs()}

        assert pending == {"Heidelberg-XL-106": 5, "HP-Indigo-6k": 7}
