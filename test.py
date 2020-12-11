import time

from data_generators import machine_info, percentagecpu_sensor, ping_sensor, trig
from protocols import rest_protocol, local_store


def get_data(sensor:str, row_count:int, sleep:float)->list: 
    """
    Based on sensor type get set values
    :args: 
        sensors:str - type of sensor [machine, ping, sin, cos, rand] 
        rows:int - number of data sets to generate for machine / ping sensor. All others have 30 rows by default 
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
            rows.append(ping_sensor.get_ping_data()) 
            time.sleep(sleep) 
    elif sensor == 'sin':  
        rows = trig.sin_value(0)
    elif sensor == 'cos': 
        rows = trig.cos_value(0)
    elif sensor == 'rand': 
         rows = trig.rand_value(0)
    return rows 

def store_data(payloads:list, conn:str, dbms:str, table_name:str, store_type:str, rest_format:str, prep_dir:str, watch_dir:str)->bool:
    """
    Store data
    :args: 
        payloads:list - Data to store 
        conn:str - IP + Port (required for REST only) 
        dbms:str - logical database name (required for REST + file) 
        table_name:str - logical table tname (required for REST + file)
        store_type:str - Format by which to store (print, file, REST) 
        rest_format:str - Format by which to send REST (file or streaming) 
        prep_dir:str - Directory to prep data in (file only) 
        watch_dir:dir - Directory data ready to be sent onto AnyLog (file only) 
    :param: 
        status:bool - status 
    """
    status = True 
    if store_type == 'rest': 
        status = rest_protocol.send_rest(payloads, conn, dbms, table_name, rest_format)
    elif store_type == 'file': 
        status = local_store.file_store(payloads, dbms, table_name, prep_dir, watch_dir) 
    elif store_type == 'print': 
        status = local_store.print_store(payloads) 

    return status  

if __name__ == '__main__': 
    payloads = get_data('ping', 10, 0) 
    store_data(payloads=payloads, conn=None, dbms='sample_data', table_name='ping_sensor', store_type='file', rest_format=None, prep_dir='$HOME/data/prep', watch_dir='$HOME/data/watch') 
