import argparse

from source.northbound.mqtt_calls import MqttClient
from source.northbound.rest_calls import RestClient
from source.support import extract_credentials
from source.southbound.random_data import main as rand_data
from source.southbound.rig_data import main as rig_data
from source.southbound.vessel_data import main as vessel_data
from source.southbound.wind_turbine import main as wind_turbine
from source.policies.mappings import RIG_INFO


def build_parser(parser:argparse.ArgumentParser):
    publish_format_help = (
        "Format to publish data: "
        "print = local only, no connection required; "
        "put/post/mqtt = publish to AnyLog/EdgeLake"
    )

    subparsers = parser.add_subparsers(dest="data", required=True, help="Data type to publish")

    # -------------------------
    # RANDOM
    # -------------------------
    random_parser = subparsers.add_parser("random")
    random_parser.add_argument("publish_format", nargs="?",  choices=["print", "put", "post", "mqtt"],
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
    parser.add_argument("--conn", type=str, default=None,
                        help="IP:Port connection information for publishing data. For OPC-UA data. the default value is 0.0.0.0:4840")
    parser.add_argument("--db-name", type=str, default="test", help="Default logical database")
    parser.add_argument("--repeat", type=int, default=10,
                        help="Number of iterations - if set to 0 then run continuously")
    parser.add_argument("--timeout", type=float, default=60, help="REST timeout")
    parser.add_argument("--sleep", type=float, default=15, help="sleep between each iteration")
    parser.add_argument("--offset-sleep", type=float, default=0.5,
                        help="When publishing multiple IDs, time offset between each ID")

    return parser



def main():
    """
    Publish synthetic or file‑based data into AnyLog / EdgeLake.

    Use msg_client_generator.py to create policies and MQTT settings when
    publishing via POST or MQTT.

    USAGE
        python generator.py [data-source] [publish-format] [options]

    DATA SOURCES
        random
            - Data: timestamp/value
            - Publish: PRINT, PUT, POST, MQTT
            - No ID selection required

        rig
            - Data: timestamp and values (single table)
            - Publish: PRINT, PUT, POST, MQTT
            - Optional: specify rig ID(s)

        vessel
            - Data: DLB and DLT engine data
            - Publish: PRINT, POST, MQTT
            - Optional: specify vessel side(s)

        wind-turbine
            - Data: timestamp and values across multiple tables
            - Publish: PRINT, POST, MQTT
            - Optional: specify turbine ID(s)

    PUBLISH FORMATS
        PRINT
            Output generated data to screen only (no network activity).
            No connection information required.

        PUT
            Send data via REST (not supported for vessel or wind-turbine).

        POST
            Send data via REST. Requires --conn.

        MQTT
            Publish data to an MQTT broker. Requires --conn.

    GLOBAL OPTIONS
        --conn IP:PORT
            Connection information for REST or MQTT publishing.
            Required when using POST or MQTT.
            For OPC-UA publishing, if omitted, defaults to 0.0.0.0:4840.

        --db-name DB_NAME
            Logical database name (default: test).

        --repeat REPEAT
            Number of iterations. If set to 0, runs continuously (default: 10).

        --timeout TIMEOUT
            REST / MQTT timeout in seconds (default: 60).

        --sleep SECONDS
            Delay between iterations (default: 15).

        --offset-sleep SECONDS
            Delay between publishing multiple IDs (default: 0.5).

    DATA-SPECIFIC OPTIONS
        --rig-ids ID [ID ...]
            Space-separated rig IDs.
            If omitted, all rigs are used.
            Examples:
                --rig-ids 1 3 7
                --rig-ids=1,3,7

        --vessel-ids SIDE [SIDE ...]
            Vessel engine sides: DLB, DLT.
            If omitted, both are used.
            Examples:
                --vessel-ids DLB
                --vessel-ids=DLB,DLT

        --turbine-ids ID [ID ...]
            Turbine IDs: 1–11 except 4.
            If omitted, all valid turbines are used.
            Examples:
                --turbine-ids 1 3 7
                --turbine-ids=1,3,7

    EXAMPLES
        # Print random data to screen
        python generator.py random print

        # Publish rig 1 and 3 via MQTT
        python generator.py rig mqtt --conn 127.0.0.1:32150 --rig-ids 1 3

        # Same as above, comma-separated
        python generator.py rig mqtt --conn 127.0.0.1:32150 --rig-ids=1,3

        # Publish all wind turbines except 4 via POST
        python generator.py wind-turbine post --conn 127.0.0.1:32149

        # Publish only turbines 2 and 7
        python generator.py wind-turbine post --conn 127.0.0.1:32149 --turbine-ids=2,7

        # Publish vessel DLB only
        python generator.py vessel mqtt --conn 127.0.0.1:32150 --vessel-ids DLB
    """
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    # parser = argparse.ArgumentParser()
    parser = build_parser(parser=parser)
    args = parser.parse_args()

    # -------------------------
    # CONDITIONAL VALIDATION
    # -------------------------
    if args.publish_format in ("post", "mqtt") and not args.conn:
        parser.error("--conn is required when using POST or MQTT")
    elif args.publish_format == "opcua" and not args.conn:
        args.conn = "0.0.0.0:4840"



    args.publish_format = args.publish_format.upper()
    conn = None
    if args.publish_format != "PRINT":
        if not args.conn:
            raise argparse.ArgumentError(argument=None, message=f"publishing format {args.publish_format} requires missing connection information")
        broker, port, user, password = extract_credentials(args.conn)
        if args.publish_format in ["POST", "PUT"]:
            conn = RestClient(conn=f"{broker}:{port}", auth=(user, password), timeout=args.timeout)
        elif args.publish_format == "MQTT":
            conn = MqttClient(host=broker, port=port, user=user, password=password, timeout=args.timeout)

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

