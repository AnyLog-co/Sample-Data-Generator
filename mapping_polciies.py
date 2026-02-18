import argparse
from source.support import extract_credentials


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("conn", type=str, default=None, help="AnyLog REST connection for post requests")
    parse.add_argument("data", type=str, default=None, choices=["wind-turbine", "rig", "vessel"],
                       help="Data source to create policies and `msg client` for")
    parse.add_argument("publish_type", type=str, default=None, choices=["MQTT", "POST"],
                       help="Format data will be published")
    parse.add_argument("--broker", type=str, required=True, default="rest",
                       help="Broker / host IP address data would be sent to")
    parse.add_argument("--port", type=int, required=False, default=32149,
                       help="port associated with `msg client` broker")
    args = parse.parse_args()

    broker, port, user, password = extract_credentials(args.conn)
    if args.data == "wind-turbine":
        pass
    elif args.data == "rig":
        pass
    elif args.data == "vessel":
        pass

if __name__ == "__main__":
    main()
    