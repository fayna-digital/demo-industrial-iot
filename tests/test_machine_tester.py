"""Unit tests for the machine connectivity heartbeat."""

from __future__ import annotations

from src.bridge.machine_tester import MachineTester


def test_demo_mode_returns_bool() -> None:
    tester = MachineTester(demo_mode=True)
    assert isinstance(tester.check_status("Heidelberg-XL-106"), bool)


def test_ping_unreachable_host_returns_false() -> None:
    tester = MachineTester(demo_mode=False)
    # TEST-NET-1 (RFC 5737) — reserved for documentation, never routable.
    assert tester.check_status("HP-Indigo-6k", host="192.0.2.1") is False
