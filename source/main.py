import argparse
import asyncio

from source.northbound.opcua import OpcuaServer
from source.southbound.random_data import main as rand_data

OPCUA = {
    "rand": 4841,
}

async def opcua_main(generator:str, db_name:str, iterations:int, wait_time:float, standalone_value:bool):
    conn = OpcuaServer(host="0.0.0.0", port=OPCUA[generator])
    await conn.connect()

    # run the sync data generator in a thread executor
    # so it doesn't block the event loop
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None,
        lambda: rand_data(method="OPCUA", conn=conn, db_name=db_name,
                          iterations=iterations, sleep=wait_time, standalone_value=False, loop=loop)
    )

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("generator", type=str, default="rand", choices=["rand"], help="data generator option")
    parse.add_argument("--method", type=str, default="print", help="how to publish data",
                       choices=["print", "put", "mqtt", "post", "kafka", "opcua"], )
    parse.add_argument("--conn", type=str, default="127.0.0.1:32149",
                       help="MQTT or REST connection {user}:{password}:{ip}{port} if OPC-UA then connection is based on generator")
    parse.add_argument("--db-name", type=str, default="mydb", help="logical database name")
    parse.add_argument("--iterations", type=int, default=10,
                       help="Number of iterations - if 0 run continuously")
    parse.add_argument("--wait-time", type=float, default=1, help="wait time between data sets (in seconds)")
    parse.add_argument("--standalone-values", type=bool, nargs='?', const=True, default=False,
                       help="If data is in JSON format or list of JSONs, then publish each value under its own subtopic")
    args = parse.parse_args()

    conn = None
    args.method = args.method.upper()

    if args.method == "opcua":
        asyncio.run(opcua_main(generator=args.generator, db_name=args.db_name, iterations=args.iterations,
                               wait_time=args.wait_time, standalone_value=args.standalone_values))

    elif args.generator == "rand":
        rand_data(method=args.method, conn=conn, db_name=args.db_name, iterations=args.iterations,
                  sleep=args.wait_time, standalone_value=args.standalone_values, loop=None)




if __name__ == "__main__":
    main()

