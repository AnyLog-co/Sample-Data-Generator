import generic_protocol
import mqtt_protocol
import rest_protocols

def publish_data(payload:list, insert_process:str, conn:str=None, topic:str=None, rest_timeout:int=30,
                 dir_name:str=None, compress:bool=False, exception:bool=False):
    """
    Publish data based on the insert_process
    :args:
        payload:list - content to store
        insert_process:str - format to store content in
        conn:str - connection information
        topic:str - REST POST + MQTT topic
        rest_timeout:int - REST timeout
        dir_name:str - directory to store files in
        compress:bool - whether to compress content or not when stored in file
        exception:bool - whether to print error message(s)
    :params:
        status:bool
    """
    auth = ()
    if insert_process in ['put', 'post', 'mqtt']:
        if '@' in conn:
            
            auth, empty, conn = conn.split('@')
            auth = tuple(auth.split(':'))

    if insert_process == "print":
        generic_protocol.print_content(payloads=payload)
    elif insert_process == "file":
        status = generic_protocol.write_to_file(payloads=payload, data_dir=dir_name, compress=compress, exception=exception)
        if status is False and exception is False:
            print(f'Failed to store content into file')
    elif insert_process == 'put':
        status = rest_protocols.put_data(payloads=payload, conn=conn, auth=auth, timeout=rest_timeout,
                                         exception=exception)
        if status is False and exception is False:
            print(f'Failed to insert one or more batches of data into {conn} via PUT')
    elif insert_process == 'post':
        status = rest_protocols.post_data(payloads=payload, topic=topic, conn=conn, auth=auth, timeout=rest_timeout,
                                          exception=exception)
        if status is False and exception is False:
            print(f'Failed to insert one or more batches of data into {conn} via POST')
    elif insert_process == 'mqtt':
        broker, port = conn.split(':')
        username = ""
        password = ""
        if auth != ():
            username, password = auth

        status = mqtt_protocol.mqtt_process(payloads=payload, topic=topic, broker=broker, port=port, username=username,
                                            password=password, exception=exception)
        if status is False and exception is False:
            print(f'Failed to send MQTT message against connection {conn}')
