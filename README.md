# Sample Data Generator

Publishes sample IoT datasets to **MQTT**, **Kafka**, **REST (PUT / POST)**, and **OPC-UA**.  
Data files are hosted at `http://45.33.11.32/Sample-Data/`.

---

## Project Structure

```
source/
├── main.py                      ← entry point
├── northbound/                  ← publishers
│   ├── mqtt.py
│   ├── kafka.py
│   ├── rest_calls.py
│   ├── opcua.py
│   └── support.py               ← unified publish_data() dispatcher
└── southbound/                  ← data generators
    ├── support.py               ← shared file fetch / decode / timestamp
    ├── random_data.py
    ├── rig_data.py
    ├── vessel_data.py
    ├── wind_turbine.py
    ├── wind_turbine2.py
    └── proveit_data.py
```

---

## Usage

```
python source/main.py <generator> [options]
```

### Positional argument

| Value | Dataset |
|---|---|
| `rand` | Random float values |
| `rigs` | Oil rig sensor data (6 rigs, Permian / Eagle Ford / Bakken / GoM / Delaware / STACK) |
| `vessel` | Marine vessel motor telemetry (DLB / DLT sides) |
| `wind-turbine` | German-locale wind turbine CSV data (turbines 1–11, excl. 4) |
| `wind-turbine2` | Farm-structured wind turbine JSON data (Farm 1: 4 turbines, Farm 2: 2 turbines) |
| `proveit` | ProveIT IoT device telemetry (~40 files, topic-embedded payloads) |

### Options

| Flag | Default | Description |
|---|---|---|
| `--method` | `print` | `print` · `put` · `post` · `mqtt` · `kafka` · `opcua` |
| `--conn` | `127.0.0.1:32149` | Broker / REST connection: `{user}:{password}@{ip}:{port}` or `{ip}:{port}` |
| `--db-name` | `mydb` | Logical database name |
| `--iterations` | `10` | Number of full dataset cycles. `0` = run continuously |
| `--wait-time` | `1` | Seconds between iterations |
| `--standalone-values` | `False` | Publish each key/value pair as its own subtopic |

---

## Examples

```bash
# Print random data to stdout
python source/main.py rand

# Publish rig data via MQTT
python source/main.py rigs --method mqtt --conn 192.168.1.10:1883 --db-name rig_db

# Publish vessel data via REST POST, run continuously
python source/main.py vessel --method post --conn 10.0.0.1:7849 --iterations 0

# Publish wind turbine data via Kafka
python source/main.py wind-turbine2 --method kafka --conn 10.0.0.1:9092 --db-name turbine_db

# Publish proveit data via OPC-UA
python source/main.py proveit --method opcua
```

---

## Publish Methods

### OPC-UA
OPC-UA spins up a local server — no `--conn` is required.  
Each generator binds to a fixed port:

| Generator | Port |
|---|---|
| `rand` | 4841 |
| `vessel` | 4842 |
| `rigs` | 4843 |
| `wind-turbine` | 4844 |
| `wind-turbine2` | 4844 |
| `proveit` | 4845 |

Topics are mapped to the OPC-UA node tree using the MQTT-style topic path as the folder hierarchy.  
Connect an OPC-UA client (e.g. Prosys, UA Expert) to `opc.tcp://<host>:<port>/freeopcua/data-generator`.

### MQTT / Kafka
Pass broker details via `--conn`:
```bash
--conn 192.168.1.10:1883              # anonymous
--conn user:password@192.168.1.10:1883  # authenticated
```

### REST PUT / POST
Pass the AnyLog / EdgeLake node address via `--conn`:
```bash
--conn 10.0.0.1:7849
```
PUT streams data directly to a table.  
POST routes data through a topic-based mapping policy.

---

## Standalone Values (`--standalone-values`)

When enabled, each key/value pair in a JSON payload is published as its own subtopic:

```
rand-data/timestamp  →  "2026-01-01T00:00:00.000000Z"
rand-data/value      →  0.7342
```

Without the flag, the full JSON object is published to the root topic.

> **Note:** `--standalone-values` is not yet fully implemented for all generators.

---

## Dataset Notes

All data files are fetched at runtime from `http://45.33.11.32/Sample-Data/`:

| Generator | Path |
|---|---|
| `rigs` | `Sample-Data/rig-data/` |
| `vessel` | `Sample-Data/vessel-data/` |
| `wind-turbine` | `Sample-Data/wind-turbine/` |
| `wind-turbine2` | `Sample-Data/wind-turbine2/{farm}/{turbine}/` |
| `proveit` | `Sample-Data/proveit-data2/` |

`rand` generates data locally — no remote files required.

---

## Known Limitations

- **`proveit` does not support PUT** — proveit payloads are standalone values by default (each row carries its own embedded topic), which is incompatible with the table-direct PUT format. Use `post`, `mqtt`, `kafka`, or `opcua` instead.
- **`--standalone-values` with PUT** — if `--standalone-values` is specified alongside `--method put`, the method is automatically switched to POST.
