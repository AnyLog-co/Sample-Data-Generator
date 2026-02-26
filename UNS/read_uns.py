import json
from source.northbound.rest_calls import RestClient
from source.northbound.rest_functions import declare_mapping_policy

def insert_uns(conn:RestClient, data_file:str, extra_params:list=None):
    with open(data_file, 'r') as f:
        for uns in json.load(f):
            name = uns.get("uns").get("name")
            namespace = uns.get("uns").get("namespace")
            if all("timestamp" not in param and (extra_params and param not in extra_params) for param in [name, namespace]):
                is_policy = check_policy(namespace)
                if is_policy == "[]":
                    parent_namespace = namespace.rsplit("/", 1)[0] if namespace.rsplit("/", 1)[0] != name else None
                    parent_policy_id = check_policy(namespace=parent_namespace)
                    declare_policy(policy=uns, parent_policy_id=parent_policy_id if parent_policy_id != "[]" else None)
