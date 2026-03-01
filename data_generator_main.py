import argparse

# from source.southbound.random_data import main as rand_data
# from source.southbound.rig_data import main as rig_data
from source.southbound.vessel_data import main as vessel_data
# from source.southbound.wind_turbine import main as wind_turbine
# from source.southbound.proveit_data import main as proveit_data

# from source.policies.random_mapping import main as random_mapping
# from source.policies.wind_turbine_mapping import main as wind_turbine_mapping
# from source.policies.rig_mapping import main as rig_mapping
from source.policies.vessel_mapping import main as vessel_mapping

from source.northbound.mqtt_calls import MqttClient
from source.northbound.rest_calls import RestClient
from source.northbound.opcua import OpcuaServer

from source.policies.mappings import RIG_INFO
from source.support import extract_credentials



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
    # PROVEIT
    # -------------------------
    proveit_parser = subparsers.add_parser("proveit")
    proveit_parser.add_argument("publish_format", nargs='?', choices=["print", "post", "mqtt", "opcua"],
                                default="print", help=publish_format_help)
    proveit_parser.add_argument("--proveit-topics", type=str, nargs="+",
                                choices=["Enterprise A",  "Enterprise A/Dallas", "Enterprise A/opto22",
                                         "Enterprise B", "Enterprise B/Site1", "Enterprise B/Site2",
                                         "Enterprise B/Site3",
                                         "Enterprise C", "Enterprise C/sub", "Enterprise C/tff", "Enterprise C/chrom",
                                         "Enterprise C/sum"],
                                help="Space-separated ProveIT topics. If omitted, all topics")

    # -------------------------
    # GLOBAL ARGS
    # -------------------------
    parser.add_argument("--control-conn", type=str, default=None, required=False,
                        help="IP:Port of the AnyLog/EdgeLake node used for mapping policies and msg-client.")
    parser.add_argument("--data-conn", type=str, default=None,
                        help="Optional IP:Port for data publishing (REST/MQTT). If omitted, defaults to --control-conn. For OPC-UA the default will be 0.0.0.0:4840")


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

        proveit
            - Data: Proveit 2026 conference data. Data is values only and require a special `msg client` or `OPC-UA` process to pull into AnyLog / EdgeLake
            - Publish: PRINT, POST, MQTT, OPC-UA (server)
            - Optional: specific group of topic-based data set
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

        --proveit-topics TOPIC [TOPIC...]
            Proveit topics:
                "Enterprise A",  "Enterprise A/Dallas", "Enterprise A/opto22", "Enterprise B", "Enterprise B/Site1",
                "Enterprise B/Site2", "Enterprise B/Site3", "Enterprise C", "Enterprise C/sub",
                "Enterprise C/tff", "Enterprise C/chrom", "Enterprise C/sum"
            Examples:
                --proveit-topic "Enterprise A"
                 --proveit-topic "Enterprise A/Dallas", "Enterprise C"
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
    args.publish_format = args.publish_format.upper()
    # 1. default for OPC-UA
    if args.publish_format == "OPCUA" and not args.data_conn:
        args.data_conn = "0.0.0.0:4840"
    # 2. for POST use data_conn if control_conn not provided
    elif args.publish_format in ["PUT", "POST"] and not args.control_conn and args.data_conn:
        args.control_conn = args.data_conn
    # 3. for PUT / POST if data_name  not provided
    elif args.publish_format in ["PUT", "POST"] and args.control_name and not args.data_conn:
        args.data_conn = args.control_conn
    # 4. Warning: missing args.control_conn, but there's data_conn
    elif args.publish_format not in ["MQTT", "OPCUA"] and not args.control_conn and args.data_conn: # warning only
        print(f"Missing `--control-conn` for {args.publish_format}, will not declare mapping or `msg client`")
    # 5. Exception: missing both control_conn and data_conn
    elif args.publish_format in ["POST", "MQTT"] and not args.control_conn and not args.data_conn:
        raise argparse.ArgumentError(argument=None, message=f"publishing format {args.publish_format} requires missing connection information")


    # Define connection information
    control_conn = None
    data_conn    = None
    data_broker = None
    data_port = None
    is_rest = False
    if args.publish_format != "PRINT":
        if args.control_conn:
            broker, port, user, password = extract_credentials(args.control_conn)
            control_conn = RestClient(conn=f"{broker}:{port}", auth=(user, password), timeout=args.timeout)
        if args.data_conn:
            broker, port, user, password = extract_credentials(args.data_conn)
            if args.publish_format in ["POST", "PUT"]:
                data_conn = RestClient(conn=f"{broker}:{port}", auth=(user, password), timeout=args.timeout)
                is_rest = True
            elif args.publish_format == "MQTT":
                data_conn = MqttClient(host=broker, port=port, user=user, password=password, timeout=args.timeout)
            elif args.publish_format == "OPCUA":
                data_conn = OpcuaServer(host=broker, port=port)
            data_broker = broker
            data_port = port

    # publish msg client and define data
    # if args.data == "random":
    #     if control_conn is not None and args.publish_format in ["POST", "MQTT"]:
    #         random_mapping(conn=control_conn, broker=data_broker, port=data_port, is_rest=is_rest)
    #     rand_data(method=args.publish_format, conn=data_conn, db_name=args.db_name, iterations=args.repeat, sleep=args.sleep)
    # elif args.data == "rig":
    #     if control_conn is not None and args.publish_format in ["POST", "MQTT"]:
    #         rig_mapping(conn=control_conn, broker=data_broker, port=data_port, is_rest=is_rest)
    #     rig_data(method=args.publish_format, conn=data_conn, db_name=args.db_name, publish_topics=args.rig_ids,
    #              iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)
    if args.data == "vessel":
        if control_conn is not None and args.publish_format in ["POST", "MQTT"]:
            vessel_mapping(conn=control_conn, broker=data_broker, port=data_port, is_rest=is_rest)
        vessel_data(method=args.publish_format, conn=data_conn, db_name=args.db_name, publish_topics=args.vessel_ids,
                    iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)
    # elif args.data == "wind-turbine":
    #     if control_conn is not None and args.publish_format in ["POST", "MQTT"]:
    #         wind_turbine_mapping(conn=control_conn, broker=data_broker, port=data_port, is_rest=is_rest)
    #     wind_turbine(method=args.publish_format, conn=data_conn, db_name=args.db_name, publish_topics=args.turbine_ids,
    #                  iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)
    # elif args.data == "proveit": # conn=control_conn, broker=data_broker, port=data_port, is_rest=is_rest
    #     if control_conn is not None and args.publish_format in ["POST", "MQTT"]:
    #         pass
    #     proveit_data(method=args.publish_format, conn=data_conn, publish_topics=args.proveit_topics,
    #                  iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)


if __name__ == "__main__":
    main()

