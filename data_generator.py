import argparse
import os
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PROTOCOLS)


def data_generators(data_generator:str, batch_repeat:int=10, batch_sleep:float=0.5, timezone:str='utc',
                    enable_timezone_range:bool=True, token:str=None, tag:str=None, initial_configs:bool=False,
                    data_dir:str=os.path.join(ROOT_PATH, 'data'), compress:bool=False, exception:bool=False)->dict:
    """
    Based on the parameters generate a data set
    :args:
        data_generator:str - which data set to generated
        batch_repeat:int - number of rows per batch
        batch_sleep:float - sleep time between rows or a specific batch
        timezone:str - whether to set the timezone in UTC or local
        enable_timezone_range:bool - whether or not to set timestamp within a "range"
        token:str - linode token
        tag:str - group of linode nodes to get data from. If not gets from all nodes associated to token
        initial_configs:bool - whether this is the first time the configs are being deployed
        data_dir:str - for data_generator type file directory containing data to read
        compress:bool - whether the content in data_dir is compressed
        exception:bool - whether or not to print error message(s)
    :params:
        payloads:dict - generated data
    :reeturn:
        payloads
    """
    if data_generator == 'linode':
        import linode
        payloads = linode.get_linode_data(token=token, tag=tag, initial_configs=initial_configs, timezone=timezone,
                                          enable_timezone_range=enable_timezone_range, exception=exception)
    elif data_generator == 'percentagecpu':
        import percentagecpu_sensor
        payloads = percentagecpu_sensor.get_percentagecpu_data(timezone=timezone,
                                                               enable_timezone_range=enable_timezone_range,
                                                               sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'ping':
        import ping_sensor
        payloads = ping_sensor.get_ping_data(timezone=timezone, enable_timezone_range=enable_timezone_range,
                                             sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'power':
        import power_company
        payloads = power_company.data_generator(timezone=timezone, enable_timezone_range=enable_timezone_range,
                                                sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'synchrophasor':
        import power_company_synchrophasor
        payloads = power_company_synchrophasor.data_generator(timezone=timezone,
                                                              enable_timezone_range=enable_timezone_range,
                                                              sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'trig':
        import trig
        payloads = trig.trig_value(timezone=timezone, enable_timezone_range=enable_timezone_range,
                                   sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'aiops':
        import customer_aiops
        payloads = customer_aiops.get_aiops_data(timezone=timezone, sleep=batch_sleep, repeat=batch_repeat)

    elif data_generator == 'file':
        import read_file
        payloads = read_file.read_data(dir_path=data_dir, compress=compress, exception=exception)

    return payloads


def store_data(protocol:str, payloads:dict, data_generator:str, dbms:str, conn:str, auth:str, timeout:float, topic:str,
               data_dir:str=os.path.join(ROOT_PATH, 'data'), compress:bool=False, exception:bool=False)->bool:
    """
    Store content based on the selected protocol(s)
    :args:
        protocol:str - format to save data
        payloads:dict - content to store
        data_generator:str - which data generated
        dbms:str - logical database to store data in
        conn:str - REST IP + Port or broker IP + Port
        auth:str - username, password
        timeout:float - REST timeout (in seconds)
        topic:str - MQTT / REST POST topic
        data_dir:str - for data_generator type file directory containing data to read
        compress:bool - whether the content in data_dir is compressed
        exception:bool - whether or not to print exceptions
    :params:
        table:str - table name
        broker:str - broker for MQTT
        port:str - port for MQTT
        username:str - username for MQTT
        password:str - password for MQTT
        mqtt_conn:paho.mqtt.client.Client - MQTT client connection
    """
    status = True
    table = ''
    if data_generator == 'ping':
        table = 'ping_sensor'
    elif data_generator == 'percentagecpu':
        table = 'percentagecpu_sensor'
    else:
        table = data_generator

    if protocol == 'print':
        import generic_protocol
        generic_protocol.print_content(data=payloads, dbms=dbms, table=table)
    if protocol == 'file':
        import generic_protocol
        if not generic_protocol.write_to_file(data=payloads, dbms=dbms, table=table, data_dir=data_dir, compress=compress,
                                        exception=exception):
            print('Failed to write data into file(s)')
            status = False
    elif protocol == 'put':
        from rest import put_data
        if not put_data(conn=conn, data=payloads, dbms=dbms, table=table, auth=auth, timeout=timeout, exception=exception):
            print('Failed to PUT data into %s' % conn)
            status = False
    elif protocol == 'post':
        from rest import post_data
        if data_generator == 'linode':
            # node_config & node_summary have a slightly different configuration
            for param in ['node_config', 'node_summary']:
                status = store_data(protocol='put', payloads=payloads[param], data_generator=param, dbms=dbms,
                                    conn=conn, auth=auth, timeout=timeout, topic=None, exception=exception)
                if status is True:
                    del payloads[param]
                else:
                    print('Failed to PUT data for %s against %s' % (param, conn))
        if status is True and not post_data(conn=conn, data=payloads, dbms=dbms, table=table, rest_topic=topic,
                                            exception=exception):
                print('Failed to POST data into %s' % conn)
                status = False
    elif protocol == 'mqtt':
        import mqtt
        broker, port = conn.rstrip().lstrip().replace(' ', '').split(':')
        user = ''
        password = ''
        if auth is not None:
            user, password = auth.rstrip().lstrip().replace(' ', '').split(',')
        mqtt_conn = mqtt.connect_mqtt_broker(broker=broker, port=port, username=user, password=password)
        if mqtt_conn is not None:
            status = mqtt.send_data(mqtt_client=mqtt_conn, topic=topic, data=payloads, dbms=dbms, table=table,
                                    exception=exception)
    elif protocol == 'kafka':
        import kafka_protocol as kafka
        servers = conn.split(',')
        kafka_conn = kafka.connect_kafka(servers=servers, exception=exception)
        if kafka_conn is not None:
            status = kafka.publish_data(producer=kafka_conn, topic=topic, data=payloads, dbms=dbms, table=table,
                                  exception=exception)

    return status


def main():
    """
    The following provides
    :positional arguments:
        conn                    IP:Port credentials for either REST, MQTT or Kafka      (default: 127.0.0.1:2049)
        data-generator:str      data set to generate content for        (default: trig)
            * file
            * linode - content from linode
            * percentagecpu sensor data
            * ping sensor data
            * power data
            * synchrophasor data
            * trig (default)
            * aiops
        protocol                format to save data                     (default: print)
            * post
            * put
            * mqtt
            * kafka
            * file
            * print (default)
        dbms                    logical database to store data in       (default: test)
    :optional arguments
        -h, --help                          show this help message and exit
        --repeat           REPEAT           number of time to repeat each batch, if 0 then run continuously
        --sleep            SLEEP            sleep time between each batch
        --batch-repeat     BATCH_REPEAT     number of rows per batch
        --batch-sleep      BATCH_SLEEP      sleep time between rows or a specific batch
        --topic            TOPIC            topic for MQTT or REST POST
        --timezone         TIMEZONE         Decide whether you want the timezone in UTC or local
            * utc   - actual UTC value
            * local - machine timestamp as UTC value
            * ET - +03:00 from UTC
            * BR - -03:00 from UTC
            * JP - +09:00 from UTC
            * WS - -09:00 from UTC
            * AU - +09:30 from UTC
            * IT - +01:00 from UTC
        --enable-timezone-range     ENABLE_TIMEZONE_RANGE   whether or not to set timestamp within a "range"
        --authentication   AUTHENTICATION   username, password
        --timeout TIMEOUT  REST             timeout (in seconds)
        --linode-token     LINODE_TOKEN     linode token
        --linode-tag       LINODE_TAG       group of linode nodes to get data from. If not gets from all nodes associated to token
        -e, -exception     EXCEPTION        whether or not to print exceptions to screen
    :params:
        payloads:dict - content to store
    """
    parser = argparse.ArgumentParser()
    # default params
    parser.add_argument('conn', type=str, default='127.0.0.1:2049', help='IP:Port credentials for either REST, MQTT or Kafka')
    parser.add_argument('data_generator', type=str, choices=['file', 'linode', 'percentagecpu', 'ping', 'power', 'synchrophasor', 'trig', 'aiops'], default='trig', help='data set to generate content for')
    parser.add_argument('protocol',       type=str, choices=['post', 'put', 'mqtt', 'kafka', 'file', 'print'], default='print', help='format to save data')
    parser.add_argument('dbms', type=str, default='test', help='Logical database to store data in')

    parser.add_argument('--repeat',       type=int,   default=1,   help='number of time to repeat  each batch, if 0 then run continuously')
    parser.add_argument('--sleep',        type=float, default=1,   help='sleep time between each batch')
    parser.add_argument('--batch-repeat', type=int,   default=10,  help='number of rows per batch')
    parser.add_argument('--batch-sleep',  type=float, default=0.5, help='sleep time between rows or a specific batch')

    parser.add_argument('--timezone', type=str, choices=['local', 'UTC', 'ET', 'BR', 'JP', 'WS', 'AU', 'IT'], default='local', help='timezone for generated timestamp(s)')
    parser.add_argument('--enable-timezone-range', type=bool, nargs='?', const=True, default=False, help='whether or not to set timestamp within a "range"')
    parser.add_argument('--authentication', type=str, default=None, help='username, password')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout (in seconds)')
    parser.add_argument('--topic', type=str, default=None, help='topic for either REST POST or MQTT')

    # files protocol options
    parser.add_argument('--store-dir', type=str, default=os.path.join(ROOT_PATH, 'data'), help='directory to store results in for file protocol')
    parser.add_argument('--read-dir', type=str, default=os.path.join(ROOT_PATH, 'data'), help='directory to read data to be sent')
    parser.add_argument('--compress', type=bool, nargs='?', const=True, default=False, help='Whether to compress create files, or decompress files being sent')

    # linode params
    parser.add_argument('--linode-token', type=str, default='ab21f3f79e22693bb33815772fd6a48fa91a0298e9052be0250a56fec7b4cc70', help='linode token')
    parser.add_argument('--linode-tag',   type=str, default=None, help='group of linode nodes to get data from. If not gets from all nodes associated to token')
    parser.add_argument('-e', '--exception', type=bool, nargs='?',     const=True, default=False, help='whether or not to print exceptions to screen')
    args = parser.parse_args()

    store_dir = os.path.expandvars(os.path.expanduser(args.store_dir))
    read_dir = os.path.expandvars(os.path.expanduser(args.read_dir))
    if not os.path.isdir(store_dir):
        os.makedirs(store_dir)
    if not os.path.isdir(read_dir) and args.data_generator == 'file':
        print(f'Failed to locate directory containing data to generate ({read_dir})')
        exit(1)

    if args.repeat == 0:
        while True:
            payloads = data_generators(data_generator=args.data_generator, batch_repeat=args.batch_repeat,
                                       batch_sleep=args.batch_sleep, timezone=args.timezone,
                                       enable_timezone_range=args.enable_timezone_range, token=args.linode_token,
                                       tag=args.linode_tag, initial_configs=True, data_dir=read_dir,
                                       compress=args.compress, exception=args.exception)
            if len(payloads) >= 1:
                store_data(protocol=args.protocol, payloads=payloads, data_generator=args.data_generator, dbms=args.dbms,
                           conn=args.conn, auth=args.authentication, timeout=args.timeout, topic=args.topic,
                           data_dir=write_dir, compress=args.compress, exception=args.exception)
            else:
                print('Failed to generate data')
            time.sleep(args.sleep)
    for i in range(args.repeat):
        payloads = data_generators(data_generator=args.data_generator, batch_repeat=args.batch_repeat,
                                   batch_sleep=args.batch_sleep, timezone=args.timezone,
                                   enable_timezone_range=args.enable_timezone_range, token=args.linode_token,
                                   tag=args.linode_tag, initial_configs=True, data_dir=read_dir, compress=args.compress,
                                   exception=args.exception)
        if len(payloads) >= 1:
            store_data(protocol=args.protocol, payloads=payloads, data_generator=args.data_generator, dbms=args.dbms,
                       conn=args.conn, auth=args.authentication, timeout=args.timeout, topic=args.topic,
                       data_dir=store_dir, compress=args.compress, exception=args.exception)
        else:
            print('Failed to generate data')
        time.sleep(args.sleep)

if __name__ == '__main__':
    main()