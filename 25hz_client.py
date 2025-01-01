from opcua import Client
import json
import time


def run_opcua_client():
    # Connect to the server
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")

    try:
        client.connect()
        print("Client connected to server.")

        # Access the root node and list all namespaces
        namespaces = client.get_namespace_array()
        root = client.get_root_node()
        objects = root.get_child(["0:Objects"])

        # Fetch data from each table namespace
        while True:
            all_data = {}
            for ns_idx, table_name in enumerate(namespaces):
                if "http://" in table_name:  # Skip default namespaces
                    continue

                # Access the table object and its data variable
                try:
                    table_object = objects.get_child([f"{ns_idx}:{table_name}Data"])
                    data_var = table_object.get_child([f"{ns_idx}:DataVariable"])
                    table_data = json.loads(data_var.get_value())

                    all_data[table_name] = table_data
                except Exception as e:
                    print(f"Error fetching data for {table_name}: {e}")

            # Print the data for all tables
            print(json.dumps(all_data, indent=4))

            time.sleep(1)  # Fetch data every second

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.disconnect()
        print("Client disconnected.")


if __name__ == "__main__":
    run_opcua_client()
