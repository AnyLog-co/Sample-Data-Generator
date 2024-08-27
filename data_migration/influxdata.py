"""
Process:
1. get data (in general) - done
2. get data in 5 minute interval - done
3. mapping
4. send to AnyLog
"""

import datetime
import json
from influxdb_client import InfluxDBClient
import time

import requests

# Your InfluxDB information
URL = "https://us-central1-1.gcp.cloud2.influxdata.com"
TOKEN = "Rx494c_v3EPx5UCnDdBJGe4ENLEKwWjsuq4eQnqBHT1MxenQrXLRBOUEGGL8PFhGa5kjfF8LkL_JeVxKBO_ecw=="
ORG = "376aed6cc475571d"
BUCKET = "csobsidian's Bucket"

CONNS = {
    "wp_digital": '172.105.60.50:32149',
    "wp_analog": '172.105.60.50:32149',
    "pp_pm": '172.105.6.90:32149'
}


def send_data(table_name:str, payload):
    headers = {
        'type': 'json',
        'dbms': 'cos',
        'table': table_name,
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.put(url=f"http://{CONNS[table_name]}", headers=headers, data=payload, auth=(), timeout=30)
    except Exception as error:
        print(f"{table_name} - failed to put data (Error: {error})")
    else:
        if int(r.status_code) >= 200 and int(r.status_code) < 300:
            print(f"{table_name} - success")
        else:
            print(f"{table_name} - failed to put data (Error: {r.status_code})")


def connect():
    # Initialize the InfluxDB client
    query_api = None
    try:
        client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
        query_api = client.query_api()
    except Exception as error:
        print(f"Failed to connect against {URL} (Error: {error})")
    return client, query_api


def disconnect(client:InfluxDBClient):
    # close connection
    try:
        client.close()
    except Exception as error:
        print(f"Failed to close connection against {URL} (Error: {error})")


def map_data_to_schema(data):
    """
    This function maps the raw InfluxDB data to the AnyLog schema based on the specified mapping logic.
    """
    mapped_data = {
        "wp_digital": [],
        "wp_analog": [],
        "pp_pm": []
    }

    def set_timestamp_index(map_data:list, timestamp:str):
        index = -1
        if len(map_data) == 0:
            map_data.append({'timestamp': timestamp})
            index = 0
        else:
            for i in range(len(map_data)):
                if timestamp == map_data[i]:
                    index = i

        return index, map_data

    def set_value(value:float):
        bool_value = True
        if value == 0.0:
            bool_value = False
        return bool_value

    for record in data:
        measurement = record["measurement"]
        field = record["field"]
        value = record['value']
        timestamp = record['time'].strftime('%Y-%m-%d %H:%M:%S.%f')


        table_name = 'wp_analog'
        if measurement in ['transferSwitch', 'generator', 'oxygenMonitor', 'plantStatus', 'servicePump', 'clearWell'] or (measurement == 'chlorinator' and field == 'Vac') or (measurement == 'watertower' and field == 'CommsStatus') or (measurement == 'carbonFeed' and field != 'Speed'):
            table_name = 'wp_digital'
            value = set_value(value)
        elif measurement == 'powerMonitors':
            table_name = 'pp_pm'

        index, mapped_data[table_name] = set_timestamp_index(map_data=mapped_data[table_name], timestamp=timestamp)

        if measurement == 'chlorinator':
            if field == 'Vac' and 'combinedchlorinatorvacdi' not in mapped_data[table_name][index]:
                mapped_data[table_name][index]['combinedchlorinatorvacdi'] = value
            elif field == 'Vac':
                mapped_data[table_name][index]['freechlorinatorvacdi'] = value
            elif field == 'PPM' and 'combinedchlorinatorai_pv' not in mapped_data[table_name][index]:
                mapped_data[table_name][index]['combinedchlorinatorai_pv'] = value
            elif field == 'PPM':
                mapped_data[table_name][index]['freechlorinatorai_pv'] = value

        elif measurement == 'watertower':
            if field == 'Level':
                mapped_data[table_name][index]['watertowerlevelai_pv'] = value
            elif field == 'CommsStatus':
                mapped_data[table_name][index]['watertowerlevelcommsdi'] = value

        elif measurement == 'carbonFeed':
            if isinstance(value, bool):
                mapped_data[table_name][index]['carbonfeeder_runningfwd'] = value
            else:
                mapped_data[table_name][index]['carbonfeeder_speedai_pv'] = value
        # water - digital
        elif measurement in ['transferSwitch', 'generator', 'oxygenMonitor', 'plantStatus', 'servicePump', 'clearWell']:
            if measurement == 'transferSwitch' and field == "NormalReady":
                mapped_data[table_name][index]['atsnormalrdydi'] = value
            elif measurement == 'transferSwitch' and field == "StandbyReady":
                mapped_data[table_name][index]['atsstandybyrdydi'] = value
            elif measurement == 'transferSwitch' and field == "OnStandby":
                mapped_data[table_name][index]['atsonstandbydi'] = value

            elif measurement == 'generator' and field == "Alarm":
                mapped_data[table_name][index]['generatoralarmdi'] = value
            elif measurement == 'generator' and field == "Running":
                mapped_data[table_name][index]['generatorstatusdi'] = value

            elif measurement == 'oxygenMonitor' and field == "Alarm":
                mapped_data[table_name][index]['oxygenmonitordi'] = value

            elif measurement == 'plantStatus' and field == "Running":
                mapped_data[table_name][index]['plantrunningdi'] = value

            elif measurement == 'plantStatus' and field == "Starting":
                mapped_data[table_name][index]['plantstartdi'] = value
            elif measurement == 'plantStatus' and field == "ShutdownCommand":
                mapped_data[table_name][index]['plantshutdowndo'] = value
            elif measurement == 'plantStatus' and field == "EnableChemicalsCommand":
                mapped_data[table_name][index]['plantenablechemicalsdo'] = value

            elif measurement == "servicePump" and field == "Running":
                if 'servicepump1running_di' in mapped_data[table_name][index]:
                    mapped_data[table_name][index]['servicepump2running_di'] = value
                else:
                    mapped_data[table_name][index]['servicepump1running_di'] = value

            elif measurement == "clearWell" and field == "HighLevel":
                mapped_data[table_name][index]['clearwellhighleveldi'] = value
            elif measurement == "clearWell" and field == "LowLevel":
                    mapped_data[table_name][index]['clearwelllowleveldi'] = value

        # water - analog
        elif measurement in ['waterMeter', 'turbidity', 'chemicalScale', 'ph']:
            if measurement == 'waterMeter' and field == "Flow":
                mapped_data[table_name][index]['rawwatermeterai_pv'] = value
            elif measurement == 'waterMeter' and field == "TotalToday":
                mapped_data[table_name][index]['rawwatermetertotalizer_curday'] = value
            elif measurement == 'waterMeter' and field == "TotalYesterday":
                mapped_data[table_name][index]['rawwatermetertotalizer_yesday'] = value

            elif measurement == "turbidity" and field == "Combined":
                mapped_data[table_name][index]['combinedturbidityai_pv'] = value
            elif measurement == "turbidity" and field == "Filter1":
                mapped_data[table_name][index]['filter1turbidityai_pv'] = value
            elif measurement == "turbidity" and field == "Filter2":
                mapped_data[table_name][index]['filter2turbidityai_pv'] = value
            elif measurement == "turbidity" and field == "Filter3":
                mapped_data[table_name][index]['filter3turbidityai_pv'] = value

            elif measurement == "chemicalScale" and field == "Weight":
                if 'chemicalscale1ai_pv' not in mapped_data[table_name][index]:
                    mapped_data[table_name][index]['chemicalscale1ai_pv'] = value
                elif 'chemicalscale2ai_pv' not in mapped_data[table_name][index]:
                    mapped_data[table_name][index]['chemicalscale2ai_pv'] = value
                elif 'chemicalscale3ai_pv' not in mapped_data[table_name][index]:
                    mapped_data[table_name][index]['chemicalscale3ai_pv'] = value
                elif 'chemicalscale4ai_pv' not in mapped_data[table_name][index]:
                    mapped_data[table_name][index]['chemicalscale4ai_pv'] = value
            elif measurement == 'ph':
                mapped_data[table_name][index]['phai_pv'] = value
        elif measurement == 'powerMonitors':
            mapping = {
                "CommsStatus": "commsstatus",
                "A_NeutralVoltage": "a_n_voltage",
                "B_NeutralVoltage": "b_n_voltage",
                "C_NeutralVoltage": "c_n_voltage",
                "A_Current": "a_current",
                "B_Current": "b_current",
                "C_Current": "c_current",
                "Frequency": "frequency",
                "PowerFactor": "powerfactor",
                "ReactivePower": "reactivepower",
                "EnergyMultiplier": "energymultiplier",
                "RealPower": "realpower"

            }
            if field == 'CommsStatus':
                mapped_data[table_name][index][mapping[field]] = set_value(value)
            else:
                mapped_data[table_name][index][mapping[field]] = value


    return mapped_data


def query_data(query: str, query_api: InfluxDBClient.query_api):
    try:
        results = query_api.query(query)
        all_data = []

        for result in results:
            for record in result.records:
                record_dict = {
                    "time": record.get_time(),
                    "measurement": record.get_measurement(),
                    "field": record.get_field(),
                    "value": record.get_value(),
                    "tags": record.values.get('tags', {}),
                }
                all_data.append(record_dict)

        if len(all_data) > 0:
            mapped_data = map_data_to_schema(all_data)
            for entry in mapped_data:
                if mapped_data[entry]:
                    for row in mapped_data[entry]:
                        send_data(table_name=entry, payload=json.dumps(row))
                # print(entry, json.dumps(sorted(mapped_data[entry]), indent=2))  # You can send this to AnyLog instead of printing
            # if len(mapped_data['wp_analog']) > 0 and len(mapped_data['wp_digital']) > 0 and len(mapped_data['pp_pm']) > 0:
            #     exit(1)
    except Exception as error:
        print(f"Failed to get results for query {query} against {URL} (Error: {error})")
        exit(1)


def main():
    conn, cur = connect()
    final_timestamp = datetime.datetime.now()
    min_timestamp = '2024-08-03T08:00:00Z' # datetime.datetime.now() - datetime.timedelta(days=31)
    min_timestamp = datetime.datetime.strptime(min_timestamp, '%Y-%m-%dT%H:%M:%SZ')

    while min_timestamp < final_timestamp:
        max_timestamp = min_timestamp + datetime.timedelta(hours=1)
        if min_timestamp.date() != max_timestamp.date():
            time.sleep(30)
        min_ts = min_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        max_ts = max_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        query = f'''from(bucket: "{BUCKET}")
        |> range(start: {min_ts}, stop: {max_ts})
        '''
        print(f"Min Timestamp: {min_ts} | Max Timestamp: {max_ts}")
        query_data(query=query, query_api=cur)
        min_timestamp = max_timestamp

    disconnect(client=conn)


if __name__ == '__main__':
    main()
