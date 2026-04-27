import argparse
from source.support import extract_credentials
from source.northbound.rest_calls import RestClient

from source.policies.rig_mapping import main as rig_mapping
from source.policies.vessel_mapping import main as vessel_mapping
from source.policies.wind_turbine_mapping import main as wind_turbine_mapping
from source.policies.random_mapping import main as random_mapping

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("conn", type=str, default=None, help="AnyLog REST connection for post requests")
    parse.add_argument("data", type=str, default=None, choices=["wind-turbine", "rig", "vessel", "random"],
                       help="Data source-original to create policies and `msg client` for")
    # parse.add_argument("publish_type", type=str, default=None, choices=["MQTT", "POST"],
    #                    help="Format data will be published")
    parse.add_argument("--broker", type=str, required=True, default="rest",
                       help="Broker / host IP address data would be sent to")
    parse.add_argument("--port", type=int, required=False, default=32149,
                       help="port associated with `msg client` broker")
    parse.add_argument("--is-rest", type=bool, nargs='?', const=True, default=False,
                       help="Data will be published via REST")
    parse.add_argument("--timeout", type=float, default=30, help="REST timeout")
    args = parse.parse_args()

    broker, port, user, password = extract_credentials(args.conn)
    conn = RestClient(conn=f"{broker}:{port}", auth=(user, password), timeout=args.timeout)
    args.is_rest = True if args.conn == "rest" else args.is_rest

    if args.data == "wind-turbine":
        wind_turbine_mapping(conn=conn, broker=args.broker, port=args.port, is_rest=args.is_rest)
    elif args.data == "rig":
        rig_mapping(conn=conn, broker=args.broker, port=args.port, is_rest=args.is_rest)
    elif args.data == "vessel":
        vessel_mapping(conn=conn, broker=args.broker, port=args.port, is_rest=args.is_rest)
    elif args.data == "random":
        random_mapping(conn=conn, broker=args.broker, port=args.port, is_rest=args.is_rest)


if __name__ == "__main__":
    main()
    