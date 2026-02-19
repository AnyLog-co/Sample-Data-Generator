import json
import requests

class RestClient:
    def __init__(self, conn:str, auth:tuple=None, timeout:float=60):
        self.url = f"http://{conn}"
        self.auth = auth
        self.timeout = timeout

    def __execute_command(self, method:str, headers:dict, payload=None):
        if (isinstance(payload, list) and isinstance(payload[0], dict)) or isinstance(payload, dict):
            payload = json.dumps(payload)
        try:
            response = requests.request(method=method.upper(), url=self.url, headers=headers, auth=self.auth,
                                        timeout=self.timeout, data=payload)
        except Exception as error:
            raise Exception(f"Failed to execute {method.upper()} against {self.url} (Error: {error})")
        return response

    def publish_data(self, headers:dict, payload, method:str="post"):
        return self.__execute_command(method=method.upper(), headers=headers, payload=payload)
        
    def get_data(self, headers:dict):
        response = self.__execute_command(method="GET", headers=headers, payload=None)

        try:
            return response.json()
        except Exception:
            return response.text



def get_file_content(url:str=None, timeout:float=30):
    response = None
    try:
        response = requests.get(url=url, timeout=timeout)
        response.raise_for_status()
    except Exception as error:
        raise Exception(f"Failed to get content from {url} (Error: {error})")

    return response

def declare_mapping_policy(conn:RestClient, policy:dict):
    policy_id = policy.get("mapping").get("id")
    get_headers = {
        "command": f"blockchain get mapping where id={policy_id}",
        "User-Agent": "AnyLog/1.23"
    }
    publish_headers = {
        "command": "blockchain insert where policy=!new_policy and local=true and master=!ledger_conn",
        "User-Agent": "Anylog/1.23"
    }

    response = conn.get_data(headers=get_headers)
    index = 0
    while not response or response == "[]":
        if index > 0:
            raise ConnectionError(f"Failed to publish policy against {conn.url}")
        new_policy = f"<new_policy={json.dumps(policy)}>"
        conn.publish_data(headers=publish_headers, payload=new_policy, method="POST")
        response = conn.get_data(headers=get_headers)
        index += 1


def declare_msg_client(conn:RestClient, broker:str, port:int, topics:str, is_rest:bool=True):
    check_msg_client = {
        "command": f"get msg client where topic={topics.split('name=', 1)[-1].split('and', 1)[0].strip()}",
        "User-Agent": "AnyLog/1.23"
    }
    declare_msg_client_header = {
        "command": f"run msg client where broker={broker} and log=false and topic={topics}",
        "User-Agent": "AnyLog/1.23"
    }

    if broker not in ["rest", "local"] and port:
        declare_msg_client_header["command"] += f" and port={port}"
    if broker  == "rest" or is_rest is True:
        declare_msg_client_header["command"] += f" and user-agent=anylog"

    response = conn.get_data(headers=check_msg_client)
    if response.strip() in ["No message client subscriptions"]:
        # print(declare_msg_client_header["command"])
        conn.publish_data(headers=declare_msg_client_header, payload=None, method="POST")
    else:
        print(response)