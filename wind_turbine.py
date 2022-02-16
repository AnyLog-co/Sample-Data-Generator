"""
The following extracts Turbine data from USGS
:link:
    https://eerscmap.usgs.gov/uswtdb/api-doc/
:input:
{'case_id': 3072661, 'faa_ors': None, 'faa_asn': None, 'usgs_pr_id': 5149, 't_state': 'CA', 't_county': 'Kern County', 't_fips': '6029', 'p_name': '251 Wind', 'p_year': 1987, 'p_tnum': 194, 'p_cap': 18.43, 't_manu': 'Vestas', 't_model': None, 't_cap': 95, 't_hh': None, 't_rd': None, 't_rsa': None, 't_ttlh': None, 't_conf_atr': 2, 't_conf_loc': 3, 't_img_date': '5/8/2018', 't_img_srce': 'Digital Globe', 'xlong': -118.36376, 'ylat': 35.07791, 'eia_id': 52161, 'retrofit': 0, 'retrofit_year': None}
:output:
{'timestamp': '1987-02-16 10:56:01.632841', 'usgs_pr_id': 5149, 'address': 'Kern County, CA', 'loc': '35.07791, -118.36376', 'p_name': '251 Wind', 'p_tnum': 194, 'p_cap': 18.43, 't_manu': 'Vestas', 't_model': None, 't_cap': 95, 't_hh': None, 't_rd': None, 't_rsa': None, 't_ttlh': None, 'retrofit': 0, 't_conf_atr': 2, 't_conf_loc': 3, 'eia_id': 52161}
"""
import argparse
import datetime
import os
import requests
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, PROTOCOLS)


def generate_timestamp(year:str='now')->str:
    """
    Replace the current YEAR with the year provided by USGS, to generate a "current" timestamp value
    if set to "now", use current timestamp
    :args:
        year:str - year to use
        current_year:str - year from datetime.datetime.now()
    :return:
        timestamp with an updated year
    """
    if year == 'now':
        return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    current_year = datetime.datetime.now().year
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ').replace(f"{current_year}-", f"{year}-")


def generate_windturbine_data():
    """
    The following utilizes data from USGS to generate Wind Turbine data
    :sample-ouput:
        {"timestamp": "1987-02-16T11:22:56.025370Z", "usgs_pr_id": 5149, "address": "Kern County, CA", "loc": "35.07791, -118.36376", "p_name": "251 Wind", "p_tnum": 194, "p_cap": 18.43, "t_manu": "Vestas", "t_model": null, "t_cap": 95, "t_hh": null, "t_rd": null, "t_rsa": null, "t_ttlh": null, "retrofit": 0, "t_conf_atr": 2, "t_conf_loc": 3, "eia_id": 52161, "dbms": "test", "table": "wind_turbine"}
        {"timestamp": "1987-02-16T11:22:57.041407Z", "usgs_pr_id": 5143, "address": "Kern County, CA", "loc": "35.07744, -118.36441", "p_name": "251 Wind", "p_tnum": 194, "p_cap": 18.43, "t_manu": "Vestas", "t_model": null, "t_cap": 95, "t_hh": null, "t_rd": null, "t_rsa": null, "t_ttlh": null, "retrofit": 0, "t_conf_atr": 2, "t_conf_loc": 3, "eia_id": 52161, "dbms": "test", "table": "wind_turbine"}
        {"timestamp": "1987-02-16T11:22:58.042236Z", "usgs_pr_id": 5146, "address": "Kern County, CA", "loc": "35.07764, -118.3642", "p_name": "251 Wind", "p_tnum": 194, "p_cap": 18.43, "t_manu": "Vestas", "t_model": null, "t_cap": 95, "t_hh": null, "t_rd": null, "t_rsa": null, "t_ttlh": null, "retrofit": 0, "t_conf_atr": 2, "t_conf_loc": 3, "eia_id": 52161, "dbms": "test", "table": "wind_turbine"}
        {"timestamp": "2017-02-16T11:22:59.043143Z", "usgs_pr_id": null, "address": "Story County, IA", "loc": "42.02823, -93.43037", "p_name": "30 MW Iowa DG Portfolio", "p_tnum": 10, "p_cap": 30.0, "t_manu": "Nordex", "t_model": "AW125/3000", "t_cap": 3000, "t_hh": 87.5, "t_rd": 125.0, "t_rsa": 12271.85, "t_ttlh": 150.0, "retrofit": 0, "t_conf_atr": 3, "t_conf_loc": 3, "eia_id": null, "dbms": "test", "table": "wind_turbine"}
        {"timestamp": "2017-02-16T11:23:00.043226Z", "usgs_pr_id": null, "address": "Boone County, IA", "loc": "41.97761, -93.70042", "p_name": "30 MW Iowa DG Portfolio", "p_tnum": 10, "p_cap": 30.0, "t_manu": "Nordex", "t_model": "AW125/3000", "t_cap": 3000, "t_hh": 87.5, "t_rd": 125.0, "t_rsa": 12271.85, "t_ttlh": 150.0, "retrofit": 0, "t_conf_atr": 3, "t_conf_loc": 3, "eia_id": null, "dbms": "test", "table": "wind_turbine"}
        {"timestamp": "2017-02-16T11:23:01.044169Z", "usgs_pr_id": null, "address": "Story County, IA", "loc": "41.88248, -93.63284", "p_name": "30 MW Iowa DG Portfolio", "p_tnum": 10, "p_cap": 30.0, "t_manu": "Nordex", "t_model": "AW125/3000", "t_cap": 3000, "t_hh": 87.5, "t_rd": 125.0, "t_rsa": 12271.85, "t_ttlh": 150.0, "retrofit": 0, "t_conf_atr": 3, "t_conf_loc": 3, "eia_id": null, "dbms": "test", "table": "wind_turbine"}
        {"timestamp": "2017-02-16T11:23:02.044782Z", "usgs_pr_id": null, "address": "Story County, IA", "loc": "42.01637, -93.51589", "p_name": "30 MW Iowa DG Portfolio", "p_tnum": 10, "p_cap": 30.0, "t_manu": "Nordex", "t_model": "AW125/3000", "t_cap": 3000, "t_hh": 87.5, "t_rd": 125.0, "t_rsa": 12271.85, "t_ttlh": 150.0, "retrofit": 0, "t_conf_atr": 3, "t_conf_loc": 3, "eia_id": null, "dbms": "test", "table": "wind_turbine"}
        {"timestamp": "2017-02-16T11:23:03.045453Z", "usgs_pr_id": null, "address": "Story County, IA", "loc": "42.01363, -93.51808", "p_name": "30 MW Iowa DG Portfolio", "p_tnum": 10, "p_cap": 30.0, "t_manu": "Nordex", "t_model": "AW125/3000", "t_cap": 3000, "t_hh": 87.5, "t_rd": 125.0, "t_rsa": 12271.85, "t_ttlh": 150.0, "retrofit": 0, "t_conf_atr": 3, "t_conf_loc": 3, "eia_id": null, "dbms": "test", "table": "wind_turbine"}
        {"timestamp": "2017-02-16T11:23:04.045743Z", "usgs_pr_id": null, "address": "Hardin County, IA", "loc": "42.49794, -93.3678", "p_name": "30 MW Iowa DG Portfolio", "p_tnum": 10, "p_cap": 30.0, "t_manu": "Nordex", "t_model": "AW125/3000", "t_cap": 3000, "t_hh": 87.5, "t_rd": 125.0, "t_rsa": 12271.85, "t_ttlh": 150.0, "retrofit": 0, "t_conf_atr": 3, "t_conf_loc": 3, "eia_id": null, "dbms": "test", "table": "wind_turbine"}
        {"timestamp": "2017-02-16T11:23:05.046557Z", "usgs_pr_id": null, "address": "Story County, IA", "loc": "42.00681, -93.52365", "p_name": "30 MW Iowa DG Portfolio", "p_tnum": 10, "p_cap": 30.0, "t_manu": "Nordex", "t_model": "AW125/3000", "t_cap": 3000, "t_hh": 87.5, "t_rd": 125.0, "t_rsa": 12271.85, "t_ttlh": 150.0, "retrofit": 0, "t_conf_atr": 3, "t_conf_loc": 3, "eia_id": null, "dbms": "test", "table": "wind_turbine"}
    :positional arguments:
        conn                              IP:Port credentials for either REST
        protocol    {post,put,print}      format to save data
        dbms                              Logical database to store data in
    :optional arguments:
        -h, --help                              show this help message and exit
        --authentication    AUTHENTICATION      username, password
        --timeout           TIMEOUT             REST timeout (in seconds)
        --timestamp-now     TIMESTAMP_NOW       use current timestamp instead of value in row
        --topic             TOPIC               topic for REST POST
        --row_count         ROW_COUNT           Number of rows to insert (if 0 insert all)
        --sleep             SLEEP               sleep time between each insert
        -e, --exception     EXCEPTION           whether or not to print exceptions to screen
    :params:
        content:requests.GET - Results from USGS wind turbine data
        table_name:str - logical table name data will be stored in
        row:dict - value(s) from content to generate rows from
        payloads:list - list of a single dict with data based on row
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('conn',     type=str, default='127.0.0.1:2049', help='IP:Port credentials for either REST')
    parser.add_argument('protocol', type=str, choices=['post', 'put', 'print'], default='print', help='format to save data')
    parser.add_argument('dbms',     type=str, default='test', help='Logical database to store data in')
    parser.add_argument('--authentication', type=str, default=None, help='username, password')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout (in seconds)')
    parser.add_argument('--topic', type=str, default=None, help='topic for REST POST')
    parser.add_argument('--timestamp-now', type=bool, nargs='?', const=True, default=False, help='use current timestamp instead of value in row')
    parser.add_argument('--row-count',   type=int, default=1, help='Number of rows to insert (if 0 insert all)')
    parser.add_argument('--sleep',  type=float, default=1, help='sleep time between each insert')
    parser.add_argument('-e', '--exception', type=bool, nargs='?',     const=True, default=False, help='whether or not to print exceptions to screen')
    args = parser.parse_args()

    content = requests.get('https://eersc.usgs.gov/api/uswtdb/v1/turbines')
    table_name = 'wind_turbine'
    count = 0
    for row in content.json():
        if args.timestamp_now is True:
            row['p_year'] = 'now'
        payloads = [{
            'timestamp': generate_timestamp(year=row['p_year']),  # Timestamp
            'usgs_pr_id': row['usgs_pr_id'], # Unique identifier for cross-reference to the 2014 USGS turbine dataset.
            'address': f"{row['t_county']}, {row['t_state']}",  # county, State where turbine is located
            'loc': f"{row['ylat']}, {row['xlong']}",  # lat/long: 'xlong': -118.36376, 'ylat': 35.07791 --> (35.07791,-118.36376)
            'p_name': row['p_name'],  # Name of the wind power project that the turbine is a part of
            'p_tnum': row['p_tnum'],  # Number of turbines in the wind power project.
            'p_cap': row['p_cap'],  # Cumulative capacity of all turbines in the wind power project in megawatts (MW).
            't_manu': row['t_manu'],  # Turbine manufacturer
            't_model': row['t_model'],  # Turbine model
            't_cap': row['t_cap'],  # Turbine rated capacity
            't_hh': row['t_hh'],  # Turbine hub height in meters
            't_rd': row['t_rd'],  # Turbine rotor diameter in meters
            't_rsa': row['t_rsa'],  # Turbine rotor swept area in square meters
            't_ttlh': row['t_ttlh'],  # Turbine total height from ground to tip of a blade at its apex in meters
            'retrofit': row['retrofit'], # Indicator of whether the turbine has been partially retrofit after initial construction
            't_conf_atr': row['t_conf_atr'],  # Level of confidence in the turbine attributes.
            't_conf_loc': row['t_conf_loc'],  # Level of confidence in turbine location
            'eia_id': row['eia_id'],  # Plant ID from Energy Information Administration (EIA).
        }]
        if args.protocol == 'print':
            import generic_protocol
            generic_protocol.print_content(data=payloads, dbms=args.dbms, table=table_name)
        elif args.protocol == 'put':
            from rest import put_data
            if not put_data(conn=args.conn, data=payloads, dbms=args.dbms, table=table_name, auth=args.auth,
                            timeout=args.timeout, exception=args.exception):
                print('Failed to PUT data into %s' % args.conn)
                status = False
        elif args.protocol == 'post':
            from rest import post_data
            post_data(conn=args.conn, data=payloads, dbms=args.dbms, table=table_name, rest_topic=args.topic,
                      exception=args.exception)
        if args.row_count != 0 and count == args.row_count - 1:
            exit(1)
        elif args.row_count != 0 and count != args.row_count - 1:
            time.sleep(args.sleep)
            count+=1


if __name__ == '__main__':
    generate_windturbine_data()
