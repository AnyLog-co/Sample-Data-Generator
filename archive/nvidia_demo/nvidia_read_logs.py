import ast
import csv
import datetime
import json
import os
import re


FILE_NAME = os.path.join(os.path.expanduser(os.path.expandvars(os.path.dirname(__file__))),
                         'data/fclog.csv')

MESSAGE_INFO_KEYS = {
    'Succeeded': 'succeed',
    'URL': 'url',
    'UsingPostRenderer': 'using_post_renderer',
    'action': None,
    'caller': None,
    'checksumupdated': 'check_sum_updated',
    'component': None,
    'helmVersion': 'version',
    'info': None,
    'kustomizationCfg': 'kustomization_cfg',
    'kustomizationPath': 'kustomization_path',
    'kustomizeHook': 'kustomize_hook',
    'kustomizeHookPath': 'kustomize_hook_path',
    'latest': None,
    'loop': None,
    'msg': None,
    'name': None,
    'phase': None,
    'release': None,
    'resource': None,
    'revision': None,
    'targetNamespace': 'target_namespace',
    'ts': 'timestamp',
    'version': None,
    'warning': None,
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


def __extract_message_info(message_data:str)->dict:
    message_values = {}
    for value in message_data.split(" "):
        if "=" in value and value.split("=")[0].strip() in MESSAGE_INFO_KEYS:
            key = value.split("=")[0].strip()
            if MESSAGE_INFO_KEYS[key] is not None:
                key = MESSAGE_INFO_KEYS[key]
            if value.split("=")[-1].strip() != "":
                message_values[key] = value.split("=")[-1].strip()
    if 'info' in message_data:
        message_values['info'] = re.sub(r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}", "",
                                        message_data.split('info="')[-1].split('"')[0].strip())

    return message_values


def __extract_additional_details(additional_details:str, exception:bool=False)->dict:
    try:
        additional_details = ast.literal_eval(additional_details)
    except Exception as error:
        if exception is True:
            print(f"Failed to convert additional details from string to dict (Error: {error})")
    else:
        additional_details['remote_ip'] = additional_details['gl2_remote_ip']
        additional_details['remote_port'] = int(ast.literal_eval(additional_details['gl2_remote_port']))
        additional_details['message_size'] = float(ast.literal_eval(additional_details['gl2_accounted_message_size']))
        additional_details['message_id'] = additional_details['gl2_message_id']
        additional_details['source_input'] = additional_details['gl2_source_input']
        additional_details['accounted_message_size'] = float(ast.literal_eval(additional_details['gl2_accounted_message_size']))
        additional_details['pod'] = additional_details['pod_name']
        additional_details['namespace'] = additional_details['namespace_name']
        additional_details['container'] = additional_details['container_name']
        additional_details['source_node'] = additional_details['gl2_source_node']
        additional_details['id'] = additional_details['_id']


        del additional_details['gl2_remote_ip']
        del additional_details['gl2_remote_port']
        del additional_details['gl2_source_input']
        del additional_details['pod_name']
        del additional_details['namespace_name']
        del additional_details['container_name']
        del additional_details['gl2_source_node']
        del additional_details['_id']
        del additional_details['gl2_message_id']
        del additional_details['gl2_accounted_message_size']

    return additional_details


def __merge_data(dbms:str, table:str, timestamp:str, message_data:dict, additional_details:dict)->dict:
    generated_row = {
        "dbms": dbms,
        "table": table,
        "timestamp": timestamp
    }

    for key in message_data:
        generated_row[key] = message_data[key]

    if isinstance(additional_details, str):
        generated_row['additional_details'] = additional_details
    else:
        for key in additional_details:
            if key in generated_row and generated_row[key] != additional_details[key]:
                generated_row[f"{additional_details['component']}_{key}"] = additional_details[key]
            elif key not in generated_row:
                generated_row[key] = additional_details[key]

    return generated_row

def nvidia_helm_data(db_name:str, table:str='fleet_command', file_name:str=FILE_NAME, exception:bool=False)->list:
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
    """
    content = []
    keys = []
    csv_data = __read_data(file_name=file_name, exception=exception)
    if csv_data != []:
        for row in csv_data:
            if 'Date and Time' in row:
                timestamp = row['Date and Time']
            if 'Message' in row:
                message_data = __extract_message_info(message_data=row['Message'])
            if 'Additional Details':
                additional_details = __extract_additional_details(additional_details=row['Additional Details'],
                                                                  exception=exception)
            content.append(__merge_data(dbms=db_name, table=table, timestamp=timestamp, message_data=message_data,
                                        additional_details=additional_details))

    return content


if __name__ == '__main__':
    nvidia_helm_data(db_name='test', exception=True)