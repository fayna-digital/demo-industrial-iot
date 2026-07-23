"""Regression test for the PLC simulator's register alignment.

`ModbusSequentialDataBlock` maps its `address` parameter onto the server's
internal PDU addressing — get this wrong and every read silently shifts by
one register instead of raising an error. This test would have caught it.
"""

from __future__ import annotations

from src.bridge.plc_simulator import build_context


def test_initial_registers_align_with_client_address_zero() -> None:
    context = build_context()
    device = context[0]

    # function code 3 = read holding registers; client address 0, count 3.
    registers = device.getValues(3, 0, count=3)

    assert registers == [1, 12000, 5500]
