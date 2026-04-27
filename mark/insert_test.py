"""
Issues:
1. SQL formating issue
    # sample data
    {"int_column": 1, "float_column": 3.14, "str_column": "hello"}
    {"int_column": null, "float_column": 3.14, "str_column": "hello"}
    {"int_column": 1, "float_column": null, "str_column": "hello"}
    {"int_column": 1, "float_column": 3.14, "str_column": ""}

    # expected
    INSERT INTO t1(int_column, float_column, str_column) VALUES
       (1, 3.14, "hello"),
       (NULL, 3.14, "hello")
       (3, NULL, "hello")
       (4, 3.14, "");

    #  actual
    INSERT INTO t1(int_column, float_column, str_column) VALUES
       (1, 3.14, "hello"),
       (, 3.14, "hello")
       (3, , "hello")
       (4, 3.14, "");

2. In mapping, when I only specify "optional", I'm getting en error:
    The key 'default' (derived from policy 'dummy-mapping') is missing in JSON object

3. In mapping, when I specify `default: None`, then there's an issue with "storing" the blockchain
"""
import datetime
import json
import requests

CONN = "50.116.20.125:32149"
TOPIC = "dummy-mapping"
POLICY = {
   "mapping": {
      "id": TOPIC,
      "dbms": "anotherpeak",
      "table": "t1",
      "readings": "",
      "schema": {
          "timestamp": {
              "type": "timestamp",
              "bring": "[timestamp]",
              "default": "now()"
          },
          "int_column": {
              "type": "int",
              "bring": "[int_column]",
              "default": None
          },
          "float_column": {
              "type": "float",
              "bring": "[float_column]",
              "default": None
          },
          "str_column": {
              "type": "string",
              "bring": "[str_column]",
              "default": "",
          }
      }
   }
}


DATA = [
    {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "int_column": 1,    "float_column": 3.14,   "str_column": "hello"},
    {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "float_column": 3.14,   "str_column": "hello"},
    {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "int_column": 1,    "float_column": None,   "str_column": "hello"},
    {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "int_column": 1,    "float_column": 3.14,   "str_column": ""},
]

def _exec_request(method:str, headers:dict, payload:str|None=None):
    try:
        response = requests.request(method=method.upper(), url=f"http://{CONN}", headers=headers, data=payload)
        response.raise_for_status()
    except Exception as error:
        raise Exception(f"Failed to execute {method.upper()} against {CONN} (Error: {error})")

    return response

def declare_policy():
    get_headers = {
        "command": "blockchain get mapping where id=dummy-mapping",
        "User-AGent": "AnyLog/1.23"
    }

    response = _exec_request(method="GET", headers=get_headers)
    is_policy = 0
    while response.text == "[]":
        if is_policy > 0:
            raise Exception(f"Failed to declare policy on blockchain")
        headers = {
            "command": "blockchain insert where policy=!new_policy and local=true",
            "User-Agent": "AnyLog/1.23"
        }
        payload = f"<new_policy={json.dumps(POLICY)}>"
        _exec_request(method="POST", headers=headers, payload=payload)
        response = _exec_request(method="GET", headers=get_headers)
        is_policy += 1

def declare_mqtt():
    get_headers = {
        "command": f"get msg client where topic={TOPIC}",
        "User-Agent": "AnyLog/1.23"
    }
    response = _exec_request(method="GET", headers=get_headers)
    if not (response.text.strip() in ["No message client subscriptions", "No such client subscription"]):
        return

    headers = {
        "command": f"run msg client where broker=rest and log=false and user-agent=anylog and topic=(name={TOPIC} and policy={TOPIC})",
        "User-Agent": "AnyLog/1.23"
    }
    _exec_request(method="POST", headers=headers, payload=None)

def publish_data(method:str):
    headers = {
        **({
            "type": "json",
            "dbms": "anotherpeak",
            "table": "t1",
            "mode": "streaming",
            "Content=Type": "text/plain"
        } if method.upper() == "PUT" else {}),
        **({
            "command": "data",
            "topic": TOPIC,
            "User-Agent": "AnyLog/1.23",
            "Content-Type": "text/plain"
        } if method.upper() == "POST" else {})
    }

    _exec_request(method=method.upper(), headers=headers, payload=json.dumps(DATA))


if __name__ == "__main__":
    # declare_policy()
    # declare_mqtt()
    publish_data(method="POST")