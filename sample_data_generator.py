import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_type", type=str,
                        choices=['ping', 'percentagecpu', 'node_insight', 'syslogs', 'images', 'cars', 'people'],
                        default='ping', help='type of data to insert into AnyLog')
    parser.add_argument("insert_process", type=str, choices=['print', 'file', 'put', 'post', 'mqtt'], default='print',
                        help='format to store data')
    parser.add_argument('db_name', type=str, default='new_company', help='logical database to ')