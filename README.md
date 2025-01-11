# Sample Data Generator

This project is a Dockerized application for generating and publishing sample data. The deployment uses the Docker image `anylogco/sample-data-generator:latest`. The application supports multiple data types, publishing methods, and configuration options.

## Table of Contents
- [Getting Started](#getting-started)
- [Usage](#usage)
  - [Main Arguments](#main-arguments)
  - [Optional Arguments](#optional-arguments)
- [Running with Docker](#running-with-docker)
- [Examples](#examples)
- [License](#license)

## Getting Started

### Prerequisites
- Docker installed on your system.
- Access to the `anylogco/sample-data-generator:latest` image.

### Deployment
The application runs in a Docker container and executes commands via a Python script or `main.sh`.

Ensure that:
- For the `rest_server` publisher, the `--service-port` is open and accessible.
- For other publishers, the service must be reachable by other containers or processes on the node.

## Usage
The primary script is `main.py`. Below are the arguments it supports.

### Main Arguments

#### Positional Arguments:
- **`data_type`**: Specifies the type of data to generate. Supported values:
  - `ping`
  - `percentagecpu`
  - `rand`
  - `r_50`
  - `large`
  - `car`
  - `people`
  - `factory`

- **`publisher`**: Format to publish data. Supported values:
  - `put`
  - `post`
  - `mqtt`
  - `kafka`
  - `server`
  - `opcua`

- **`db_name`**: Logical database name.

#### Optional Arguments:
- `-h, --help`: Show help message and exit.
- `--rest-conn REST_CONN`: Connection information for PUT, POST, MQTT, and Kafka. Format: `[user]:[passwd]@[ip]:[port]`.
- `--batch-size BATCH_SIZE`: Number of rows per insert batch.
- `--total-rows TOTAL_ROWS`: Total rows to insert. Set to `0` for continuous generation.
- `--sleep SLEEP`: Wait time between row inserts (in seconds).
- `--topic TOPIC`: Topic name for POST, MQTT, and Kafka.
- `--timeout TIMEOUT`: REST timeout (in seconds).
- `--qos {0,1,2,3}`: Quality of Service.
- `--service-port SERVICE_PORT`: Server or OPC-UA service port.
- `--create-large-data [CREATE_LARGE_DATA]`: Create a new dataset for large data.
- `--num-tables NUM_TABLES`: Number of tables when creating a large dataset.
- `--num-columns NUM_COLUMNS`: Number of columns per table.
- `--exception [EXCEPTION]`: Whether to print exceptions.

## Running with Docker

To run the application using Docker, use the following command:

```bash
docker run -e VIEW_HELP=true \
           -e CREATE_LARGE_DATA=false \
           -e EXCEPTION=true \
           -e DATA_TYPE=<data_type> \
           -e PUBLISHER=<publisher> \
           -e DB_NAME=<db_name> \
           -e REST_CONN=<rest_conn> \
           -e BATCH_SIZE=<batch_size> \
           -e TOTAL_ROWS=<total_rows> \
           -e SLEEP=<sleep> \
           -e TOPIC=<topic> \
           -e TIMEOUT=<timeout> \
           -e QOS=<qos> \
           -e SERVICE_PORT=<service_port> \
           anylogco/sample-data-generator:latest
```

## Examples

### View Help
To view the help menu:
```bash
docker run -e VIEW_HELP=true anylogco/sample-data-generator:latest
```

### Generate Large Data with Exceptions
```bash
docker run -e CREATE_LARGE_DATA=true \
           -e EXCEPTION=true \
           -e DATA_TYPE=large \
           -e PUBLISHER=put \
           -e DB_NAME=test_db \
           -e REST_CONN=user:pass@127.0.0.1:8080 \
           -e NUM_TABLES=5 \
           -e NUM_COLUMNS=10 \
           anylogco/sample-data-generator:latest
```

### Publish Data via Kafka
```bash
docker run -e DATA_TYPE=factory \
           -e PUBLISHER=kafka \
           -e DB_NAME=production_db \
           -e REST_CONN=user:pass@127.0.0.1:9092 \
           -e TOPIC=data_topic \
           -e TOTAL_ROWS=1000 \
           -e SLEEP=1 \
           anylogco/sample-data-generator:latest
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.
