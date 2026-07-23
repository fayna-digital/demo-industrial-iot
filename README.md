# 🏭 Industrial IoT Bridge — Odoo 17 MRP Integration

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Modbus](https://img.shields.io/badge/Modbus-TCP-red)
![Odoo](https://img.shields.io/badge/Odoo-17.0%20MRP-purple)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-demo%20%2F%20portfolio-orange)

**Developed by [Fayna Digital](https://fayna.agency) — Author: Volodymyr Shevchenko**

---

## Problem

Printing houses and manufacturing shops with 2–10 industrial machines
(offset, digital, CNC) track production the way most SMEs do: an operator
walks the floor with a clipboard and re-types counters into the ERP at the
end of a shift. It's slow, error-prone, and by the time a manager sees the
numbers the shift is already over.

## Solution

A lightweight **Industrial IoT Bridge** written in Python that reads machine
state directly off the shop floor — over Modbus TCP — and pushes it straight
into **Odoo 17 MRP** work orders via XML-RPC, with a local SQLite buffer so
no reading is lost if Odoo is briefly unreachable. A bundled Modbus
simulator (`plc_simulator.py`) lets the entire flow run end-to-end without
any physical hardware, which is what this public demo ships with.

> **Note:** this is a portfolio/demo project. Client-specific logic,
> credentials, and register maps are excluded — see [Business context](#business-context).

## Result

- Manual counter entry eliminated — production data lands in Odoo work
  orders as it happens, not at end of shift.
- Local buffering means a flaky network link no longer means lost data: the
  bridge keeps reading, queues locally, and syncs once Odoo is reachable
  again.
- The concept proved out here now runs in production, extended into a full
  Odoo module with an operator kiosk and manager dashboard — see
  [Related projects](#related-projects).

## Stack

Python 3.10+ · [pymodbus](https://github.com/pymodbus-dev/pymodbus) (Modbus
TCP) · `xmlrpc.client` (Odoo integration, stdlib) · SQLite (local buffer) ·
pytest / ruff / mypy.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│             Industrial Machine Floor             │
│   Heidelberg XL-106  │  HP Indigo 6K             │
│   (offset printing)  │  (digital printing)       │
└────────────┬─────────────────────────────────────┘
             │  Modbus TCP / ICMP heartbeat
             ▼
┌─────────────────────────────────────────────────┐
│             Industrial IoT Bridge                │
│  machine_tester.py  ← heartbeat / connectivity   │
│  scanner.py         ← Modbus TCP reader          │
│  main.py            ← orchestrator               │
│  odoo_api.py        ← XML-RPC client to Odoo     │
│  db_handler.py      ← local buffer (SQLite)      │
└────────────┬─────────────────────────────────────┘
             │  Odoo XML-RPC
             ▼
┌─────────────────────────────────────────────────┐
│              Odoo 17 MRP                         │
│  Work Orders  │  Production Reports  │  MO       │
└─────────────────────────────────────────────────┘
```

## Components

| File | Role |
|------|------|
| `src/bridge/main.py` | Orchestrator — checks each monitored asset, drives the poll loop |
| `src/bridge/machine_tester.py` | Connectivity heartbeat — demo-mode simulation or real ICMP ping |
| `src/bridge/scanner.py` | Modbus TCP reader — reads holding registers (status, speed, counter) |
| `src/bridge/odoo_api.py` | Odoo XML-RPC client — pushes readings to Work Orders |
| `src/bridge/db_handler.py` | Local SQLite buffer — queues data while Odoo is unreachable |
| `src/bridge/plc_simulator.py` | Modbus server simulator — full flow without physical hardware |
| `config/settings.py` | All configuration, env-var driven — no secrets in code |

## Modbus register map

| Register | Value |
|----------|-------|
| `HR[0]` | Status: `0` = idle, `1` = running |
| `HR[1]` | Speed (units/hour) |
| `HR[2]` | Counter (total units produced) |

> Register maps vary per machine model — configure in
> `src/bridge/scanner.py` → `read_machine_state()`.

---

## Quick start

### Requirements

- Python 3.10+
- `pip install -r requirements.txt`
- An Odoo 17.0 instance (or skip it — the Modbus side runs fully offline)

### Run with the bundled simulator (no hardware, no Odoo)

```bash
# Terminal 1 — start the Modbus simulator
python -m src.bridge.plc_simulator
# Exposes a Modbus server on 127.0.0.1:5020

# Terminal 2 — run the bridge (demo mode, connectivity check only)
python -m src.bridge.main
```

### Configure

All settings are environment variables (see `config/settings.py` for the
full list and defaults) — nothing is hard-coded:

```bash
export BRIDGE_ODOO_URL="https://your-odoo-instance.com"
export BRIDGE_ODOO_DB="your_database"
export BRIDGE_ODOO_USER="admin@company.com"
export BRIDGE_ODOO_PASSWORD="your_api_key"
export BRIDGE_DEMO_MODE=false   # use a real ICMP heartbeat instead of simulation
```

### Tests

```bash
python -m pytest tests/ -v
```

---

## Business context

**Industry:** Printing / manufacturing
**Client profile:** Printing house or shop with 2–10 industrial machines
**Problem solved:** Manual production-data entry into the ERP — slow,
error-prone, delayed by a full shift
**Solution:** Automated bridge pushing real-time machine output straight
into Odoo work orders
**Data handling:** All data stays on-premises or in the client's own cloud —
no third-party SaaS in the loop, and no personal data is generated or
stored by the bridge itself

## Related projects

- [dnj-shopfloor](https://github.com/VladSh77/dnj-shopfloor) — the full
  production Odoo module this demo's concept was extended into: operator
  kiosk, manager dashboard, and a hardened Modbus bridge.

## License

MIT — see [LICENSE](LICENSE).

---

*Built by [Fayna Digital](https://fayna.agency) · Volodymyr Shevchenko*
*Systems architecture & industrial automation for manufacturing SMEs*
