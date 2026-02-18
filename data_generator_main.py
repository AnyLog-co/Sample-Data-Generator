import argparse

from source.northbound.mqtt_calls import MqttClient
from source.northbound.rest_calls import RestClient
from source.northbound.opcua import OpcuaServer
from source.support import extract_credentials
from source.southbound.random_data import main as rand_data
from source.southbound.rig_data import main as rig_data
from source.southbound.wind_turbine import main as wind_turbine
from source.policies.mappings import RIG_INFO


def main():
    """
    The following provides the ability to publish data into AnyLog / EdgeLake

    Please use msg_client_generator.py to create policies and MQTT when publishing
    into AnyLog / EdgeLage via POST or Message broker

    :positional arguments:
        conn                  Connection information ([user]:[pass]@[ip]:[port])
    :data sources:
        * random
            - data: timestamp/value
            - publish: PUT, POST and MQTT
        * proveit
            - data: value by topic
            - publish: POST, MQTT and OPC-UA server
            - optional: specify topic(s)
        * rig:
            - data: timestamp and values (single table)
            - publish: PUT, POST and MQTT
            - optional: specify rig(s)
        * wind turbine
            - data: timestamp and values for multiple tables
            - publish: PUT, POST and MQTT
            - optional: wind turbine specific
        * boat
            - data: DLB and DLT data
            - publish: PUT, POST and MQTT

    :positional arguments:
        conn    Connection information ([user]:[pass]@[ip]:[port]). For OPC-UA, specify the server endpoint (default: 0.0.0.0:4840)."
        data    Data to publish into Anylog/EdgeLake
            * random
            * proveit
            * rig
            * wind-turbine
            * boat
        publish_format  format to publish data into AnyLog/EdgeLake
            * PUT (not supported with Proveit)
            * POST
            * MQTT
            * OPC-UA  (Proveit only)
    :optional arguments:
        -h, --help              show this help message and exit
        --repeat    REPEAT      number of iterations per run
        --timeout   TIMEOUT     REST and MQTT timeout
        --sleep     SLEEP       time period to wait between each insertion
    :publish-specific arguments:
        --rig-id        space separated ID to get rig data from, if not set - will provide for all
        --turbine-id    space separated ID to get wind turbines data from, if not set - will provide for
        --topics        comma separated topics to get data from. If not set, provide all data
    """
    parser = argparse.ArgumentParser(description=main.__doc__,  formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("conn", type=str, nargs="?", default=None,
                        help="Connection information ([user]:[pass]@[ip]:[port]). For OPC-UA, specify the server endpoint (default: 0.0.0.0:4840).")

    subparsers = parser.add_subparsers(dest="data", required=True, help="data to publish into Anylog/EdgeLake")

    for param in ["random", "boat", "wind-turbine", "rig"]:
        common_parser = subparsers.add_parser(param)
        common_parser.add_argument("publish_format", nargs="?", choices=["put", "post", "mqtt"],
                                   default="put", help="format to publish data into AnyLog/EdgeLake")
        if param == "rig":
            common_parser.add_argument("--rig-id", type=int, nargs="+", choices=list(RIG_INFO.keys()),
                                       default=None,
                                       help="space separated ID to get rig data from, if not set - will provide for all"
                                            "rigs")

        elif param == "wind-turbine":
            common_parser.add_argument("--turbine-id", type=int, nargs="+", choices=list(range(1, 12)), default=None,
                                       help="space separated ID to get wind turbines data from, if not set - will provide for"
                                            "all turbines")

    proveit_parser = subparsers.add_parser("proveit")
    proveit_parser.add_argument("publish_format", nargs="?", choices=["opcua", "post", "mqtt"], default="opcua", help = "format to publish data into AnyLog/EdgeLake")
    proveit_parser.add_argument("--topics", type=lambda s: s.split(","), default=None,
                                help="comma separated topics to get data from. If not set, provide all data")

    parser.add_argument("--db-name", type=str, defualt="test", help="logical database used when publishing data in all formats but OPC-UA")
    parser.add_argument("--repeat", type=int, default=10, help="number of iterations per run")
    parser.add_argument("--timeout", type=float, default=60, help="REST and MQTT timeout")
    parser.add_argument("--sleep", type=float, default=15, help="time period to wait between each insertion")
    args = parser.parse_args()

    broker, port, user, password = extract_credentials(credentials=args.conn)
    if args.publish_format.lower() in ["put", "post"]:
        conn = RestClient(conn=f"{broker}:{port}", auth=(user, password), timeout=args.timeout)
    elif args.publish_format.lower() == "mqtt":
        conn = MqttClient(host=broker, port=port, user=user, password=password, timeout=args.timeout )
    elif args.publish_format.lower() == "opcua": # runs an OPC-UA server against the IP and port provided in the connection
        conn = OpcuaServer(host=broker, port=port)
    else:
        raise ValueError(f"Unsupported {args.publish_format}")

    if args.data == "random":
       rand_data(method=args.publish_format.upper(), conn=conn, db_name=args.db_name, iterations=args.repeat,
                 sleep=args.sleep)
    elif args.data == "rig":
        rig_data(method=args.publish_format.upper(), conn=conn, db_name=args.db_name, iterations=args.repeat,
                 rig_ids=args.rig_ids, sleep=args.sleep)
    elif args.data == "wind-turbine":
        wind_turbine(method=args.publish_format.upper(), conn=conn, db_name=args.db_name, iterations=args.repeat,
                     turbine_ids=args.turbine_id, sleep=args.sleep)


if __name__ == "__main__":
    main()

