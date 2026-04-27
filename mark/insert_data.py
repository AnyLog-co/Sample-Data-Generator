import json
import requests
CONN = "129.212.178.167:32049"
DATA_FILE = "../UNS/rigs.json"


def _exec_request(method:str, headers:dict, payload:str|None=None):
    try:
        response = requests.request(method=method.upper(), url=f"http://{CONN}", headers=headers, data=payload)
        response.raise_for_status()
    except Exception as error:
        raise Exception(f"Failed to execute {method.upper()} against {CONN} (Error: {error})")

    return response


def check_policy(namespace:str):
    headers = {
        "command": f'blockchain get UNS where namespace="{namespace}" bring [*][id]',
        "User-Agent": "AnyLog/1.23",
    }
    response = _exec_request(method="GET", headers=headers, payload=None)
    return response.text


def declare_policy(policy:dict, parent_policy_id:str=None):
    headers = {
        "command": "blockchain insert where policy=!new_policy and local=true and master=!ledger_conn",
        "User-Agent": "AnyLog/1.23"
    }

    if parent_policy_id:
        policy["UNS"]["parent"] = parent_policy_id
    _exec_request(method="POST", headers=headers, payload=f"<new_policy={json.dumps(policy)}>")



def main():

    with open(DATA_FILE, 'r') as f:
        for uns in json.load(f):
            name = uns.get("UNS").get("name")
            namespace = uns.get("UNS").get("namespace")
            if all("timestamp" not in param and "rig_id" not in param for param in [name, namespace]):
                is_policy = check_policy(namespace)
                if is_policy == "[]":
                    parent_namespace = namespace.rsplit("/", 1)[0] if namespace.rsplit("/", 1)[0] != name else None
                    parent_policy_id = check_policy(namespace=parent_namespace)
                    declare_policy(policy=uns, parent_policy_id=parent_policy_id if parent_policy_id != "[]" else None)


if __name__ == "__main__":
    main()