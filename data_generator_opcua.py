import asyncio
import argparse
import os
from data_generator.opcua_data_gen import describe_data
from data_publisher.opcua_server import run_opcua_server

DATA_FILE = os.path.join(os.path.dirname(__file__).split("data_generator")[0], "blobs", "opcua_describe_data.json")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str, default='0.0.0.0', help='OPC-UA server IP')
    parser.add_argument('port', type=int, default=4840, help='OPC-UA server port')
    parser.add_argument('--sleep', type=float, default=2, help='OPC-UA sleep rate')
    parser.add_argument('--db-name', type=str, default='test', help='logical database name')
    parser.add_argument('--create-data-size', type=bool, nargs='?', const=True, default=False, help='create data size for larger data set')
    parser.add_argument('--num-tables', type=int, default=20, help='number of tables for large data')
    parser.add_argument('--num-columns', type=int, default=100, help='total number of columns per table')
    parser.add_argument('--show-quality', type=bool, const=True, default=False, help='Quality (True/False) per numeric column')
    args = parser.parse_args()

    if args.create_data_size is True or not os.path.isfile(DATA_FILE):
        describe_data(num_tables=args.num_tables, num_columns=args.num_columns, include_quality=args.show_quality)

    asyncio.run(run_opcua_server(sleep_rate=args.sleep_rate, db_name=args.db_name))


if __name__ == '__main__':
    main()