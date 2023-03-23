import ast
import csv
import datetime
import json
import os

FILE_NAME = os.path.join(os.path.expanduser(os.path.expandvars(os.path.dirname(__file__))), 'fclog.csv')

DETAILS = {
    'app': None,
    'gl2_accounted_message_size': 'message_size',
    'release': None,
    'gl2_remote_ip': 'ip',
    'gl2_remote_port': 'port',
    'streams': None,
    'gl2_message_id': 'message_id',
    'source': None,
    'gl2_source_input': 'source_input',
    'pod_name': 'pod',
    'namespace_name': 'namespace',
    'system': None,
    'container_name': None,
    'location': None,
    'gl2_source_node': 'source_node',
    '_id': 'id'
}


def __read_data(file_name:str=FILE_NAME, exception:bool=False)->csv.DictReader:
    """
    Read content in file
    :args:
        file_name:str - file (with path to read
        exception:bool - whether to print exceptions
    :params:
        file_path:sr  - full path of file
        content:csv.DictReader - content in file
    :return:
        content
    """
    file_path = os.path.expanduser(os.path.expandvars(file_name))
    file_content = []
    if os.path.isfile(file_path):
        try:
            with open(file_path, encoding ='utf-8') as cfile:
                try:
                    # return csv.DictReader(cfile)
                    for row in csv.DictReader(cfile):
                        file_content.append(row)
                except Exception as error:
                    if exception is True:
                        print(f"Failed to extract content from {file_name} (Error: {error})")
        except Exception as error:
            if exception is True:
                print(f"Failed to open {file_name} (Error: {error})")
    elif exception is True:
        print(f"Failed to locate {file_name}")

    return file_content


def __extract_message(dbms:str, table:str, message:str, timestamp:str)->dict:
    """
    Format content for message information & timestamp
    :args:

    """
    return {
        'dbms': dbms,
        'table': table,
        "timestamp": timestamp,
        "component": message.split("component=")[-1].split("version")[0].strip(),
        "version": message.split("version=")[-1].split("info")[0].strip(),
        "caller": message.split("caller=")[-1].split("component")[0].strip(),
        "info": message.split('info="')[-1].split('"')[0],
        "targetNamespace": message.split("targetNamespace=")[-1].split("release=")[0].strip(),
        "release": message.split("release=")[-1]
    }


def __extract_additional_details(base_information:dict, additional_details:str, exception:bool=False):
    try:
        additional_details = ast.literal_eval(additional_details)
    except Exception as error:
        if exception is True:
            print(f"Failed to convert content into dictionary (Error: {error})")
        base_information['additional_details'] = additional_details
    else:
        for key in additional_details:
            if key in DETAILS and DETAILS[key] is None:
                base_information[key] = additional_details[key]
            elif key in DETAILS and DETAILS[key] is not None:
                base_information[DETAILS[key]] = additional_details[key]
            elif key not in base_information:
                print(key, additional_details[key])

        base_information['port'] = int(ast.literal_eval(base_information['port']))
        base_information['message_size'] = float(ast.literal_eval((base_information['message_size'])))

    return base_information


def nvidia_helm_data(db_name:str, table:str=None, file_name:str=FILE_NAME, exception:bool=False)->list:
    """
    Given an fclog.csv file (NVIDIA Helm) generate dictionary values to be stored in AnyLog.
    The default file has about 27,600 rows between "2022-05-25 00:10:08.857000" and "2022-05-30 01:10:15.208000"
    :args:
        file_name:str - file to read
        exception:bool - whether to print exception
    :params:
        csv_data:list - raw data from file
        content:list - data from file formatted to be used by AnyLog
        base_information;dict - individual rows of data to be stored
    :return:
        content
    :sample output:
    {
        "timestamp": "2022-05-30T01:10:15.208Z",
        "component": "helm",
        "version": "v3",
        "caller": "helm.go:69",
        "info": "beginning wait for 6 resources with timeout of 27777h46m39s",
        "targetNamespace": "egx-system",
        "release": "helm-operator",
        "app": "helm-operator",
        "message_size": 500.0,
        "ip": "127.0.0.1",
        "port": 55826,
        "streams": "[000000000000000000000001]",
        "message_id": "01G4986YESDCAD5H88HE7SW8AZ",
        "source": "system-1.egx.nvidia.com",
        "source_input": "624b89d37a58035d78e001fd",
        "pod": "helm-operator-654dffb688-c5sxl",
        "namespace": "helm",
        "system": "system-1",
        "container_name": "flux-helm-operator",
        "location": "system-2",
        "source_node": "28f73eb7-1879-450a-a538-2c8eede22877",
        "id": "43489e8b-dfb5-11ec-8504-e6df01411171"
    }
    """
    content = []
    if table in [None, ""]:
        table = 'fclog'
    csv_data = __read_data(file_name=file_name, exception=exception)
    if csv_data != []:
        for row in csv_data:
            base_information = __extract_message(dbms=db_name, table=table, message=row['Message'],
                                                 timestamp=row['Date and Time'])
            if table is None:
                base_information['table'] = 'fclog'
            content.append(__extract_additional_details(base_information=base_information,
                                                        additional_details=row['Additional Details'],
                                                        exception=exception))

    return content

