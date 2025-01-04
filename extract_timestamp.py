from opcua import Client

# Define the server URL and node
server_url = "opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer"

# "ns=3;i=1004"
def extract_values(node_id="ns=3;s=Sinusoid"):
    # connect to server
    try:
        client = Client(server_url)
        client.connect()
    except Exception as error:
        raise Exception(f'Failed to connect to OPC-UA against {server_url} (Error: {error})')
    else:
        print(f"Connected to OPC-UA server against {server_url}")

    def get_value():
        """
        Get value and source timestamp
        """
        try:
            node =  client.get_node(node_id)
            value_data = node.get_data_value()
        except Exception as error:
            raise Exception(f'Failed to extract node information from {server_url} (Error: {error})')
        else:
            browser_name = node.get_browse_name()
            value = value_data.Value.Value
            source_time = value_data.SourceTimestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
        print(f'Value: {value}')
        print(f'Source Time: {source_time}')

    def get_server_timestamp():
        """
        Get server timestamp
        """
        SERVER_TIME_NODE = "i=2258"  # Server.ServerStatus.CurrentTime

        try:
            server_time_node = client.get_node(SERVER_TIME_NODE)
            server_time = server_time_node.get_value()  # Fetch the server's current time
        except Exception as error:
            raise Exception(f'Failed to get server time from OPC-UA (Error: {error})')
        else:
            print(f"Server Time: {server_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")


    get_value()
    get_server_timestamp()

    try:
        client.disconnect()
    except Exception as error:
        raise Exception(f'Failed to discconect from OPC-UA (Error: {error})')
    else:
        print("Disconnected from OPC UA Server.")

if __name__ == '__main__':
    extract_values()

# # Server Time
# # Standard OPC UA node for server time
#   # Server.ServerStatus.CurrentTime
#
# # Connect to the OPC UA server
# client = Client(server_url)
# try:
#     client.connect()
#     print("Connected to OPC UA Server.")
#
#     # Access the Server's Current Time node
#
#
#     print(f"Server Time: {server_time}")
#
# finally:
#     client.disconnect()
#     print("Disconnected from OPC UA Server.")

