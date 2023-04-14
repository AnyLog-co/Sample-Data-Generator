import ast
import datetime
import json
import os
import sys
import requests

DIR_PATH = os.path.join(os.path.expanduser(os.path.expandvars(__file__)).split("data_generators")[0], "publishing_protocols")
sys.path.insert(0, DIR_PATH)
from publishing_protocols.rest_protocols import NETWORK_ERRORS, NETWORK_ERRORS_GENERIC


DIRECTIONS = {
    "N": "North",
    "E": "East",
    "S": "South",
    "W": "West"
}

TRANSIT_AGENCIES = {
    "3D": "Tri Delta Transit",
    "AC": "AC TRANSIT",
    "AF": "Angel Island Tiburon Ferry",
    "AM": "Capitol Corridor Joint Powers Authority",
    "BA": "Bay Area Rapid Transit",
    "CC": "County Connection",
    "CE": "Altamont Corridor Express",
    "CM": "Commute.org Shuttles",
    "CT": "Caltrain",
    "DE": "Dumbarton Express Consortium",
    "EM": "Emery Go-Round",
    "FS": "FAST",
    "GF": "Golden Gate Ferry",
    "GG": "Golden Gate Transit",
    "MA": "Marin Transit",
    "MB": "Mission Bay TMA",
    "MV": "MVgo Mountain View",
    "PE": "Petaluma Transit",
    "RG": "Regional GTFS",
    "RV": "Rio Vista Delta Breeze",
    "SA": "Sonoma Marin Area Rail Transit",
    "SB": "San Francisco Bay Ferry",
    "SC": "VTA",
    "SF": "San Francisco Municipal Transportation Agency",
    "SI": "San Francisco International Airport",
    "SM": "SamTrans",
    "SO": "Sonoma County Transit",
    "SR": "Santa Rosa CityBus",
    "SS": "City of South San Francisco",
    "ST": "SolTrans",
    "TD": "Tideline Water Taxi",
    "TF": "Treasure Island Ferry",
    "UC": "Union City Transit",
    "VC": "Vacaville City Coach",
    "VN": "VINE Transit",
    "WC": "WestCat (Western Contra Costa)",
    "WH": "Livermore Amador Valley Transit Authority"
}

LICENSE_KEY = "efe23758-318f-4e2c-b147-ab63cde78549"


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


def list_service_providers(exception:bool=False):
    """
    Get a list of available public transit providers
    :params:
        transit_companies:dict - list of transit companies and their code
        url:str - URL to get results from
        output - content from GET request
    :return:
        transit_companies
    """
    transit_companies = {}
    url = f"http://api.511.org/transit/gtfsoperators?api_key={LICENSE_KEY}"
    output = __request_data(url=url, exception=exception)
    if output is not None:
        for row in ast.literal_eval(output.content.decode('utf-8-sig')):
            transit_companies[row['Id']] = row['Name']

        return json.dumps(transit_companies, indent=4)


def get_vehicle_position(agency:str, bus_line:int=22, exception:bool=False):
    """
    Based on agency and bus line number get information
    :args:
        agency:str - agency name
        bus_line:str - bus number
        exception:bool - whether to print exceptions
    :params;
        
    """ 
    data = []
    content = []
    url = f"http://api.511.org/transit/VehicleMonitoring?api_key={LICENSE_KEY}&format=json"
    if agency is not None and agency in TRANSIT_AGENCIES:
        url += f"&agency={agency}"

    output = __request_data(url=url, exception=exception)

    if output is not None:
        try:
            content = json.loads(output.content.decode('utf-8-sig'))
        except Exception as error:
            if exception is True:
                print(f"Failed to convert content to be useable (Error: {error})")
    if content is not []:
        try:
            content=content['Siri']['ServiceDelivery']['VehicleMonitoringDelivery']['VehicleActivity']
        except Exception as error:
            content = []
            if exception is True:
                pint(f"Failed to extract content (Error: {error})")

    for row in content:
        try:
            line_ref = int(row['MonitoredVehicleJourney']['LineRef'])
        except ValueError:
            line_ref = row['MonitoredVehicleJourney']['LineRef']
        except Exception:
            line_ref = None

        if line_ref == bus_line:
            new_row = {
                "operator": TRANSIT_AGENCIES[agency],
                "timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%s.%fZ'),
                "line": line_ref
            }

            if "PublishedLineName" in row["MonitoredVehicleJourney"]:
                new_row["name"] = row['MonitoredVehicleJourney']["PublishedLineName"]
            if "VehicleRef" in row["MonitoredVehicleJourney"]:
                try:
                    new_row["vehicle_ref"] = int(row["MonitoredVehicleJourney"]["VehicleRef"])
                except:
                    new_row["vehicle_ref"] = row["MonitoredVehicleJourney"]["VehicleRef"]
            if "OriginName" in row["MonitoredVehicleJourney"]:
                new_row["origin"] = row["MonitoredVehicleJourney"]["OriginName"]
            if "DestinationName" in row["MonitoredVehicleJourney"]:
                new_row["destination"] = row["MonitoredVehicleJourney"]["DestinationName"]
            if "InCongestion" in row["MonitoredVehicleJourney"]:
                new_row["in_traffic"] = False
                if row["MonitoredVehicleJourney"]["InCongestion"] is not None and row["MonitoredVehicleJourney"]["InCongestion"] is not False:
                    new_row["in_traffic"] = True
            if 'DirectionRef' in row["MonitoredVehicleJourney"]:
                try:
                    new_row['direction'] = DIRECTIONS[row["MonitoredVehicleJourney"]["DirectionRef"]]
                except Exception:
                    new_row['direction'] = row["MonitoredVehicleJourney"]["DirectionRef"]
            if "VehicleLocation" in row["MonitoredVehicleJourney"]:
                location = row["MonitoredVehicleJourney"]['VehicleLocation']
                if "Longitude" in location and "Latitude" in location:
                    new_row['location'] = f'{float(location["Longitude"])}, {float(location["Latitude"])}'
                else:
                    new_row['location'] = location
            if "Occupancy" in row["MonitoredVehicleJourney"]:
                if row["MonitoredVehicleJourney"]["Occupancy"] is None:
                    new_row["occupancy"] = "seatsAvailable"
                else:
                    new_row["occupancy"] = row["MonitoredVehicleJourney"]["Occupancy"]
            data.append(new_row)

    return data
