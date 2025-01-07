import os
from opcua import Server
from data_generator.configuration_based_data import read_description, describe_data
from data_publisher.rest_server import generate_data

HOST = "0.0.0.0"  # Replace with your host IP or name

def run_opcua_server(describe_data_file, port, db_name:str, rows, include_quality:bool=False):
    data_describe = read_description(describe_data_file)

    # Create an instance of the Server
    server = Server()

    # Set endpoint with configurable port and hostname
    server.set_endpoint(f"opc.tcp://{HOST}:{port}/DummyOPCUA")

    # Setup server namespace and register one for each table
    server.set_server_name("Point-Based OPC UA Server")
    table_namespaces = {
        "large": {table_name: server.register_namespace(table_name) for table_name in data_describe.keys()},
        "networking": {table_name: server.register_namespace(table_name) for table_name in ['ping', 'percentagecpu']},
        "r_50": server.register_namespace('r_50'),
        "rand": server.register_namespace('rand'),
    }

    # Create a new object for each table
    objects = server.nodes.objects
    table_objects = {}
    table_variables = {}

    for category in table_namespaces:
        if category == 'large':
            payload = generate_data(data_generator=category, db_name=db_name)
            print(payload)
        elif category == 'networking':
            for namespace in list(table_namespaces[category].keys()):
                payload = generate_data(data_generator=namespace, db_name=db_name)
                print(payload)
        else:
            payload = generate_data(data_generator=category, db_name=db_name)
            print(payload)

if __name__ == '__main__':
    # describe_data(
    #     describe_data_file=os.path.join(os.path.dirname(__file__).strip('data_publisher'), "blobs", "opcua_describe_data.json"),
    #     num_tables=1,
    #     num_columns=5,
    #     include_quality=False
    # )

    run_opcua_server(
        describe_data_file=os.path.join(os.path.dirname(__file__).strip('data_publisher'), "blobs", "opcua_describe_data.json"),
        db_name='test',
        port=4840,
        rows=25,
        include_quality=False,
    )