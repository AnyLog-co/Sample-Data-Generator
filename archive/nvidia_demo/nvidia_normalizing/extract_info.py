import ast

DEFAULT_PARAMS = {
    "helm": ["line", "timestamp", "component", "version", "info", "target_namespace", "release"],
    "release": ["line", "timestamp", "component", "release", "target_namespace", "resource", "helm_version", "using_post_renderer", "info", "action", "phase", "checksum_updated", "error", "warning", "succeeded", "revision"],
    "postrender": ["line", "timestamp", "component", "kustomization_hook", "kustomization_hook_path", "kustomization_config", "kustomization_path", "release", "target_namespace", "resource", "helm_version"],
    "logwriter": ["line", "timestamp", "info"],
    "checkpoint": ["line", "timestamp", "component", "msg", "latest", "url"],
    "operator": ["line", "timestamp", "component", "info"],
    "main": ["line", "timestamp", "exiting...", "component", "info"],
    "git": ["line", "timestamp", "component", "info"],
    "server": ["line", "timestamp", "component", "info"],
    "repository": ["line", "timestamp", "component", "version", "info", "name", "url", "error"],
    "status": ["line", "timestamp", "component", "loop", "err"]
}


def __extract_message(message:str)->dict:
    """
    Given a message as string - convert to dictionary
    :example:
        Input - 2022-05-30T01:10:15.208742319Z stderr F ts=2022-05-30T01:10:15.208700783Z caller=helm.go:69 component=helm version=v3 info=\"beginning wait for 6 resources with timeout of 27777h46m39s\" targetNamespace=egx-system release=edge-logging
        Output - {
            "timestamp":  "2022-05-30T01:10:15.208700783Z",
            "caller": "helm.go:69",
            "component": "helm",
            "version": "v3",
            "info": "beginning wait for 6 resources with timeout of 27777h46m39s",
            "namesapce": "egx-system",
            "release": edge-logging
        }
    :args:
        message:str - content to convert
    :params:
        content_dict:dict - converted message
    :return:
        content_dict
    """
    content_dict = {}
    content = message.split("=")
    for i in range(len(content)):
        if i == 0:
            key = content[i].split(" ")[-1]
        elif i == len(content) - 1:
            content_dict[key] = content[i]
        else:
            content_dict[key] = content[i].replace(content[i].split(" ")[-1], "").rstrip().lstrip().replace('"', "")
            key = content[i].split(" ")[-1]
    return content_dict


def extract_message(db_name:str, message:str)->dict:
    """
    Given a message - convert its content into a dictionary and "make it pretty"
    :args:
        message:str - message to convert
    :params:
        content_dict:dict - results from __extract_message
        complete_dict:dict - completed dictionary
    :return:
        complete_dict
    """
    content_dict = __extract_message(message=message)

    complete_dict = {
        'dbms': db_name,
        'table': '',
        'line': '',
    }
    # Validate basic information exists
    if 'caller' in content_dict:
        caller = content_dict.pop('caller').split(':')
        complete_dict['table'] = caller[0].split('.go')[0]
        try:
            complete_dict['line'] = int(caller[1])
        except: 
            complete_dict['line'] = caller[1]
    else:
        return {}

    # Insert  content_dict into compelete dict
    for key in content_dict:
        if key == 'ts':
            timestamp = content_dict[key].replace('"', "").rstrip().lstrip().replace('T', ' ').replace('Z', '')
            ts, sub_seconds = timestamp.split('.')
            complete_dict['timestamp'] = ts + "." + sub_seconds[:6]
        elif key == "UsingPostRenderer":
            complete_dict['using_post_renderer'] = content_dict[key].replace('"', "").rstrip().lstrip()
        elif key == "checksumupdated":
            complete_dict['checksum_updated'] = content_dict[key].replace('"', "").rstrip().lstrip()
        elif 'exiting' in key:
            complete_dict['exiting'] = content_dict[key].replace('"', "").rstrip().lstrip()
        elif key == "helmVersion":
            complete_dict['helm_version'] = content_dict[key].replace('"', "").rstrip().lstrip()
        elif key == "kustomizationCfg":
            complete_dict['kustomization_config'] = content_dict[key].replace('"', "").rstrip().lstrip()
        elif key == "kustomizationPath":
            complete_dict["kustomization_path"] = content_dict[key].replace('"', "").rstrip().lstrip()
        elif key == "kustomizeHook":
            complete_dict["kustomization_hook"] = content_dict[key].replace('"', "").rstrip().lstrip()
        elif key == "kustomizeHookPath":
            complete_dict["kustomization_hook_path"] = content_dict[key].replace('"', "").rstrip().lstrip()
        elif key == "targetNamespace":
            complete_dict['target_namespace'] = content_dict[key].replace('"', "").rstrip().lstrip()
        elif any(x.isdigit() for x in str(key)) is False:
            complete_dict[key.lower()] = content_dict[key].replace('"', "")

    # Add missing params
    for param in DEFAULT_PARAMS[complete_dict['table']]:
        if param not in complete_dict or complete_dict[param] == '':
            complete_dict[param] = None

    return complete_dict


def extract_additional_details(content:dict)->dict:
    """
    Given additional content, extract relevent infromation
    :example:
        Input-
        {
            "app": "helm-operator",
            "gl2_accounted_message_size": "500.0",
            "release": "helm-operator",
            "gl2_remote_ip": "127.0.0.1",
            "gl2_remote_port": "55826.0",
            "streams": "[000000000000000000000001]",
            "gl2_message_id": "01G4986YESDCAD5H88HE7SW8AZ",
            "source": "system-1.egx.nvidia.com",
            "gl2_source_input": "624b89d37a58035d78e001fd",
            "pod_name": "helm-operator-654dffb688-c5sxl",
            "namespace_name": "helm",
            "component": "helm",
            "system": "system-1",
            "container_name": "flux-helm-operator",
            "location": "system-2",
            "gl2_source_node": "28f73eb7-1879-450a-a538-2c8eede22877",
            "_id": "43489e8b-dfb5-11ec-8504-e6df01411171"
        }
        Output -
        { details: {
            "node_id": "28f73eb7-1879-450a-a538-2c8eede22877",
            "source": "system-1.egx.nvidia.com",
            "system": "system-1",
            "location": "system-2",
            "ip": "127.0.0.1",
            "port": 55826,
            "app_id": "43489e8b-dfb5-11ec-8504-e6df01411171",
            "app": "helm-operator",
            "release": "helm-operator",
            "pod": "helm-operator-654dffb688-c5sxl",
            "namespace": "helm",
            "container": "flux-helm-operator",
        }}
    :args:
        content:dict - content to extract information from
    :params:
        formatted_content:dict - extracted content
    :return:
        formatted_content
    """
    complete_content = None
    try:
        content = ast.literal_eval(content)
    except:
        pass
    else:
        if isinstance(content, dict):
            complete_content = {
                "app": content['app'],
                "app_release": content['release'],
                "source": content['source'],
                "system": content['system'],
                "pod_name": content['pod_name'],
                "namespace": content['namespace_name'],
                "app_component": content['component'],
                "container": content['container_name'],
                "location": content['location'],
                "node_id": content['_id']
            }
            for param in content:
                if 'remote_ip' in param:
                    complete_content['remote_ip'] = content[param]
                elif 'remote_port' in param:
                    try:
                        complete_content['remote_port'] = int(float(content[param]))
                    except:
                        complete_content['remote_port'] = content[param]
                elif 'message_id' in param:
                    complete_content['message_id'] = content[param]
                elif 'source_input' in param:
                    complete_content['source_input'] = content[param]
                elif 'source_node' in param:
                    complete_content['source_node'] = content[param]


    return complete_content
