"""Modbus TCP register reader for the shop-floor bridge.

Register map (holding registers), configurable per machine model in
`read_machine_state()`:

  HR[0] — status (0 = idle, 1 = running)
  HR[1] — speed (units/hour)
  HR[2] — counter (total units produced)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

logger = logging.getLogger(__name__)

DEFAULT_REGISTER_COUNT = 100


@dataclass(frozen=True, slots=True)
class MachineState:
    """Decoded holding-register snapshot for one machine."""

    status: int
    speed: int
    counter: int


def read_machine_state(
    host: str, port: int = 502, register_count: int = DEFAULT_REGISTER_COUNT
) -> MachineState | None:
    """Read holding registers `HR[0:register_count]` from one machine.

    Returns `None` if the machine is unreachable or the read fails — callers
    should treat that as "skip this poll cycle", not a fatal error.
    """
    client = ModbusTcpClient(host, port=port)
    try:
        if not client.connect():
            logger.warning("no connection to machine at %s:%s", host, port)
            return None
        result = client.read_holding_registers(0, count=register_count)
        if result.isError():
            logger.error("Modbus read error from %s:%s: %s", host, port, result)
            return None
        registers = result.registers
        return MachineState(status=registers[0], speed=registers[1], counter=registers[2])
    except ModbusException as exc:
        logger.error("Modbus exception for %s:%s: %s", host, port, exc)
        return None
    finally:
        client.close()
