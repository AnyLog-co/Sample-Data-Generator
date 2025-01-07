import asyncio

from flask import Flask, jsonify
from concurrent.futures import ThreadPoolExecutor

from data_generator.configuration_based_data import configuration_data,  opcua_serialize_data
from data_generator.rand_data import data_generator as rand_data
from data_generator.ping_percentagecpu import ping_sensor, percentagecpu_sensor
from data_generator.modified_atmosphere_packaging_machine import r_50

app = Flask(__name__)

executor = ThreadPoolExecutor()
# ROOT_PATH = os.path.expandvars(os.path.expanduser(__file__)).split("data_publisher")[0]
# PEOPLE_DIR  = os.path.join(ROOT_PATH, 'blobs', 'people_video')
# CAR_DIR  = os.path.join(ROOT_PATH, 'blobs', 'car_video')
# PEOPLE_DIR  = os.path.join(ROOT_PATH, 'blobs', 'factory_images')


def generate_data(data_generator:str, db_name:str):
    """
    Generate payload data based on the specified data generator type.

    :param data_generator: The type of data generator (e.g., 'ping', 'percentagecpu', 'rand', 'r_50').
    :param db_name: The name of the database.
    :return: The generated payload data.
    :raises ValueError: If an unsupported data generator is specified.
    """
    if data_generator == 'ping':
        payload = ping_sensor(db_name=db_name)
    elif data_generator == 'percentagecpu':
        payload = percentagecpu_sensor(db_name=db_name)
    elif data_generator == 'rand':
        payload = rand_data(db_name=db_name)
    elif data_generator == 'r_50':
        payload = r_50()
        payload['dbms'] = DB_NAME
    elif data_generator == 'large':
        # Schedule configuration_data to run in a separate thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            payload = loop.run_until_complete(configuration_data())
        finally:
            loop.close()
        payload = opcua_serialize_data(payload, db_name=db_name)
    else:
        payload = {}
        if EXCEPTION is True:
            raise ValueError(f"Unsupported data generator: {data_generator}")

    return payload


@app.route('/simulated_data/<data_type>', methods=['GET'])
def simulated_data(data_type):
    try:
        data = generate_data(data_type, db_name=DB_NAME)
        try:
            return jsonify(data)
        except TypeError:
            return jsonify(data['table_1'])
    except ValueError as e:
        if EXCEPTION is True:
            return jsonify({"error": str(e)}), 400


def main(db_name:str, service_port:int, exception:bool=False):
    global DB_NAME
    global EXCEPTION
    DB_NAME = db_name
    EXCEPTION = exception
    app.run(host='0.0.0.0', port=service_port, debug=True)

