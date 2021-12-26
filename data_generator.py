import argparse
import os
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('protocols', 1)[0]
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PROTOCOLS)


def data_generators(data_generator:str, batch_repeat:int=10, batch_sleep:float=0.5, token:str=None, tag:str=None,
                    initial_configs:bool=False)->dict:
    """
    Based on the parameters generate a data set
    :args:
        data_generator:str - which data set to generated
        batch_repeat:int - number of rows per batch
        batch_sleep:float - sleep time between rows or a specific batch
        token:str - linode token
        tag:str - group of linode nodes to get data from. If not gets from all nodes associated to token
        initial_configs:bool - whether this is the first timee the configs are being deployed
    :params:
        payloads:dict - generated data
    :reeturn:
        payloads
    """
    if data_generator == 'linode':
        import linode
        payloads = linode.get_linode_data(token=token, tag=tag, initial_configs=initial_configs)
    elif data_generator == 'percentagecpu':
        import percentagecpu_sensor
        payloads = percentagecpu_sensor.get_percentagecpu_data(sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'ping':
        import ping_sensor
        payloads = ping_sensor.get_ping_data(sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'power':
        import power_company
        payloads = power_company.data_generator(sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'synchrophasor':
        import power_company_synchrophasor
        payloads = power_company_synchrophasor.data_generator(sleep=batch_sleep, repeat=batch_repeat)
    elif data_generator == 'trig':
        import trig
        payloads = trig.trig_value(sleep=batch_sleep, repeat=batch_repeat)

    return payloads

def store_data(protocol:str, payloads:dict, data_generator:str, dbms:str, conn:str, auth:str, timeout:float,
                   topic:str=None):
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
    :params:
        table:str - table name
        broker:str - broker for MQTT
        port:str - port for MQTT
        username:str - username for MQTT
        password:str - password for MQTT
    """
    table = ''
    if data_generator == 'ping':
        table = 'ping_sensor'
    elif data_generator == 'percentagecpu':
        table = 'percentagecpu_sensor'
    else:
        table = data_generator

    if protocol == 'post' or protocol == 'put':
        import rest
        if auth is not None:
            auth = tuple(auth.replace(' ', '').split(','))
    elif protocol == 'mqtt':
        import mqtt
        username = None
        password = None
        broker, port = conn.replace(' ', '').split(':')
        if auth is not None:
            username, password = auth.replace(' ', '').split(',')

    if protocol == 'file':
        import to_file
        to_file.write_to_file(data=payloads, dbms=dbms, table=table)
    elif protocol == 'post':
        rest.post_data(conn=conn, data=payloads, dbms=dbms, table=table, rest_topic=topic, auth=auth, timeout=timeout)
    elif protocol == 'put':
        rest.put_data(conn=conn, data=payloads, dbms=dbms, table=table, auth=auth, timeout=timeout)
    elif protocol == 'mqtt':
        mqtt.mqtt_data(broker=broker, port=port, topic=topic, data=payloads, dbms=dbms, table=table, username=username,
                       password=password)

def main():
    """
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
        dbms                    logical database to store data in       (default: test)
    :optional arguments
        -h, --help                          show this help message and exit
        --batch-repeat     BATCH_REPEAT    number of rows per batch
        --batch-sleep      BATCH_SLEEP     sleep time between rows or a specific batch
        --topic            TOPIC           topic for MQTT or REST POST
        --linode-token     LINODE_TOKEN    linode token
        --linode-tag       LINODE_TAG      group of linode nodes to get data from.
                                            If not gets from all nodes associated to token
        --authentication   AUTHENTICATION   username, password
        --timeout TIMEOUT  REST             timeout (in seconds)
    :params:
        payloads:dict - content to store
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, default='127.0.0.1:2049', help='REST IP + Port or broker IP + Port')
    parser.add_argument('data_generator', type=str, default='trig', help='data set to generate content for',
                        choices=['linode', 'percentagecpu', 'ping', 'power', 'synchrophasor', 'trig'])
    parser.add_argument('protocol', type=str, choices=['post', 'put', 'mqtt', 'file'], default='file',
                          help='format to save data')
    parser.add_argument('dbms', type=str, default='test', help='Logical database to store data in')
    parser.add_argument('--batch-repeat', type=int, default=10,     help='number of rows per batch')
    parser.add_argument('--batch-sleep',  type=float, default=0.5, help='sleep time between rows or a specific batch')
    parser.add_argument('--linode-token', type=str, default='ab21f3f79e22693bb33815772fd6a48fa91a0298e9052be0250a56fec7b4cc70',
                        help='linode token')
    parser.add_argument('--linode-tag', type=str, default=None,
                        help='group of linode nodes to get data from. If not gets from all nodes associated to token')
    parser.add_argument('--authentication', type=str, default=None, help='username, password')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout (in seconds)')
    args = parser.parse_args()

    if args.protocol == 'post' or args.protocol == 'mqtt':
        import mqtt_client
        if protocol == 'post':
            conn = 'rest:%s' % conn.replace(' ', '').split(':')[-1]
        mqtt_client.declare_mqtt_client(conn=conn, data_generator=args.data_generator, auth=args.auth,
                                        timeout=args.timeout)


    payloads = data_generators(data_generator=args.data_generator, batch_repeat=args.batch_repeat, batch_sleep=args.batch_sleep,
                               token=args.linode_token, tag=args.linode_tag, initial_configs=True)
    if 'node_config' in payloads:
        store_data(protocol='put', payloads=payloads['node_config'], data_generator='node_config', dbms=args.dbms,
               conn=args.conn, auth=args.authentication, timeout=args.timeout, topic=args.data_generator)
        del payloads['node_config']
    if 'node_summary' in payloads:
        store_data(protocol='put', payloads=payloads['node_summary'], data_generator='node_summary', dbms=args.dbms,
               conn=args.conn, auth=args.authentication, timeout=args.timeout, topic=args.data_generator)
        del payloads['node_summary']
    store_data(protocol=args.protocol, payloads=payloads, data_generator=args.data_generator, dbms=args.dbms,
               conn=args.conn, auth=args.authentication, timeout=args.timeout, topic=args.data_generator)

if __name__ == '__main__':
    main()