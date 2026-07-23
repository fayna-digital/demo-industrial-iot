"""Modbus TCP simulator — stand-in for a real machine's PLC.

Lets the full bridge flow (scanner -> Odoo push) run without physical
hardware: `python -m src.bridge.plc_simulator`.
"""

from __future__ import annotations

import logging

from pymodbus.datastore import (
    ModbusDeviceContext,
    ModbusSequentialDataBlock,
    ModbusServerContext,
)
from pymodbus.server import StartTcpServer

logger = logging.getLogger(__name__)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5020

# HR[0]=status (1=running), HR[1]=speed, HR[2]=counter, HR[3:100]=reserved
_INITIAL_REGISTERS = [1, 12000, 5500] + [0] * 97


def build_context() -> ModbusServerContext:
    """Build a single-device Modbus context seeded with demo register values.

    `ModbusSequentialDataBlock`'s starting address must be `1`, not `0`: the
    server maps client-requested PDU address 0 onto the block's `address`
    offset internally, so a block created at address 0 would silently drop
    its first value and shift every read by one register.
    """
    device = ModbusDeviceContext(hr=ModbusSequentialDataBlock(1, _INITIAL_REGISTERS))
    return ModbusServerContext(devices=device, single=True)


def run_simulator(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Start the simulated Modbus TCP server (blocking)."""
    logging.basicConfig(level=logging.INFO)
    logger.info("simulator online at %s:%s", host, port)
    StartTcpServer(context=build_context(), address=(host, port))


if __name__ == "__main__":
    run_simulator()
