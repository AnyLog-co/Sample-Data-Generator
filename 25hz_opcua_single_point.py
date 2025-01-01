import asyncio
import orjson
from opcua import Server
import random
from datetime import datetime
import json
import string  # For random string generation

DESCRIBE_DATA = "describe_data.json"
PORT = 4840  # Configurable port
HOST = "0.0.0.0"  # Replace with your host IP or name

def read_description():
    """Read the JSON description file."""
    with open(DESCRIBE_DATA, 'rb') as f:
        return orjson.loads(f.read())

async def get_column_data(column, props):
    """Generate data for a single column asynchronously."""
    if column in ['timestamp', 'device_id']:
        return None  # Skip timestamp and device_id

    col_type = props['type']
    result = {}

    if col_type == 'bool':
        result[column] = random.choice([True, False, None])
        result[f'quality_{column}'] = 'NOk' if result[column] is None else 'Ok'
    elif col_type in ['int', 'float']:
        value = round(random.uniform(props['min'], props['max']), 3)
        result[column] = int(value) if col_type == 'int' else value
        result[f'quality_{column}'] = 'Ok' if 0.75 * ((props['min'] + props['max']) / 2) <= value <= 1.25 * ((props['min'] + props['max']) / 2) else 'Nok'
    elif col_type == 'string':
        length = props['length']
        result[column] = ''.join(random.choices(string.ascii_letters, k=length))
        result[f'quality_{column}'] = 'Ok'

    return result

async def generate_table_data(data_describe, rows=25):
    """Generate multiple rows of data for a table."""
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    device_id = data_describe['device_id']['value']

    columns = [column for column in data_describe if column not in ['timestamp', 'device_id']]

    table_data = []
    for _ in range(rows):
        tasks = [get_column_data(column, data_describe[column]) for column in columns]
        results = await asyncio.gather(*tasks)

        row = {'timestamp': timestamp, 'device_id': device_id}
        for result in results:
            if result:
                row.update(result)

        table_data.append(row)

    return table_data

def run_opcua_server():
    data_describe = read_description()

    # Create an instance of the Server
    server = Server()

    # Set endpoint with configurable port and hostname
    server.set_endpoint(f"opc.tcp://{HOST}:{PORT}/DummyOPCUA")

    # Setup server namespace and register one for each table
    server.set_server_name("Table-Based OPC UA Server")
    table_namespaces = {table_name: server.register_namespace(table_name) for table_name in data_describe.keys()}

    # Create a new object for each table to hold variables
    objects = server.nodes.objects
    table_objects = {}
    for table_name, ns_idx in table_namespaces.items():
        table_objects[table_name] = objects.add_object(ns_idx, f"{table_name}")

    # Add a variable for each table
    table_variables = {
        table_name: table_objects[table_name].add_variable(ns_idx, "DataVariable", json.dumps([]))
        for table_name, ns_idx in table_namespaces.items()
    }
    for var in table_variables.values():
        var.set_writable()

    # Start the server
    server.start()
    print(f"Server started at {server.endpoint}")

    async def update_data():
        while True:
            for table_name, table_desc in data_describe.items():
                table_data = await generate_table_data(table_desc, rows=25)
                table_variables[table_name].set_value(json.dumps(table_data))
                # table_variables[table_name].set_value(table_data)

            await asyncio.sleep(1)  # Update every second

    try:
        asyncio.run(update_data())
    finally:
        server.stop()
        print("Server stopped.")

if __name__ == "__main__":
    run_opcua_server()
# get opcua values where url =opc.tcp://10.0.0.228:4840/freeopcua/server/ and node = "ns=2;i=2"
# run opcua client where url =opc.tcp://10.0.0.228:4840/freeopcua/server/ and node = "ns=2;i=2" and frequency=25 and dbms=nov and table=table_2
# get opcua values where url = opc.tcp://10.0.0.228:4840/freeopcua/server/ and node = "ns=2;i=2" and format=json