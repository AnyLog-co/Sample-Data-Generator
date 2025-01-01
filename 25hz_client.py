from opcua import Client
import json
import time


def run_opcua_client():
    # Connect to the server
    server_url = "opc.tcp://10.0.0.228:4840/freeopcua/server/"
    client = Client(server_url)

    try:
        client.connect()
        print(f"Client connected to server at {server_url}.")

        # Access the root node
        root = client.get_root_node()
        print("Root node:", root)

        # Specify the namespace and node ID
        namespace_index = 2
        node_id = f"ns={namespace_index};i=2"

        # Create the Node object
        node = client.get_node(node_id)
        print(f"Accessing node: {node_id}")

        # Continuously fetch data
        while True:
            try:
                # Get the value of the node
                value = node.get_value()
                print(json.loads(value))
                exit(1)
                print(f"Node value: {value}")
            except Exception as e:
                print(f"Error accessing node value: {e}")

            time.sleep(1)  # Fetch data every second

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.disconnect()
        print("Client disconnected.")


if __name__ == "__main__":
    run_opcua_client()
