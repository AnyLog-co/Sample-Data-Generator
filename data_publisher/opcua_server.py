import asyncio
import time
from opcua import Server
from data_generator.configuration_based_data import read_description
from data_publisher.rest_server import generate_data
from data_generator.configuration_based_data import generate_row_data


def run_opcua_server(data_generator:str, port:int, db_name:str, describe_data_file:str, rows,
                     include_quality:bool=False, exception:bool=False):
    data_describe = read_description(describe_data_file)

    # Create an instance of the Server
    server = Server()
    server.set_endpoint(f"opc.tcp://localhost:{port}/DummyOPCUA")
    server.set_server_name("Point-Based OPC UA Server")

    # Register namespaces for tables
    table_namespaces = {table_name: server.register_namespace(table_name) for table_name in data_describe.keys()}
    objects = server.nodes.objects
    table_objects = {}
    table_variables = {}

    for table_name, ns_idx in table_namespaces.items():
        table_obj = objects.add_object(ns_idx, f"{table_name}")
        table_objects[table_name] = table_obj
        table_variables[table_name] = {}

        for column, props in data_describe[table_name].items():
            if "type" not in props:
                continue
            initial_value = None
            table_variables[table_name][column] = table_obj.add_variable(ns_idx, column, initial_value)
            table_variables[table_name][column].set_writable()

    server.start()
    print(f"Server started at {server.endpoint}")

    async def update_data(custom_generator=None, db_name:str=None):
        row_count = 0
        start_time = time.time()

        while True:
            for table_name, table_desc in data_describe.items():
                if custom_generator == 'large':
                    row_data = await generate_row_data(table_desc, include_quality)
                elif custom_generator:
                    row_data = generate_data(custom_generator, db_name=db_name)
                else:
                    row_data = {}
                    if exception is True:
                        raise ValueError(f'Invalid value {custom_generator}')

                for column, value in row_data.items():
                    if column in table_variables[table_name]:
                        table_variables[table_name][column].set_value(value)

                row_count += 1

            elapsed_time = time.time() - start_time
            if elapsed_time >= 60:
                print(f"Rows processed in the last minute: {row_count}")
                row_count = 0
                start_time = time.time()

            await asyncio.sleep(1 / rows)

    try:
        asyncio.run(update_data(custom_generator=data_generator, db_name=db_name))
    finally:
        server.stop()
        print("Server stopped.")
