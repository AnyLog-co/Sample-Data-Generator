import argparse


from source.northbound.mqtt import MqttClient
from source.northbound.kafka import KafkaClient
from source.northbound.rest_calls import RestClient
from source.northbound.opcua import OpcuaServer

from source.policies.mappings import RIG_INFO
from source.support import extract_credentials


def _import_parser(data:str, skip_insert:bool=False, skip_msg_client:bool=False)->dict:
    """
    Import `msg client` and data generator based on used defined params as opposed to importing everything
    :Args:
        data:str - data generator
        skip_insert:bool - whether to skip insert or not
        skip_msg_client:bool - whether to skip message client or not
    :params:
        imports:dict defined import functions
    :return:
        imports
    """
    imports = {}

    if data == "random":
        if not skip_insert:
            from source.southbound.random_data import main as rand_data
            imports["insert"] = rand_data
        if not skip_msg_client:
            from source.policies.random_mapping import main as random_mapping
            imports["msg_client"] = random_mapping
    elif data == "rig":
        if not skip_insert:
            from source.southbound.rig_data import main as rig_data
            imports["insert"] = rig_data
        if not skip_msg_client:
            from source.policies.rig_mapping import main as rig_mapping
            imports["msg_client"] = rig_mapping
    elif data == "vessel":
        if not skip_insert:
            from source.southbound.vessel_data import main as vessel_data
            imports["insert"] = vessel_data              # ← was missing
        if not skip_msg_client:
            from source.policies.vessel_mapping import main as vessel_mapping
            imports["msg_client"] = vessel_mapping           # ← was missing
    elif data == "wind-turbine":
        if not skip_insert:
            from source.southbound.wind_turbine import main as wind_turbine
            imports["insert"] = wind_turbine             # ← was missing
        if not skip_msg_client:
            from source.policies.wind_turbine_mapping import main as wind_turbine_mapping
            imports["msg_client"] = wind_turbine_mapping     # ← was missing
    elif data == "wind-turbine2":
        if not skip_insert:
            from source.southbound.wind_turbine2 import main as wind_turbine2
            imports["insert"] = wind_turbine2            # ← was missing
        if not skip_msg_client:
            from source.policies.wind_turbine2_mqtt import run_msg_client as wind_turbine2_msg_client, enable_streamer
            imports["msg_client"] = wind_turbine2_msg_client # ← was missing
    elif data == "proveit":
        if not skip_insert:
            from source.southbound.proveit_data import main as proveit_data
            imports["insert"] = proveit_data             # ← was missing

    return imports


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
    random_parser.add_argument("publish_format", nargs="?",  choices=["print", "put", "post", "mqtt", "kafka"],
                               default="print", help=publish_format_help)

    # -------------------------
    # RIG
    # -------------------------
    rig_parser = subparsers.add_parser("rig")
    rig_parser.add_argument("publish_format", nargs="?", choices=["print", "put", "post", "mqtt", "kafka"],
                            default="print", help=publish_format_help)
    rig_parser.add_argument("--ids", type=int, nargs="+", choices=list(RIG_INFO.keys()), default=None,
                            help="Space-separated rig IDs. If omitted, all rigs are used.")

    # -------------------------
    # VESSEL
    # -------------------------
    vessel_parser = subparsers.add_parser("vessel")
    vessel_parser.add_argument("publish_format", nargs="?", choices=["print", "put", "post", "mqtt", "kafka"],
                               default="print", help=publish_format_help)
    vessel_parser.add_argument("--ids", nargs="+", choices=["DLB", "DLT"], default=None,
                               help="Vessel engine side(s)")

    # -------------------------
    # WIND TURBINE
    # -------------------------
    wt_parser = subparsers.add_parser("wind-turbine")
    wt_parser.add_argument("publish_format", nargs="?", choices=["print", "post", "mqtt", "kafka"],
                           default="print", help=publish_format_help)
    wt_parser.add_argument("--ids", type=int, nargs="+",
                           choices=[i for i in range(1, 12) if i != 4], default=None,
                           help="Space-separated turbine IDs. If omitted, all turbines except 4.")

    # -------------------------
    # WIND TURBINE 2
    # -------------------------
    turbine_ids = []
    for farm_id in range(1, 3):
        turbine_ids.append(f"farm-{farm_id}")
        for turbine_id in range(1, 5) if farm_id == 1 else range(1, 3):
            turbine_ids.append(f"farm-{farm_id}/turbine-{turbine_id}")

    wt2_parser = subparsers.add_parser("wind-turbine2")
    wt2_parser.add_argument("publish_format", nargs="?", choices=["print", "post", "mqtt", "kafka", "opcua"],
                                default="print", help=publish_format_help)
    wt2_parser.add_argument("--ids", type=str, nargs="+", choices=turbine_ids, default=None,
                           help="Space-separated turbine IDs.")

    # -------------------------
    # PROVEIT
    # -------------------------
    proveit_parser = subparsers.add_parser("proveit")
    proveit_parser.add_argument("publish_format", nargs='?', choices=["print", "post", "mqtt", "kafka", "opcua"],
                                default="print", help=publish_format_help)
    proveit_parser.add_argument("--topics", type=str, nargs="+", default="#",
                                choices=["Enterprise A", "Enterprise A/Dallas/", "Enterprise A/Dallas/Line 1",
                                         "Enterprise A/Dallas/Site", "Enterprise A/opto22",
                                         "Enterprise A/opto22/Utilities/Air Dryers",
                                         "Enterprise A/opto22/Utilities/Building Power",
                                         "Enterprise A/opto22/Utilities/Compressors",
                                         "Enterprise A/opto22/Utilities/Electrical Panels",
                                         "Enterprise A/opto22/Utilities/Environmental",

                                         "Enterprise B", "Enterprise B/Metric", "Enterprise B/Site1",
                                         "Enterprise B/Site2", "Enterprise B/Site3",

                                         "Enterprise C",  "Enterprise C/chrom",  "Enterprise C/opto22",
                                         "Enterprise C/sub", "Enterprise C/sum", "Enterprise C/tff"],
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
    parser.add_argument("--skip-msg-client", type=bool, nargs='?', const=True, default=False,
                        help="Skip generating `run msg client` for POST / MQTT / OPC-Ua process")
    parser.add_argument("--skip-inserts", type=bool, nargs='?', const=True, default=False,
                        help="Only execute `run msg client` and skip insertion process (invalid for PUT)")

    return parser


def main():
    """
    Publish synthetic or file‑based data into AnyLog / EdgeLake.

    Use msg_client_generator.py to create policies and MQTT settings when
    publishing via POST or MQTT.

    USAGE
        python generator.py [data-source-original] [publish-format] [options]

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

    imports = _import_parser(data=args.data, skip_insert=args.skip_inserts, skip_msg_client=args.skip_msg_client)
    insert_fn = imports.get("insert")
    msg_fn = imports.get("msg_client")

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
    elif args.publish_format in ["PUT", "POST"] and args.control_conn and not args.data_conn:
        args.data_conn = args.control_conn
    # 4. Warning: missing args.control_conn, but there's data_conn
    elif args.publish_format not in ["MQTT", "OPCUA"] and not args.control_conn and args.data_conn: # warning only
        print(f"Missing `--control-conn` for {args.publish_format}, will not declare mapping or `msg client`")
    # 5. Exception: missing both control_conn and data_conn
    elif args.publish_format in ["POST", "mqtt", "kafka"] and not args.control_conn and not args.data_conn:
        raise argparse.ArgumentError(argument=None, message=f"publishing format {args.publish_format} requires missing connection information")


    # Define connection information
    control_conn = None
    data_conn    = None
    data_broker = None
    data_port = None
    data_user = None
    data_password = None
    is_rest = False
    if args.publish_format != "PRINT":
        if args.control_conn:
            broker, port, user, password = extract_credentials(args.control_conn)
            control_conn = RestClient(conn=f"{broker}:{port}", auth=(user, password), timeout=args.timeout)
        if args.data_conn:
            broker, port, data_user, data_password = extract_credentials(args.data_conn)
            if args.publish_format in ["POST", "PUT"]:
                data_conn = RestClient(conn=f"{broker}:{port}", auth=(data_user, data_password), timeout=args.timeout)
                is_rest = True
            elif args.publish_format == "MQTT":
                data_conn = MqttClient(host=broker, port=port, user=data_user, password=data_password, timeout=args.timeout)
            elif args.publish_format == "KAFKA":
                data_conn = KafkaClient(host=broker, port=port, user=data_user, password=data_password, timeout=args.timeout)
            elif args.publish_format == "OPCUA":
                data_conn = OpcuaServer(host=broker, port=port)

            data_broker = broker
            data_port = port


    # publish msg client and define data
    if args.data == "random":
        if control_conn is not None and args.publish_format in ["POST", "mqtt", "kafka"] and not args.skip_msg_client:
            msg_fn(conn=control_conn, broker=data_broker, port=data_port, user=data_user, password=data_password,
                           is_rest=is_rest)
        if not args.skip_inserts:
            insert_fn(method=args.publish_format, conn=data_conn, db_name=args.db_name, iterations=args.repeat, sleep=args.sleep)
    elif args.data == "rig":
        if control_conn is not None and args.publish_format in ["POST", "mqtt", "kafka"] and not args.skip_msg_client:
            rig_ids = args.ids[0] if len(args.ids) == 1 else None
            msg_fn(conn=control_conn, broker=data_broker, port=data_port, is_rest=is_rest, user=data_user,
                        password=data_password, rig_id=rig_ids)
        if not args.skip_inserts:
            insert_fn(method=args.publish_format, conn=data_conn, db_name=args.db_name, publish_topics=args.ids,
                     iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)
    elif args.data == "vessel": #
        if control_conn is not None and args.publish_format in ["POST", "mqtt", "kafka"] and not args.skip_msg_client:
            vessel_ids = args.ids[0] if len(args.ids) == 1 else None
            msg_fn(conn=control_conn, broker=data_broker, port=data_port, is_rest=is_rest,
                           user=data_user, password=data_password,
                           publish_topics=vessel_ids)
        if not args.skip_inserts:
            insert_fn(method=args.publish_format, conn=data_conn, db_name=args.db_name, publish_topics=args.ids, iterations=args.repeat,
                        sleep=args.sleep, offset_sleep=args.offset_sleep)
    elif args.data == "wind-turbine":
        if control_conn is not None and args.publish_format in ["POST", "mqtt", "kafka"] and not args.skip_msg_client:
            turbine_id = args.ids[0] if len(args.ids) == 1 else None
            msg_fn(conn=control_conn, broker=data_broker, port=data_port, user=data_user,
                                 password=data_password, is_rest=is_rest, turbine_id=turbine_id)
        if not args.skip_inserts:
            insert_fn(method=args.publish_format, conn=data_conn, db_name=args.db_name, publish_topics=args.ids,
                         iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)

    elif args.data == "wind-turbine2":
        if control_conn is not None and args.publish_format in ["POST", "mqtt", "kafka"] and not args.skip_msg_client:
            msg_fn(conn=control_conn, broker=data_broker, port=data_port, is_rest=is_rest,
                                     db_name=args.db_name, turbine_id=args.ids)
        elif not args.skip_inserts:
            insert_fn(method=args.publish_format, conn=data_conn, publish_topics=args.ids,
                          iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)
    elif args.data == "proveit": # conn=control_conn, broker=data_broker, port=data_port, is_rest=is_rest
        if control_conn is not None and args.publish_format in ["POST", "mqtt", "kafka"]:
            pass
        if not args.skip_inserts:
            insert_fn(method=args.publish_format, conn=data_conn, publish_topics=args.topics,
                         iterations=args.repeat, sleep=args.sleep, offset_sleep=args.offset_sleep)


if __name__ == "__main__":
    main()

