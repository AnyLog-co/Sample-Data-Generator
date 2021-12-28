import argparse
import os
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PROTOCOLS)


def data_generators(data_generator:str, batch_repeat:int=10, batch_sleep:float=0.5, timezone:str='utc',
                    token:str=None, tag:str=None, initial_configs:bool=False, exception:bool=False)->dict:
    """
    Based on the parameters generate a data set
    :args:
        data_generator:str - which data set to generated
        batch_repeat:int - number of rows per batch
        batch_sleep:float - sleep time between rows or a specific batch
        timezone:str - whether to set the timezone in UTC or local
        token:str - linode token
        tag:str - group of linode nodes to get data from. If not gets from all nodes associated to token
        initial_configs:bool - whether this is the first timee the configs are being deployed
        exception:bool - whether or not to print error message(s)
    :params:
        payloads:dict - generated data
    :reeturn:
        payloads
    """
    if data_generator == 'linode':
        import linode
        payloads = linode.get_linode_data(token=token, tag=tag, initial_configs=initial_configs, timezone=timezone,
                                          exception=exception)
    elif data_generator == 'percentagecpu':
        import percentagecpu_sensor
        payloads = percentagecpu_sensor.get_percentagecpu_data(timezone=timezone, sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'ping':
        import ping_sensor
        payloads = ping_sensor.get_ping_data(timezone=timezone, sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'power':
        import power_company
        payloads = power_company.data_generator(timezone=timezone, sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'synchrophasor':
        import power_company_synchrophasor
        payloads = power_company_synchrophasor.data_generator(timezone=timezone, sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'trig':
        import trig
        payloads = trig.trig_value(timezone=timezone, sleep=batch_sleep, repeat=batch_repeat)

    return payloads


def store_data(protocol:str, payloads:dict, data_generator:str, dbms:str, conn:str, auth:str, timeout:float, topic:str,
               exception:bool=False)->bool:
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
        import to_file
        to_file.print_content(data=payloads, dbms=dbms, table=table)
    if protocol == 'file':
        import to_file
        if not to_file.write_to_file(data=payloads, dbms=dbms, table=table, exception=exception):
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
        if status is True and not post_data(conn=conn, data=payloads, dbms=dbms, table=table, rest_topic=topic):
                print('Failed to POST data into %s' % conn)
                status = False
    elif protocol == 'mqtt':
        import mqtt
        broker, port = conn.rstrip().lstrip().replace(' ', '').split(':')
        user, password = auth.rstrip().lstrip().replace(' ', '').split(',')
        mqtt_conn = mqtt.connect_mqtt_broker(broker=broker, port=port, username=user, password=password)
        if mqtt_conn is not None:
            status = mqtt.send_data(mqtt_client=mqtt_conn, topic=topic, data=payloads, dbms=dbms, table=table, exception=exception)

    return status

def main():
    """
    The following provides
    :positional arguments:
        conn                    REST IP + Port or broker IP + Port      (default: 127.0.0.1:2049)
        data-generator:str      data set to generate content for        (default: trig)
            * linode - content from linode
            * percentagecpu sensor data
            * ping sensor data
            * power data
            * synchrophasor data
            * trig (default)
        protocol                format to save data                     (default: file)
            * post
            * put
            * mqtt
            * file (default)
            * print
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
    parser.add_argument('conn', type=str, default='127.0.0.1:2049', help='REST IP + Port or broker IP + Port')
    parser.add_argument('data_generator', type=str, choices=['linode', 'percentagecpu', 'ping', 'power', 'synchrophasor', 'trig'], default='trig', help='data set to generate content for')
    parser.add_argument('protocol',       type=str, choices=['post', 'put', 'mqtt', 'file', 'print'], default='file', help='format to save data')
    parser.add_argument('dbms', type=str, default='test', help='Logical database to store data in')

    # repeat / sleep params
    parser.add_argument('--repeat',       type=int,   default=1,   help='number of time to repeat  each batch, if 0 then run continuously')
    parser.add_argument('--sleep',        type=float, default=1,   help='sleep time between each batch')
    parser.add_argument('--batch-repeat', type=int,   default=10,  help='number of rows per batch')
    parser.add_argument('--batch-sleep',  type=float, default=0.5, help='sleep time between rows or a specific batch')

    parser.add_argument('--timezone', type=str, choices=['local', 'UTC', 'ET', 'BR', 'JP', 'WS', 'AU', 'IT'], default='local', help='timezone for generated timestamp(s)')
    parser.add_argument('--authentication', type=str, default=None, help='username, password')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout (in seconds)')
    parser.add_argument('--topic', type=str, default=None, help='topic for either REST POST or MQTT')

    # linode params
    parser.add_argument('--linode-token', type=str, default='ab21f3f79e22693bb33815772fd6a48fa91a0298e9052be0250a56fec7b4cc70', help='linode token')
    parser.add_argument('--linode-tag',   type=str, default=None, help='group of linode nodes to get data from. If not gets from all nodes associated to token')
    parser.add_argument('-e', '--exception', type=bool, nargs='?',     const=True, default=False, help='whether or not to print exceptions to screen')
    args = parser.parse_args()

    payloads = data_generators(data_generator=args.data_generator, batch_repeat=args.batch_repeat,
                               batch_sleep=args.batch_sleep, timezone=args.timezone, token=args.linode_token,
                               tag=args.linode_tag, initial_configs=True)
    if len(payloads) >= 1:
        store_data(protocol=args.protocol, payloads=payloads, data_generator=args.data_generator, dbms=args.dbms,
                   conn=args.conn, auth=args.authentication, timeout=args.timeout, topic=args.topic, exception=args.exception)
    else:
        print('Failed to generate data')


if __name__ == '__main__':
    main()