import asyncio
from opcua import Server
from data_generator.configuration_based_data import configuration_data, opcua_serialize_data
from data_publisher.rest_server import generate_data

HOST = "0.0.0.0"  # Replace with your host IP or name


async def run_opcua_server(port: int, db_name: str, rows=1):
    # Create an instance of the Server
    server = Server()

    # Set endpoint with configurable port and hostname
    server.set_endpoint(f"opc.tcp://{HOST}:{port}/DummyOPCUA")
    server.set_server_name("Point-Based OPC UA Server")

    # Setup server namespaces
    namespaces = {
        "large": server.register_namespace("large"),
        "networking": server.register_namespace("networking"),
        "r_50": server.register_namespace("r_50"),
        "rand": server.register_namespace("rand"),
    }

    # Create the root object node
    objects = server.nodes.objects

    # Store OPC UA nodes and variables for updates
    category_nodes = {}
    variable_references = {}

    # Helper function to create or retrieve OPC UA nodes
    def get_or_create_object(parent_node, namespace_id, name):
        if name not in category_nodes:
            category_nodes[name] = parent_node.add_object(namespace_id, name)
        return category_nodes[name]

    async def update_data():
        for category, namespace_id in namespaces.items():
            # Get or create the root node for the category
            category_node = get_or_create_object(objects, namespace_id, category)

            if category == "large":
                # Handle "large" category
                data = await configuration_data()
                payload = opcua_serialize_data(data, db_name=db_name)
                for table_name, table_data in payload.items():
                    table_node = get_or_create_object(category_node, namespace_id, table_name)
                    for key, value in table_data.items():
                        variable = variable_references.get(key)
                        if variable:
                            variable.set_value(value)
                        else:
                            variable = table_node.add_variable(namespace_id, key, value)
                            variable.set_writable()
                            variable_references[key] = variable

            elif category == "networking":
                # Handle "networking" category
                for table_name in ['ping', 'percentagecpu']:
                    table_node = get_or_create_object(category_node, namespace_id, table_name)
                    data = generate_data(data_generator=table_name, db_name=db_name)
                    payload = {k: v for k, v in data.items() if k not in ['dbms', 'table']}
                    for key, value in payload.items():
                        variable = variable_references.get(key)
                        if variable:
                            variable.set_value(value)
                        else:
                            variable = table_node.add_variable(namespace_id, key, value)
                            variable.set_writable()
                            variable_references[key] = variable

            else:
                # Handle other categories
                data = generate_data(data_generator=category, db_name=db_name)
                payload = {k: v for k, v in data.items() if k not in ['dbms', 'table']}
                table_node = get_or_create_object(category_node, namespace_id, category)
                for key, value in payload.items():
                    variable = variable_references.get(key)
                    if variable:
                        variable.set_value(value)
                    else:
                        variable = table_node.add_variable(namespace_id, key, value)
                        variable.set_writable()
                        variable_references[key] = variable

    # Start the server
    try:
        server.start()
        print(f"Server started at {server.endpoint}")
        # Update data periodically
        while True:
            await update_data()
            await asyncio.sleep(1 / rows)
    finally:
        server.stop()
        print("Server stopped.")


if __name__ == '__main__':
    asyncio.run(run_opcua_server(port=4840, db_name="dummy_db", rows=1))
