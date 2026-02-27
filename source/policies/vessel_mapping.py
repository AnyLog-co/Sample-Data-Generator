import copy
import posixpath
import json

from source.northbound.rest_calls import RestClient
from source.support import read_json_content
from source.support import get_files_by_url
from source.support import mapping_param
from source.policies.mappings import BASE_POLICY
from source.policies.mappings import SCHEMA
from source.northbound.rest_functions import declare_policy
from source.northbound.rest_functions import declare_msg_client
from source.support import _to_snake

DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)

TOPIC = "vessel-data"

for column in SCHEMA.get("_metadata"):
    BASE_POLICY["mapping"]["schema"][column] = {
        **({"type": "int"} if column in ["ip_index", "motor_id"] else {}),
        **({"type": "string"} if column in ["boat_name", "side"] else {}),
        "bring": f"[{column}]",
        **({"default": None} if column in ["ip_index", "motor_id"] else {}),
        **({"default": ""} if column in ["boat_name", "side"] else {})
    }



# , =None, port:int, is_rest:bool=False
def main(conn:RestClient|None, broker:str, port:int, is_rest:bool=False):
    topics = f"(name={TOPIC} "
    columns = {}
    for fname in VESSEL_FILES: # extract all columns and corresponding types
        # print(fname)
        url = posixpath.join(DATA_DIR, fname)
        for row_id in range(3):
            _, row = read_json_content(url=url, row_id=row_id, timestamp=None, german_format=False, timeout=30)
            for column in row:
                if column not in columns:
                    columns[column] = []
                if type(row.get(column)) not in columns.get(column):
                    columns[column].append(type(row.get(column)))

    for table in SCHEMA:
        if table != "_metadata":
            mapping_policy = copy.deepcopy(BASE_POLICY)
            mapping_policy["mapping"]["id"] = table.upper().replace('_', '-')
            mapping_policy["mapping"]["table"] = table
            topics += f" and policy={table.upper().replace('_', '-')}"
            for column in SCHEMA[table]:
                if columns.get(column) is not None:
                    data_type = mapping_param(columns.get(column))
                    mapping_policy["mapping"]["schema"].update({
                       column: {
                            "type": data_type,
                            "bring": f"[{column}]",
                            "default": None if data_type in ["int", "float"] else "",
                           "optional": True
                        }
                    })
            declare_policy(conn=conn, policy=mapping_policy)

    topics += ')'
    declare_msg_client(conn=conn, broker=broker, port=port, topics=topics, is_rest=is_rest)


    # for table in VESSEL_INFO:
    #     if table != "general":
    #         mapping_policy = copy.deepcopy(BASE_POLICY)
    #         mapping_policy["mapping"]["id"] = _to_snake(table).replace('_', '-')
    #         mapping_policy["mapping"]["table"] = _to_snake(table)
    #         for column in VESSEL_INFO.get("general"):
    #             mapping_policy["mapping"]["schema"].update({
    #                 _to_snake(name=column): {
    #                     "type": VESSEL_INFO.get("general").get(column),
    #                     "default": None if VESSEL_INFO.get("general").get(column) in ["float", "int"] else "",
    #                     "bring": f"[{column}]"
    #                 }
    #             })
    #         for column in VESSEL_INFO[table]:
    #             if columns.get(column):
    #
    #                 mapping_policy["mapping"]["schema"].update({
    #                     _to_snake(name=column): {
    #                         "type": data_type,
    #                         "default": None if data_type in ["float", "int"] else "",
    #                         "bring": f"[{column}]",
    #                         **({"optional": True} if VESSEL_INFO.get("general").get(column) is None else {})
    #                     }
    #                 })
    #
    #         policy_id = declare_policy(conn=conn, policy=mapping_policy)
    #         topics += f" and policy={policy_id}"
    #
    # topics += ')'
    # # print(topics)
    #



if __name__ == "__main__":
    conn = RestClient(conn="50.116.20.125:32149", auth=(), timeout=30 )
    # conn = RestClient(conn="10.0.0.78:7849", auth=(), timeout=30)
    main(conn=conn, broker="rest", port=32149 , is_rest=True)
    # main(conn=conn, broker="rest", port=7849 , is_rest=True)

