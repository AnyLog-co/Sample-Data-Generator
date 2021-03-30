def extract_conn_info(conn:str)->(str, str, str): 
    """
    The following code extracts connection information from conn
    :args: 
        conn:str - connection info (user@broker:passwd) 
    :params: 
        broker:str - MQTT broker info 
        user:str - MQTT user info 
        passwd:str - MQTT user password 
    :return: 
        broker, user and password info 
    """
    try: 
        broker = conn.split('@')[1].split(':')[0]
    except: 
        broker = conn 
    try: 
        user = conn.split('@')[0]
    except:
        user = '' 
    try: 
        passwd = conn.split(':')[1] 
    except:
        passwd = '' 

    return broker, user, passwd 

def format_machine_data(payload:dict, dbms:str, table_name:str)->dict: 
    """
    Format machine data 
    :args: 
        payload:dict - data to store 
        dbms:str - database name 
        table_name:str - table_name name
    :param:
        message:dict - MQTT object to send 
    :return: 
        MQTT object to send 
    :payload: 
    {"timestamp": "2021-03-26 18:17:08.872183", "hostname": "os-anylog-develop", "local_ip": "10.0.0.89", "remote_ip": "24.23.250.144", "boot_time": 90225.0942993164, "cpu_percentage": 36.4, "swap_memory": 0.0, "disk_usage": 0.0}
    """
    message = {
        'value': {
            'boot_time': payload['boot_time'],
            'cpu_percentage': payload['cpu_percentage'],
            'swap_memory': payload['swap_memory'],
            'disk_usage': payload['disk_usage']
        },
        'ts': payload['timestamp'],
        'metadata': {
            'company': dbms,
            'machine_name': table_name,
            'hostname': payload['hostname'], 
            'local_ip': payload['local_ip'], 
            'remote_ip': payload['remote_ip']
        }
    }
    return message 

def format_trig_data(payload:dict, dbms:str, table_name:str)->dict: 
    """
    Format sin/cos/rand data   
    :args: 
        payload:dict - data to store 
        dbms:str - database name 
        table_name:str - table_name name
    :param:
        message:dict - MQTT object to send 
    :return: 
        MQTT object to send 
    :payload: 
    {"timestamp": "2021-03-26 18:21:40.207469", "value": 0.0}
    """
    message = {
        'value': payload['value'],
        'ts': payload['timestamp'],
        'metadata': {
            'company': dbms,
            'machine_name': table_name,
        }
    }
    return message 

def format_network_data(payload:dict, dbms:str, table_name:str)->dict: 
    """
    Format percentagecpu and ping table_name data 
    :args: 
        payload:dict - data to store 
        dbms:str - database name 
        table_name:str - table name
    :param:
        message:dict - MQTT object to send 
    :return: 
        MQTT object to send 
    :payload: 
    {"timestamp": "2021-03-26 18:44:06.530026", "device_name": "Catalyst 3500XL", "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw", "value": 6}
    """
    message = {
        'value': payload['value'],
        'ts': payload['timestamp'],
        'metadata': {
            'company': dbms,
            'machine_name': table_name,
            'device_name': payload['device_name'], 
            'parentelement': payload['parentelement'],
            'webid': payload['webid']
        }
    }
    return message 


