"""
Issue:

There should be a param in mapping policy called "config" (ex. timestamp, monitor_id, device)
If non-configs (ex. sensor_1 and sensor_3 ) are all null then do not insert row
"""

import datetime
import random

from source.northbound.rest_calls import RestClient
from source.northbound.rest_functions import check_policy
from source.northbound.rest_functions import declare_policy
from source.northbound.rest_functions import declare_msg_client
from source.northbound.rest_functions import publish_data

MAPPING = [
    {
      "mapping": {
        "id": "policy1",
        "dbms": "bring [dbms]",
        "table": "t1",
        "readings": "",
        "schema": {
          "__start__": {
            "script": ["set policy1_counter = 0"]
          },
          "timestamp": {
            "type": "timestamp",
            "default": "NOW()",
            "bring": "[timestamp]"
          },
          "monitor_id": {
            "type": "string",
            "bring": "[monitor_id]",
            "default": ""
          },
          "device": {
            "type": "string",
            "bring": "[device]",
            "default": ""
          },
          "sensor_1": {
            "type": "int",
            "bring": "[sensor_1]",
            "default": None,
            "script": ["if [sensor_1] then policy1_counter = incr !policy1_counter"]
          },
          "sensor_3": {
            "type": "float",
            "bring": "[sensor_3]",
            "default": None,
            "script": ["if [sensor_3] then policy1_counter = incr !policy1_counter"]
          },
          "__end__": {
            "script": ["if policy1_counter == 0 then return IGNORE_EVENT"]
          },
        }
      }
    },
    {
        "mapping": {
            "id": "policy2",
            "dbms": "bring [dbms]",
            "table": "t2",
            "readings": "",
            "schema": {
                "__start__": {
                    "script": ["set policy2_counter = 0"]
                },
                "timestamp": {
                    "type": "timestamp",
                    "default": "NOW()",
                    "bring": "[timestamp]"
                },
                "monitor_id": {
                    "type": "string",
                    "bring": "[monitor_id]",
                    "default": ""
                },
                "device": {
                    "type": "string",
                    "bring": "[device]",
                    "default": ""
                },
                "sensor_2": {
                    "type": "int",
                    "bring": "[sensor_2]",
                    "default": None,
                    "script": ["if [sensor_2] then policy2_counter = incr !policy2_counter"]
                },
                "sensor_4": {
                    "type": "float",
                    "bring": "[sensor_4]",
                    "default": None,
                    "script": ["if [sensor_4] then policy2_counter = incr !policy2_counter"]
                },
                "__end__": {
                    "script": ["if policy2_counter == 0 then return IGNORE_EVENT"]
                },
            }
        }
    },
]

BASE_COLUMNS = ["sensor_1", "sensor_2", "sensor_3", "sensor_4"]

BASE_DATA = {
    "DBL": "device_1",
    "DlT": "device_2"
}

TOPIC = "null-test"


def prep_node(conn:RestClient|None):
    topics = f"(name={TOPIC} "
    for policy in MAPPING:
        policy_id = policy.get('mapping').get('id')
        topics += f" and policy={policy_id}"

        is_policy = check_policy(conn=conn, policy_type="mapping", id=policy_id)
        if not is_policy or is_policy == "[]":
            declare_policy(conn=conn, policy=policy)

    topics += ')'
    declare_msg_client(conn=conn, broker="rest", port=7849, topics=topics, is_rest=True)


def main(conn: RestClient | None):
    payload = []

    for i in range(12):
        row = {
            "dbms": "anotherpeak",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "monitor_id": random.choice(list(BASE_DATA))
        }
        row["device"] = BASE_DATA[row["monitor_id"]]

        case_type = i % 3  # rotate through 0,1,2

        # -----------------------
        # CASE 1: All 4 full
        # -----------------------
        if case_type == 0:
            for index, column in enumerate(BASE_COLUMNS):
                if index < 2:
                    row[column] = random.randint(0, 100)
                else:
                    row[column] = random.random() * 100

        # -----------------------
        # CASE 2: All 4 present, 1–2 NULL
        # -----------------------
        elif case_type == 1:
            null_count = random.randint(1, 2)
            null_columns = random.sample(BASE_COLUMNS, null_count)

            for index, column in enumerate(BASE_COLUMNS):
                if column in null_columns:
                    row[column] = None
                else:
                    if index < 2:
                        row[column] = random.randint(0, 100)
                    else:
                        row[column] = random.random() * 100

        # -----------------------
        # CASE 3: Only 1–3 keys exist
        # -----------------------
        else:
            key_count = random.randint(1, 3)
            selected_columns = random.sample(BASE_COLUMNS, key_count)

            for column in selected_columns:
                index = BASE_COLUMNS.index(column)
                if index < 2:
                    row[column] = random.randint(0, 100)
                else:
                    row[column] = random.random() * 100

        payload.append(row)

    for row in payload:
        print(row)
        publish_data(
            method="POST",
            conn=conn,
            payload=row,
            topic=TOPIC,
            table_name=None,
            db_name=None
        )


if __name__ == "__main__":
    conn = RestClient(conn="50.116.20.125:32149")
    # conn = RestClient(conn="10.0.0.78:7849")
    prep_node(conn=conn)
    main(conn=conn)