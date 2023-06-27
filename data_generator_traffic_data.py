import argparse
import os
import random
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import data_generators.transit_data as transit_data
import publishing_protocols.support as support
import publishing_protocols.publish_data as publish_data


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
    "SF": "SFMTA", # San Francisco Municipal Transportation Agency
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



def create_base_transit_map(license_key:str, transit_agency:str, bus_line:str, exception:bool=False):
    create_table_stmt = """
            CREATE TABLE IF NOT EXISTS transit_map(
                id SERIAL NOT NULL PRIMARY KEY,
                operator VARCHAR, 
                line INT,
                stop VARCHAR,
                location GEOMETRY(Point, 4326)
            );
        """
    insert_stmt = "INSERT INTO transit_map(operator, line, stop, location) VALUES "

    line_stops = transit_data.list_stops(license_key=license_key, operator_id=transit_agency,
                                         line=bus_line, exception=exception)
    for stop in line_stops:
        insert_stmt += f"\n\t('{TRANSIT_AGENCIES[stop['operator']]}', '{bus_line}', '{stop['stop']}', ST_SetSRID(ST_MakePoint({stop['location']}), 4326)),"
    insert_stmt = insert_stmt.rsplit(",", 1)[0] + ";"
    print(insert_stmt)





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('transit_agency', type=str, choices=list(TRANSIT_AGENCIES.keys()), default="SM",
                        help="transit agency to get insight from")
    parser.add_argument('insert_process', type=str, choices=['print', 'put', 'post', 'mqtt'],
                        default='print', help='format to store generated data')
    parser.add_argument('--db-name', type=str, default='test', help='logical database name')
    parser.add_argument('--table-name', type=str, default="transit_data",
                        help='Change default table name')
    parser.add_argument('--total-rows', type=support.validate_row_size, default=1000000,
                        help='number of rows to insert. If set to 0, will run continuously')
    parser.add_argument('--batch-size', type=support.validate_row_size, default=10,
                        help='number of rows to insert per iteration')
    parser.add_argument('--sleep', type=float, default=0.5, help='wait time between each row')
    parser.add_argument('--conn', type=support.validate_conn_pattern, default=None,
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('--topic', type=str, default=None, help='topic for publishing data via REST POST or MQTT')
    parser.add_argument('--rest-timeout', type=float, default=30, help='how long to wait before stopping REST')
    parser.add_argument('--qos', type=int, choices=list(range(0, 3)), default=0, help='MQTT Quality of Service')
    parser.add_argument("--license-key", type=str, default=LICENSE_KEY, help="license key for 511.org")
    parser.add_argument("--exception", type=bool, nargs='?', const=True, default=False, help="Print exception")
    args = parser.parse_args()
    transit_agencies = args.transit_agency.split(",")
    total_rows = 0
    if args.batch_size <= 0:
        args.batch_size = 1

    conns = None
    if args.conn is not None:
        conns = args.conn.split(',')
    if args.insert_process == "mqtt":
        conns = publish_data.connect_mqtt(conns, exception=args.exception)
        if not conns:
            print("Failed to set connection for MQTT publisher")
            exit(1)
    elif args.insert_process in ["post", "put"]:
        conns = publish_data.setup_put_post_conn(conns=conns)


    while True:
        transit_agency = random.choice(transit_agencies)
        payloads = transit_data.vehicle_position(license_key=args.license_key, transit_code=transit_agency,
                                                 transit_agency=TRANSIT_AGENCIES[transit_agency], db_name=args.db_name,
                                                 table_name=args.table_name, batch_size=args.batch_size,
                                                 exception=args.exception)

        publish_data.publish_data(payload=payloads, insert_process=args.insert_process, conns=conns,
                                  topic=args.topic, compress=args.compress, rest_timeout=args.rest_timeout,
                                  qos=args.qos, dir_name=args.dir_name, exception=args.exception)

        total_rows += len(payloads)
        if total_rows >= args.total_rows:
            exit(1)
        time.sleep(args.sleep)



if __name__ == '__main__':
    main()

