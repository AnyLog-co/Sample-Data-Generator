import argparse

from source.northbound.mqtt_calls import MqttClient
from source.northbound.rest_calls import RestClient
from source.northbound.opcua import OpcuaServer
from source.support import extract_credentials
from source.southbound.random_data import main as rand_data
from source.southbound.rig_data import main as rig_data
from source.southbound.vessel_data import main as vessel_data
from source.southbound.wind_turbine import main as wind_turbine
from source.policies.mappings import RIG_INFO


def main():
    """
    The following provides the ability to publish data into AnyLog / EdgeLake.

    Please use msg_client_generator.py to create policies and MQTT settings when
    publishing into AnyLog / EdgeLake via POST or Message Broker.

    POSITIONAL ARGUMENTS
        conn    Connection information in the form: [user]:[pass]@[ip]:[port]

    DATA SOURCES
        random
            - Data: timestamp/value
            - Publish: PUT, POST, MQTT, PRINT
            - No ID selection required
        rig
            - Data: timestamp and values (single table)
            - Publish: PUT, POST, MQTT, PRINT
            - Optional: specify rig ID(s)
        vessel
            - Data: DLB and DLT engine data
            - Publish: POST, MQTT, PRINT
            - Optional: specify vessel side(s)
        wind-turbine
            - Data: timestamp and values across multiple tables
            - Publish: POST, MQTT, PRINT
            - Optional: specify turbine ID(s)

    PUBLISH FORMATS
        PUT     Send data via REST (not supported for vessel or wind-turbine)
        POST    Send data via REST
        MQTT    Publish data to an MQTT broker
        PRINT   Output generated data to screen only (no network activity)

    OPTIONAL ARGUMENTS
        -h,             --help          Show this help message and exit
        --db-name       DB_NAME         Logical database to store content in (default: test)
        --repeat        REPEAT          Number of iterations to run. If set to 0, runs continuously.
        --timeout       TIMEOUT         REST / MQTT timeout in seconds (default: 60)
        --sleep         SLEEP           Delay between iterations (default: 15 seconds)
        --offset-sleep  OFFSET_SLEEP    Delay between publishing multiple IDs (default: 0.5 seconds)

    PUBLISH-SPECIFIC ARGUMENTS
        --rig-id ID [ID ...]
            Space-separated or comma-separated rig IDs.
            If omitted, all rigs are used.
            Examples:
                --rig-id 1 3 7
                --rig-id=1,3,7
        --vessel-ids SIDE [SIDE ...]
            Space-separated or comma-separated vessel sides (DLB, DLT).
            If omitted, both are used.
            Examples:
                --vessel-ids DLB
                --vessel-ids=DLB,DLT
        --turbine-id ID [ID ...]
            Space-separated or comma-separated turbine IDs.
            Valid IDs: 1–11 except 4.
            If omitted, all valid turbines are used.
            Examples:
                --turbine-id 1 3 7
                --turbine-id=1,3,7

    EXAMPLES
        # Print random data to screen
        python generator.py random print

        # Publish rig 1 and 3 via MQTT
        python generator.py 127.0.0.1:32150 rig mqtt --rig-id 1 3

        # Same as above, comma-separated
        python generator.py 127.0.0.1:32150 rig mqtt --rig-id=1,3

        # Publish all wind turbines except 4 via POST
        python generator.py 127.0.0.1:32149 wind-turbine post

        # Publish only turbines 2 and 7
        python generator.py 127.0.0.1:32149  wind-turbine post --turbine-id=2,7

        # Publish vessel DLB only
        python generator.py 127.0.0.1:32150 vessel mqtt --vessel-ids DLB
    """
    publish_format_help=("How to output the generated data: "
                         "\n\t- 'put' and 'post' send via REST" 
                         "\n\t- 'mqtt' publishes to MQTT"
                         "\n\t- 'print' outputs to screen only")
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("conn", type=str, nargs="?", default=None,
                        help="Connection information ([user]:[pass]@[ip]:[port]).")

    subparsers = parser.add_subparsers(dest="data", required=True, help="Data type to publish into AnyLog/EdgeLake")

    # -------------------------
    # RANDOM
    # -------------------------
    random_parser = subparsers.add_parser("random")
    random_parser.add_argument("publish_format", nargs="?", choices=["print", "put", "post", "mqtt"],
                               default="print", help=publish_format_help)

    # -------------------------
    # RIG
    # -------------------------
    rig_parser = subparsers.add_parser("rig")
    rig_parser.add_argument("publish_format", nargs="?", choices=["print", "put", "post", "mqtt"],
                               default="print", help=publish_format_help)
    rig_parser.add_argument("--rig-ids", type=int, nargs="+", choices=list(RIG_INFO.keys()), default=None,
                            help="Space-separated rig IDs. If omitted, all rigs are used.")

    # -------------------------
    # VESSEL
    # -------------------------
    vessel_parser = subparsers.add_parser("vessel")
    vessel_parser.add_argument("publish_format", nargs="?", choices=["print", "post", "mqtt"],
                               default="print", help=publish_format_help)
    vessel_parser.add_argument("--vessel-ids", nargs="+", choices=["DLB", "DLT"], default=None,
                               help="Vessel engine side(s)")
    # -------------------------
    # WIND TURBINE
    # -------------------------
    wt_parser = subparsers.add_parser("wind-turbine")
    wt_parser.add_argument("publish_format", nargs="?", choices=["print", "post", "mqtt"],
                               default="print", help=publish_format_help)
    wt_parser.add_argument("--turbine-ids", type=int, nargs="+",
                           choices=[i for i in range(1, 12) if i != 4], default=None,
                           help="Space-separated turbine IDs. If omitted, all turbines except 4.")

    # -------------------------
    # GLOBAL ARGS
    # -------------------------
    parser.add_argument("--db-name", type=str, default="test", help="logical database to store content in")
    parser.add_argument("--repeat", type=int, default=10,
                        help="Number of iterations until stop. If set to 0, then run continuously")
    parser.add_argument("--timeout", type=float, default=60, help="REST / MQTT timeout")
    parser.add_argument("--sleep", type=float, default=15, help="sleep between each iteration")
    parser.add_argument("--offset-sleep", type=float, default=0.5,
                        help="When publishing multiple IDs, time offset between each ID")

    args = parser.parse_args()


    args.publish_format = args.publish_format.upper()
    conn = None
    if args.publish_format != "PRINT":
        if not args.conn:
            raise argparse.ArgumentError(f"publishing format {args.publish_format} requires missing connection information")
        broker, port, user, password = extract_credentials(args.conn)
        if args.publish_format in ["POST", "PUT"]:
            conn = RestClient(conn=f"{broker}:{port}", auth=(user, password), timeout=args.timeout)
        elif args.publish_format == "MQTT":
            conn = MqttClient(broker=broker, port=port, user=user, password=password, timeout=args.timeout)

    if args.data == "random":
        rand_data(method=args.publish_format, conn=conn, db_name=args.db_name, iterations=args.repeat, sleep=args.sleep)
    elif args.data == "rig":
        rig_data(method=args.publish_format, conn=conn, db_name=args.db_name, publish_topics=args.rig_ids,
                 iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)
    elif args.data == "vessel":
        vessel_data(method=args.publish_format, conn=conn, db_name=args.db_name, publish_topics=args.vessel_ids,
                    iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)
    elif args.data == "wind-turbine":
        wind_turbine(method=args.publish_format, conn=conn, db_name=args.db_name, publish_topics=args.turbine_ids,
                    iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)


if __name__ == "__main__":
    main()

