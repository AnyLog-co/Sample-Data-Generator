import argparse
import random 
import time

from data_generators import machine_info, percentagecpu_sensor, ping_sensor, trig
from protocols import rest_protocol, local_store

def __validate_values(iteration:int, repeat:int, sleep:float)->bool: 
    """
    Validate values are within range
    :args: 
        iteration:int -  >= 0
        repeat:int -  >= 1
        sleep:float - >= 0 
    :param: 
        status:bool
    :return: 
        status
    """
    status = True 
    if not isinstance(iteration, int) or iteration < 0:
        print('Value %s is invalid for iteration' % iteration) 
        status = False 
    if not isinstance(repeat, int) or repeat < 1: 
        print('Value %s is invalid for repeat' % repeat) 
        status = False 
    if (not isinstance(sleep, float) and not isinstance(sleep, int)) or sleep < 0: 
        print(type(sleep))
        print('Value %s is invalid for sleep' % sleep) 
        status = False 

    return status 

def __table_name(sensor:str)->str:
    """
    convert sensor to table_name
    :args:
        senesor:str - sensor to generate data for 
    :param: 
        table_name:str - table name 
    :return: 
        table_name
    """
    table_name = ''
    if sensor == 'ping' or sensor == 'percentagecpu': 
        table_name = '%s_sensor' % sensor 
    else: 
        table_name = '%s_data' % sensor 

    return table_name

def get_data(sensor:str, row_count:int, frequency:float, sleep:float)->list: 
    """
    Based on sensor type get set values
    :args: 
        sensors:str - type of sensor [machine, ping, sin, cos, rand] 
        rows:int - number of data sets to generate for machine / ping sensor. All others have 30 rows by default 
        frequency:float - frequency by which to multiple th generated value 
        sleep:float - wait time between each row 
    :param: 
        rows:list - rows genenrated
    :return: 
        rows
    """
    rows = [] 
    if sensor == 'machine': 
        for row in range(row_count): 
            rows.append(machine_info.get_device_data())
            time.sleep(sleep) 
    elif sensor == 'ping': 
        for row in range(row_count): 
            rows.append(ping_sensor.get_ping_data(frequency)) 
            time.sleep(sleep) 
    elif sensor == 'percentagecpu': 
        for row in range(row_count): 
            rows.append(percentagecpu_sensor.get_percentagecpu_data(frequency)) 
            time.sleep(sleep) 
    elif sensor == 'sin':  
        rows = trig.sin_value(frequency, sleep)
    elif sensor == 'cos': 
        rows = trig.cos_value(frequency, sleep)
    elif sensor == 'rand': 
         rows = trig.rand_value(frequency, sleep)
    return rows 

def store_data(payloads:list, conn:str, dbms:str, table_name:str, store_type:str, mode:str, prep_dir:str, watch_dir:str, mqtt_conn:str, mqtt_port:int, mqtt_topic:str, al_broker:bool)->bool:
    """
    Store data
    :args: 
        payloads:list - Data to store 
        conn:str - IP + Port (required for REST only) 
        dbms:str - logical database name (required for REST + file) 
        table_name:str - logical table tname (required for REST + file)
        store_type:str - Format by which to store (print, file, REST) 
        mode:str - Format by which to send REST (file or streaming) 
        
        prep_dir:str - Directory to prep data in (file only) 
        watch_dir:dir - Directory data ready to be sent onto AnyLog (file only) 

        mqtt_conn:str - MQTT connection info (MQTT Only)
        mqtt_port:int - MQTT port (MQTT Only) 
        mqtt_topic:str - MQTT topic (MQTT Only)
        al_broker:bool - Whether to use AnyLog broker (MQTT only) 
    :param: 
        status:bool - status 
    """
    status = True 
    if store_type == 'rest': 
        status = rest_protocol.validate_connection(conn)
        if status == True: 
            status = rest_protocol.send_data(payloads, conn, dbms, table_name, mode)
    elif store_type == 'file': 
        status = local_store.file_store(payloads, dbms, table_name, prep_dir, watch_dir) 
    elif store_type == 'print': 
        status = local_store.print_store(payloads) 
    elif store_type == 'mqtt': 
        if status == True: 
            status = rest_protocol.mqtt_protocol(payloads, conn, dbms, table_name, mqtt_conn, mqtt_port, mqtt_topic)
    return status  

def main(): 
    """
    Based on the configuration set by a user, generate data and store it either to file, directly in AnyLog or print to screen
    :positional arguments:
        dbms       database name
        sensor     type of sensor to get data from    {machine,percentagecpu,ping,sin,cos,rand}
    :optional arguments:
        -h,  --help             show this help message and exit
        -c,  --conn             REST host and port                                                    (default: None)
        -f,  --store-format     format to get data                                                    (default: print)        {rest,file,print}
        -m,  --mode             insert type                                                           (default: streaming)    {file,streaming}
        -i,  --iteration        number of iterations. if set to 0 run continuesly                     (default: 1)
        -r,  --repeat           For machine & ping data number of rows to generate per iteration      (default: 10)
        -x,  --frequency        Value by which to multiply generated value(s)                         (default: 1) 
        -s,  --sleep            wait between insert                                                   (default: 0)
        -p,  --prep-dir         directory to prepare data in                                          (default: $HOME/AnyLog-Network/data/prep)
        -w,  --watch-dir        directory for data ready to be stored                                 (default: $HOME/AnyLog-Network/data/watch)
        -mc, --mqtt-conn        MQTT connection info                                                  (default: mqwdtklv@driver.cloudmqtt.com:uRimssLO4dIo)
        -mp, --mqtt-port        MQTT port 			       			              (default: 18975)
        -mt, --mqtt-topic       MQTT topic 							      (default: test)
        -ab, --al-broker        If MQTT broker is AnyLog                                              (default: false) 
    :param:
        table_name:str - based on the sensor type generate table_name 
        payloads:dict - data generated for a given sensor 
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('dbms',                 type=str,   default='sample_data', help='database name') 
    parser.add_argument('sensor',               type=str,   default='ping',        choices=['machine', 'percentagecpu', 'ping', 'sin', 'cos', 'rand'], help='type of sensor to get data from') 
    parser.add_argument('-c', '--conn',         type=str,   default=None,          help='REST host and port, use commas for multiple IPs and ports')
    parser.add_argument('-f', '--store-format', type=str,   default='print',       choices=['rest', 'file', 'print', 'mqtt'], help='format to get data') 
    parser.add_argument('-m', '--mode',         type=str,   default='streaming',   choices=['file', 'streaming'],             help='insert type') 
    parser.add_argument('-i', '--iteration',    type=int,   default=1,                                            help='number of iterations. if set to 0 run continuesly') 
    parser.add_argument('-x', '--frequency',    type=float, default=1,                                            help='Value by which to multiply generated value(s)') 
    parser.add_argument('-r', '--repeat',       type=int,   default=10,                                           help='For machine & ping data number of rows to generate per iteration') 
    parser.add_argument('-s', '--sleep',        type=float, default=0,                                            help='wait between insert') 
    parser.add_argument('-p', '--prep-dir',     type=str,   default='$HOME/AnyLog-Network/data/prep',             help='directory to prepare data in') 
    parser.add_argument('-w', '--watch-dir',    type=str,   default='$HOME/AnyLog-Network/data/watch',            help='directory for data ready to be stored') 
    parser.add_argument('-mc', '--mqtt-conn',   type=str,   default='mqwdtklv@driver.cloudmqtt.com:uRimssLO4dIo', help='MQTT connection info') 
    parser.add_argument('-mp', '--mqtt-port',   type=int,   default=18975,                                        help='MQTT port') 
    parser.add_argument('-mt', '--mqtt-topic',  type=str,   default='test',                                       help='MQTT topic')  
    parser.add_argument('-ab', '--al-broker',   type=bool,  default=False, nargs='?', const=True,                 help='If MQTT broker is AnyLog set configs accordingly') 
    args = parser.parse_args()
    
    if (args.sensor == 'machine' or args.sensor == 'ping' or args.sensor == 'percentagecpu') and args.store_format == 'mqtt': 
        print("MQTT isn't supported with sensor type: %s" % args.sensor) 
        exit(1) 

    # validate values 
    if not __validate_values(args.iteration, args.repeat, args.sleep): 
        print('Invalid Options') 
        exit(1)

    if args.conn == None and (args.store_format == 'rest' or args.store_format == 'mqtt'):
        print('Unable to send data via REST when conn is set to None') 
        exit(1) 

    table_name = __table_name(args.sensor) 

    if args.conn != None: 
        conns = args.conn.split(',') # convert conn(s) in to a list 
    else:
        conns = args.conn 

    conn = None 
    if args.iteration == 0: 
        payloads = get_data(args.sensor, args.repeat, args.frequency, args.sleep) 
        if conns != None: 
            conn = random.choice(conns) 
        store_data(payloads=payloads, conn=conn, dbms=args.dbms, table_name=table_name, store_type=args.store_format, mode=args.mode, prep_dir=args.prep_dir, watch_dir=args.watch_dir, mqtt_conn=args.mqtt_conn, mqtt_port=args.mqtt_port, mqtt_topic=args.mqtt_topic, al_broker=args.al_broker) 

    for row in range(args.iteration): 
        payloads = get_data(args.sensor, args.repeat, args.frequency, args.sleep) 
        if conns != None:
            conn = random.choice(conns) 
        store_data(payloads=payloads, conn=conn, dbms=args.dbms, table_name=table_name, store_type=args.store_format, mode=args.mode, prep_dir=args.prep_dir, watch_dir=args.watch_dir, mqtt_conn=args.mqtt_conn, mqtt_port=args.mqtt_port, mqtt_topic=args.mqtt_topic, al_broker=args.al_broker) 

if __name__ == '__main__': 
    main() 
