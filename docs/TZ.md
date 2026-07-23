# TZ — demo-industrial-iot (Industrial IoT Bridge Demo)

> Full checklist of implemented and planned functionality.
> ✅ — done | 🔲 — planned | ❌ — cancelled

---

> **Note:** this is a demo/portfolio project. The production implementation
> is [dnj-shopfloor](https://github.com/VladSh77/dnj-shopfloor) (private).

---

## 1. System components

| Component | File | Status |
|-----------|------|--------|
| Orchestrator (main loop) | `src/bridge/main.py` | ✅ |
| Connectivity heartbeat | `src/bridge/machine_tester.py` | ✅ |
| Modbus TCP reader | `src/bridge/scanner.py` | ✅ |
| Odoo XML-RPC client | `src/bridge/odoo_api.py` | ✅ |
| Local SQLite buffer | `src/bridge/db_handler.py` | ✅ |
| PLC simulator (Modbus server) | `src/bridge/plc_simulator.py` | ✅ |
| Configuration (env-var driven) | `config/settings.py` | ✅ |

---

## 2. Modbus TCP integration

| Function | Status |
|----------|--------|
| Connect to a machine over Modbus TCP | ✅ |
| Read `HR[0]` — status (0=idle, 1=running) | ✅ |
| Read `HR[1]` — speed (units/hour) | ✅ |
| Read `HR[2]` — counter (total units) | ✅ |
| Graceful handling of an unreachable machine | ✅ |
| PLC simulator for hardware-free testing (`127.0.0.1:5020`) | ✅ |
| Per-machine dynamic register map | 🔲 |

---

## 3. Connectivity heartbeat

| Function | Status |
|----------|--------|
| Demo-mode simulated heartbeat (no hardware) | ✅ |
| Real ICMP ping heartbeat (`BRIDGE_DEMO_MODE=false`) | ✅ |
| Online / offline status per machine | ✅ |

---

## 4. Buffer and Odoo API

| Function | Status |
|----------|--------|
| Write to SQLite buffer when Odoo is unreachable | ✅ |
| Send buffered data once Odoo recovers | ✅ |
| Push data to Odoo Work Orders (MRP) | ✅ |
| Odoo XML-RPC authentication | ✅ |
| Retry logic on HTTP 5xx | 🔲 |
| HMAC signature on bridge webhook | 🔲 |

---

## 5. Configuration

| Parameter | File | Status |
|-----------|------|--------|
| `BRIDGE_ODOO_URL`, `BRIDGE_ODOO_DB`, `BRIDGE_ODOO_USER`, `BRIDGE_ODOO_PASSWORD` | `config/settings.py` | ✅ |
| Environment variables instead of hard-coded config | ✅ |

---

## 6. Roadmap / next steps

| Function | Status | Note |
|----------|--------|------|
| OPC-UA for newer Heidelberg presses with Prinect | 🔲 | More complex protocol |
| Docker Compose deploy | 🔲 | Present in dnj-shopfloor |
| MQTT support | 🔲 | For newer IoT devices |
| Automatic register-map detection | 🔲 | By machine model |
| Retry logic on Odoo 500 | 🔲 | Protects against data loss |

---

## Business context

- **Industry:** Printing / manufacturing
- **Client profile:** Printing house with 2–10 industrial machines
- **Task:** Automate production-data entry into Odoo (replacing manual entry)
- **ROI:** 30+ min/day saved on manual entry; real-time data instead of
  end-of-shift estimates
- **Demo:** `python -m src.bridge.plc_simulator` → `python -m src.bridge.main`
  — full flow without hardware
