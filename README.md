# Sample Data Generator

Publishes sample IoT datasets to **MQTT**, **Kafka**, **REST (PUT / POST)**, and **OPC-UA**.  
Data files are hosted at `http://45.33.11.32/Sample-Data/`.

Pre-built sample scripts for MQTT are available in [`data-generator-scripts/`](data-generator-scripts) and are also 
included in the deployment-scripts package downloaded as part of AnyLog.

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

| Value | Dataset                                                                             |
|---|-------------------------------------------------------------------------------------|
| `rand` | Random float values                                                                 |
| `rigs` | Oil rig sensor data (6 rigs, Permian / Eagle Ford / Bakken / GoM / Delaware / STACK) |
| `vessel` | Marine vessel motor telemetry (DLB / DLT sides)                                     |
| `wind-turbine` | German-locale wind turbine CSV data (turbines 1–11, excl. 4)                        |
| `wind-turbine2` | Farm-structured wind turbine JSON data (Farm 1: 4 turbines, Farm 2: 2 turbines)     |
| `proveit` | ProveIT conference IoT device telemetry (~40 files, topic-embedded payloads)        |

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
python source/main.py rigs --method mqtt --conn 172.104.228.251:1883 --db-name rig_db

# Publish vessel data via REST POST, run continuously
python source/main.py vessel --method post --conn 10.0.0.1:7849 --iterations 0

# Publish wind turbine data via Kafka
python source/main.py wind-turbine2 --method kafka --conn 10.0.0.1:9092 --db-name turbine_db

# Publish proveit data via OPC-UA
python source/main.py proveit --method opcua
```

---

## Publish Methods

### MQTT

Default broker: `172.104.228.251:1883`

Payloads are published as **serialized JSON lists**, except for `proveit` which uses standalone values by default
(each row carries its own embedded topic).

MQTT topics per generator:

| Generator | Topic pattern |
|---|---|
| `rand` | `rand-data` |
| `rigs` | `rig-data/rig-{rig_id}` |
| `vessel` | `vessel-data/{side}` |
| `wind-turbine` | `wind-turbine/turbine-{turbine_id}` |
| `wind-turbine2` | `wind-turbine2/{farm}/{turbine}/{mapped}` |
| `proveit` | `proveit/{sub_topic}` |

Sample scripts for all generators are available in `data-generator-scripts/` and in the AnyLog deployment-scripts package.

```bash
--conn 172.104.228.251:1883              # anonymous
--conn user:password@172.104.228.251:1883  # authenticated
```

### OPC-UA

Default server: `172.233.108.122`

OPC-UA spins up a local server — no `--conn` is required. By default, OPC-UA publishes using
`--standalone-values` (each key/value pair as its own subtopic rather than a serialized JSON object).

Each generator binds to a fixed port:

| Generator | Port | OPC-UA endpoint |
|---|---|---|
| `rand` | 4841 | `opc.tcp://172.233.108.122:4841/freeopcua/data-generator` |
| `vessel` | 4842 | `opc.tcp://172.233.108.122:4842/freeopcua/data-generator` |
| `rigs` | 4843 | `opc.tcp://172.233.108.122:4843/freeopcua/data-generator` |
| `wind-turbine` | 4844 | `opc.tcp://172.233.108.122:4844/freeopcua/data-generator` |
| `wind-turbine2` | 4844 | `opc.tcp://172.233.108.122:4844/freeopcua/data-generator` |
| `proveit` | 4845 | `opc.tcp://172.233.108.122:4845/freeopcua/data-generator` |

Topics are mapped to the OPC-UA node tree using the MQTT-style topic path as the folder hierarchy.
Connect an OPC-UA client (e.g. Prosys, UA Expert) to the endpoint shown above.

### Kafka

Pass broker details via `--conn`:

```bash
--conn 10.0.0.1:9092
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

Without the flag, the full JSON object is published to the root topic as a serialized list.

Default behaviour by method:

| Method | Default payload format |
|---|---|
| MQTT | Serialized JSON (full object), except `proveit` which always uses standalone values |
| OPC-UA | Standalone values (`--standalone-values` on by default) |
| REST PUT / POST | Serialized JSON |
| Kafka | Serialized JSON |

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

- **`proveit` does not support PUT** — proveit payloads are standalone values by default (each row carries its own
  embedded topic), which is incompatible with the table-direct PUT format. Use `post`, `mqtt`, `kafka`, or `opcua` instead.
- **`--standalone-values` with PUT** — if `--standalone-values` is specified alongside `--method put`, the method
  is automatically switched to POST.