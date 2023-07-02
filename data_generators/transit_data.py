import ast
import random

import geopy
import json
import os
import sys
import requests

DIR_PATH = os.path.join(os.path.expanduser(os.path.expandvars(__file__)).split("data_generators")[0], "publishing_protocols")
sys.path.insert(0, DIR_PATH)
from publishing_protocols.rest_protocols import NETWORK_ERRORS, NETWORK_ERRORS_GENERIC

GEOLOCATOR = geopy.Nominatim(user_agent="transit-app")

def __request_data(url:str, exception:bool=True):
    """
    Get data based on a given  URL
    :args:
    """
    try:
        r = requests.get(url=url, headers=None)
    except Exception as error:
        r = None
        if exception is True:
            print(f"Failed to get data from {url} (Error: {error})")
    else:
        status_code = int(r.status_code)
        if status_code != 200:
            r = None
            if exception is True:
                error_msg = f"Failed to execute GET for {url} (Network Error: {status_code} - %s)"
                if status_code in NETWORK_ERRORS:
                    error_msg = error_msg % NETWORK_ERRORS[status_code]
                elif int(str(status_code)[0]) in NETWORK_ERRORS_GENERIC:
                    error_msg = error_msg % NETWORK_ERRORS_GENERIC[int(str(status_code)[0])]
                else:
                    error_msg.replace(" %s)", ")")
                print(error_msg)

    return r

def __get_location(latitude:float, longitude:float)->(str, tuple):
    """
    based on lat / long get location of vehicle
    :args:
        latitude:float - latitude coordinate
        longitude:float - longitude coordinates
    :params:
        coordinates:tuple - coordinates in tuple form
        location:str - address
    :return:
        location, coordinates
    """
    coordinates = (latitude, longitude)
    location = GEOLOCATOR.reverse(coordinates, exactly_one=True)
    return str(location), coordinates

def vehicle_position(license_key:str, transit_code:str, transit_agency:str, db_name:str, table_name:str, batch_size:int,
                     exception:bool=False):
    url = f"https://api.511.org/transit/vehiclepositions?api_key={license_key}&agency={transit_code}&format=json"
    output = __request_data(url=url, exception=exception)
    readings = []
    if output is not None:
        output = json.loads(output.content.decode("utf-8-sig"))
        vehicle = {
            "dbms": db_name,
            "table": table_name,
            "timestamp": output["Header"]["Timestamp"],
            "agency": transit_agency,
            "vehicle": "",
            "license_plate": "",
            "address": "",
            "location": "",
            "bearing": 0,
            "speed": 0
        }

        random.shuffle(output["Entities"])

        for row in output["Entities"]:
            if "Id" in row:
                vehicle["vehicle"] = row["Id"]
            if "Vehicle" in row:
                if "LicensePlate" in row["Vehicle"]:
                    vehicle["license_plate"] = row["Vehicle"]["LicensePlate"]
                if "Position" in row["Vehicle"]:
                    if "Latitude" in row["Vehicle"]["Position"] and "Longitude" in row["Vehicle"]["Position"]:

                        vehicle["address"], vehicle["location"] = __get_location(latitude=row["Vehicle"]["Position"]["Latitude"],
                                                                                 longitude=row["Vehicle"]["Position"]["Longitude"])
                    if "Bearing" in row["Vehicle"]["Position"]:
                        vehicle["bearing"] = row["Vehicle"]["Position"]["Bearing"]
                    if "Speed" in row["Vehicle"]["Position"]:
                        vehicle["speed"] = row["Vehicle"]["Position"]["Speed"]

            readings.append(vehicle)
            if len(readings) == batch_size:
                return readings

    return readings




