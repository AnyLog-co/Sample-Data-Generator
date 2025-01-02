import argparse
import asyncio
import json
import string
import os
import random
import uuid
import time

from datetime import datetime
from opcua import Server

HOST = "0.0.0.0"  # Replace with your host IP or name


def __check_num(value):
    try:
        value = int(value)
    except Exception as error:
        raise argparse.ArgumentTypeError(f"Invalid data type for column - expected int but got {type(value)}")
    else:
        if value < 1:
            raise argparse.ArgumentTypeError("Invalid value for column. Minimum value is 1")
    return value


# -- Functions for data description -- #
def describe_data(describe_data_file: str, num_tables: int = 20, num_columns: int = 100, include_quality: bool = False):
    """
    Generate configuration for data flowing into OPC-UA server.
    """
    data = {}
    for table in range(num_tables):
        table_name = f"table_{table + 1}"
        data[table_name] = {}
        for column in ["timestamp", "device_id"]:
            data[table_name][column] = {}
            if column == "timestamp":
                data[table_name][column]["type"] = "datetime"
            elif column == "device_id":
                data[table_name][column]["value"] = uuid.uuid4().__str__()

        column_count = 0
        while column_count < num_columns:
            col_name = f"column_{column_count + 1}"
            col_type = random.choice(["string", "bool", "int", "float"])
            data[table_name][col_name] = {"type": col_type}
            if col_type in ["int", "float"]:
                data[table_name][col_name]["min"] = random.randint(1, 500)
                data[table_name][col_name]["max"] = random.randint(501, 1000)
            elif col_type == "string":
                data[table_name][col_name]["length"] = random.randint(1, 10)
            column_count += 1
            if col_type in ["bool", "int", "float"] and include_quality is True:
                column_count += 1

    with open(describe_data_file, "w") as f:
        f.write(json.dumps(data, indent=4))


def read_description(describe_data_file):
    """Read the JSON description file."""
    with open(describe_data_file, "r") as f:
        return json.loads(f.read())


async def get_column_data(column, props, include_quality: bool = False):
    """Generate data for a single column asynchronously."""
    if column in ["timestamp", "device_id"]:
        return None  # Skip timestamp and device_id

    col_type = props["type"]
    result = {}

    if col_type == "bool":
        result[column] = random.choice([True, False, None])
        if include_quality:
            result[f"quality_{column}"] = "NOk" if result[column] is None else "Ok"
    elif col_type in ["int", "float"]:
        value = round(random.uniform(props["min"], props["max"]), 3)
        result[column] = int(value) if col_type == "int" else value
        if include_quality:
            result[f"quality_{column}"] = (
                "Ok"
                if 0.75 * ((props["min"] + props["max"]) / 2)
                <= value
                <= 1.25 * ((props["min"] + props["max"]) / 2)
                else "Nok"
            )
    elif col_type == "string":
        length = props["length"]
        result[column] = "".join(random.choices(string.ascii_letters, k=length))

    return result


async def generate_row_data(data_describe, include_quality: bool = False):
    """Generate a single row of data."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    device_id = data_describe["device_id"]["value"]

    columns = [column for column in data_describe if column not in ["timestamp", "device_id"]]
    tasks = [get_column_data(column, data_describe[column], include_quality) for column in columns]
    results = await asyncio.gather(*tasks)

    row = {"timestamp": timestamp, "device_id": device_id}
    for result in results:
        if result:
            row.update(result)

    return row


def run_opcua_server(describe_data_file, port, rows, include_quality: bool = False):
    data_describe = read_description(describe_data_file)

    # Create an instance of the Server
    server = Server()

    # Set endpoint with configurable port and hostname
    server.set_endpoint(f"opc.tcp://{HOST}:{port}/DummyOPCUA")

    # Setup server namespace and register one for each table
    server.set_server_name("Point-Based OPC UA Server")
    table_namespaces = {table_name: server.register_namespace(table_name) for table_name in data_describe.keys()}

    # Create a new object for each table
    objects = server.nodes.objects
    table_objects = {}
    table_variables = {}

    for table_name, ns_idx in table_namespaces.items():
        table_obj = objects.add_object(ns_idx, f"{table_name}")
        table_objects[table_name] = table_obj
        table_variables[table_name] = {}

        for column, props in data_describe[table_name].items():
            if "type" not in props:
                continue  # Skip columns without a 'type' key

            col_type = props["type"]
            initial_value = None
            table_variables[table_name][column] = table_obj.add_variable(ns_idx, column, initial_value)
            table_variables[table_name][column].set_writable()

    # Start the server
    server.start()
    print(f"Server started at {server.endpoint}")

    async def update_data():
        row_count = 0  # To count the total number of rows generated
        start_time = time.time()  # Record the start time

        while True:
            for table_name, table_desc in data_describe.items():
                row_data = await generate_row_data(table_desc, include_quality)

                # Update each variable
                for column, value in row_data.items():
                    if column in table_variables[table_name]:
                        table_variables[table_name][column].set_value(value)

                row_count += 1  # Increment the row count for each generated row

            # Log rows processed every second
            elapsed_time = time.time() - start_time
            if elapsed_time >= 60:  # Every second
                print(f"Rows processed in the last minute: {row_count}")
                row_count = 0  # Reset the row counter
                start_time = time.time()  # Reset the timer

            await asyncio.sleep(1 / rows)  # Update at the specified rate

    try:
        asyncio.run(update_data())
    finally:
        server.stop()
        print("Server stopped.")


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("--opcua-port", type=int, default=4840, help="OPC-UA server port")
    parse.add_argument(
        "--describe-data-file",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "opcua_describe_data.json"),
        help="File describing data",
    )
    parse.add_argument(
        "--describe-data", type=bool, nargs="?", const=True, default=False, help="Generate describe data"
    )
    parse.add_argument("--num-tables", type=__check_num, default=5, help="Number of tables in describe data")
    parse.add_argument("--num-columns", type=__check_num, default=100, help="Number of columns per table")
    parse.add_argument("--num-rows", type=__check_num, default=25, help="Number of rows per second per table")
    parse.add_argument(
        "--quality", type=bool, nargs="?", const=True, default=False, help="Include quality per data"
    )
    args = parse.parse_args()

    # Generate or get describe data
    args.describe_data_file = os.path.expanduser(os.path.expandvars(args.describe_data_file))
    if args.describe_data:
        describe_data(
            describe_data_file=args.describe_data_file,
            num_tables=args.num_tables,
            num_columns=args.num_columns,
            include_quality=args.quality,
        )
    elif not os.path.isfile(args.describe_data_file):
        raise FileNotFoundError(f"Failed to locate {args.describe_data_file}")

    run_opcua_server(
        describe_data_file=args.describe_data_file,
        port=args.opcua_port,
        rows=args.num_rows,
        include_quality=args.quality,
    )


if __name__ == "__main__":
    main()
