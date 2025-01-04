from flask import Flask, jsonify, request
from data_generator.rand_data import data_generator as rand_data
from data_generator.ping_percentagecpu import ping_sensor, percentagecpu_sensor
from data_generator.modified_atmosphere_packaging_machine import r_50

app = Flask(__name__)

global DB_NAME

def generate_data(data_generator:str, db_name:str):
    """
    Generate payload data based on the specified data generator type.

    :param data_generator: The type of data generator (e.g., 'ping', 'percentagecpu', 'rand', 'r_50').
    :param db_name: The name of the database.
    :return: The generated payload data.
    :raises ValueError: If an unsupported data generator is specified.
    """
    if data_generator == 'ping':
        return ping_sensor(db_name=DB_NAME)
    elif data_generator == 'percentagecpu':
        return percentagecpu_sensor(db_name=DB_NAME)
    elif data_generator == 'rand':
        return rand_data(db_name=DB_NAME)
    elif data_generator == 'r_50':
        payload = r_50()
        payload['dbms'] = DB_NAME
        return payload
    else:
        raise ValueError(f"Unsupported data generator: {data_generator}")

@app.route('/simulated_data/<device_type>', methods=['GET'])
def get_simulated_data(device_type):
    """
    Endpoint to retrieve simulated data for the specified device type.

    :param device_type: The type of device to simulate.
    :return: JSON response with the simulated data or an error message.
    """
    db_name = request.args.get('db_name', DB_NAME)
    try:
        payload = generate_data(data_generator=device_type, db_name=DB_NAME)
        return jsonify(payload), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def rest_server(host:str ='0.0.0.0', port: int = 8481, debug: bool = False):
    """
    Start the REST server with the specified configuration.

    :param host: The host address for the server (default: '0.0.0.0').
    :param port: The port for the server (default: 8481).
    :param debug: Whether to run the server in debug mode (default: False).
    """
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    # Start the server
    DB_NAME = "ori"
    rest_server(host='0.0.0.0', port=8481, debug=True)
