import asyncio
import opcua
import time

from data_generator.configuration_based_data import configuration_data, large_data
from data_generator.rand_data import data_generator as rand_data
from data_generator.ping_percentagecpu import ping_sensor, percentagecpu_sensor
from data_generator.modified_atmosphere_packaging_machine import r_50

SERVER = '127.0.0.1'
PORT = 4840

NAMESPACES = {
    2: "large",
    3: "network",
    4: "rand",
    5: "r_50"
}


async def generate_data(hostname: int, db_name: str):
    """
    Generate payload data based on the specified data generator type.

    :param hostname: The type of data generator (e.g., 2 for 'large', 3 for 'ping', etc.)
    :param db_name: The name of the database.
    :return: The generated payload data.
    :raises ValueError: If an unsupported data generator is specified.
    """
    payload = {}
    if hostname == 2:
        # Schedule configuration_data to run in a separate thread
        """
         <get opcua struct where 
            url=opc.tcp://127.0.0.1:4840/freeopcua/data-generator and 
            node="ns=2;i=[TABLE_ID - 1, 2...]" and 
            class = variable and
            format = get_value and 
            validate=true>         
        """
        data = await configuration_data()
        payload = large_data(data=data, db_name=db_name)
        del payload['dbms']
    elif hostname == 3:
        """
         <get opcua struct where 
            url=opc.tcp://127.0.0.1:4840/freeopcua/data-generator and 
            node="ns=3;i=[1 OR 2]" and 
            class = variable and
            format = get_value and 
            validate=true>         
        """
        ping = ping_sensor(db_name=db_name)
        percentagecpu = percentagecpu_sensor(db_name=db_name)
        for param in ['dbms', 'table']:
            del ping[param]
            del percentagecpu[param]
        payload = {
            "ping_sensor": ping,
            'percentagecpu_sensor': percentagecpu
        }
    elif hostname == 4:
        """
         <get opcua struct where 
            url=opc.tcp://127.0.0.1:4840/freeopcua/data-generator and 
            node="ns=4;i=1" and 
            class = variable and
            format = get_value and 
            validate=true>         
        """
        rand = rand_data(db_name=db_name)
        for param in ['dbms', 'table']:
            del rand[param]
        payload['rand_data'] = rand
    elif hostname == 5:
        """
         <get opcua struct where 
            url=opc.tcp://127.0.0.1:4840/freeopcua/data-generator and 
            node="ns=5;i=1" and 
            class = variable and
            format = get_value and 
            validate=true>         
        """
        r50 = r_50()
        del r50['table']
        payload['r_50'] = r50
    else:
        raise ValueError(f"Unsupported data generator: {hostname}")

    # Log the payload to inspect its structure
    # print(f"Generated data for hostname {hostname}: {payload}")

    return payload


async def run_opcua_server(sleep_rate: float, db_name: str, port: int = PORT):
    server = None
    is_connected = False
    sleep_rate = 1 / sleep_rate if sleep_rate > 0 else 1
    try:
        server = opcua.Server()
        server.set_endpoint(url=f'opc.tcp://{SERVER}:{port}/freeopcua/data-generator')
        print(server)

        # Register namespaces in the OPC-UA server
        namespace_idx = {}
        for ns_id, ns_name in NAMESPACES.items():
            namespace_idx[ns_id] = server.register_namespace(ns_name)

        objects = server.nodes.objects

        # Initialize a dictionary to store the created variables for updating
        created_variables = {}

        print("Adding tables to the address space:")

        # Generate and add data for each namespace
        for ns_id, ns_name in NAMESPACES.items():
            payload = await generate_data(hostname=ns_id, db_name=db_name)
            # del payload['dbms']  # Ensure payload does not contain unnecessary keys

            # Register the namespace and add data for each table in the namespace
            idx = namespace_idx[ns_id]
            for table_name, rows in payload.items():
                # Log the structure of each table's rows before processing
                print(f"  Processing table: {table_name}, rows: {rows}")

                # Ensure rows is either a list or a single dictionary
                if isinstance(rows, dict):
                    rows = [rows]  # Wrap single dictionary in a list
                elif not isinstance(rows, list):
                    raise ValueError(f"Expected rows for {table_name} to be a list or dict, but got {type(rows).__name__} | {rows}")

                # Add table object
                table_obj = objects.add_object(idx, table_name)
                print(f"  Added Object: {table_name} with NodeId: ns={idx};s={table_name}")

                for i, row in enumerate(rows):
                    if not isinstance(row, dict):
                        raise ValueError(f"Expected row to be a dictionary, but got {type(row).__name__}")

                    for col_name, value in row.items():
                        # Create a unique NodeId using table name, column name, and row index
                        unique_node_id = f"{table_name}_{col_name}"
                        # unique_node_id = f"{table_name}_{col_name}_{i}"
                        var = table_obj.add_variable(opcua.ua.NodeId(unique_node_id, idx), col_name, value)
                        var.set_writable()  # Allow clients to write values
                        print(f"    Added Variable: {col_name} with NodeId: ns={idx};s={unique_node_id}")

                        # Store the variable for future updates
                        if table_name not in created_variables:
                            created_variables[table_name] = {}
                        created_variables[table_name][(i, col_name)] = var

        # Start the server
        server.start()
        is_connected = True
        print("Server started. Press Ctrl+C to stop.")

        while True:
            # Fetch new data and update the variables periodically for each namespace
            for ns_id, ns_name in NAMESPACES.items():
                new_payload = await generate_data(hostname=ns_id, db_name=db_name)
                # del new_payload['dbms']  # Ensure payload does not contain unnecessary keys

                # Update variables with new data
                idx = namespace_idx[ns_id]
                for table_name, rows in new_payload.items():
                    if isinstance(rows, dict):
                        rows = [rows]  # Wrap single dictionary in a list
                    for i, row in enumerate(rows):
                        for col_name, value in row.items():
                            if (i, col_name) in created_variables.get(table_name, {}):
                                # Update the existing variable with the new value
                                var = created_variables[table_name][(i, col_name)]
                                var.set_value(value)
                                print(f"Updated Variable: {col_name} with NodeId: ns={idx};s={table_name}_{col_name}_{i}")

            # Wait for the next update (e.g., every 2 seconds)
            time.sleep(sleep_rate)

    except KeyboardInterrupt:
        print("Shutting down server...")
    except Exception as error:
        print(f"Failed to connect to OPC-UA against {SERVER}:{port} (Error: {error})")
        raise
    finally:
        if server and is_connected is True:
            server.stop()


if __name__ == '__main__':
    asyncio.run(run_opcua_server(sleep_rate=2, db_name='test'))
