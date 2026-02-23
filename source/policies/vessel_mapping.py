import copy
import posixpath


from source.northbound.rest_calls import RestClient
from source.northbound.rest_functions import declare_mapping_policy
from source.northbound.rest_functions import declare_msg_client
from source.support import read_json_content
from source.support import get_files_by_url
from source.support import _to_snake
from source.support import mapping_param
from source.policies.mappings import BASE_POLICY
from source.policies.mappings import VESSEL_INFO

DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)

TOPIC = "vessel-data"


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

    for table in VESSEL_INFO:
        if table != "general":
            mapping_policy = copy.deepcopy(BASE_POLICY)
            mapping_policy["mapping"]["id"] = _to_snake(table).replace('_', '-')
            mapping_policy["mapping"]["table"] = _to_snake(table)
            for column in VESSEL_INFO.get("general"):
                mapping_policy["mapping"]["schema"].update({
                    _to_snake(name=column): {
                        "type": VESSEL_INFO.get("general").get(column),
                        **({"default": ""} if VESSEL_INFO.get("general").get(column) == "string" else {}),
                        "bring": f"[{column}]"
                    }
                })
            for column in VESSEL_INFO[table]:
                if columns.get(column):
                    data_type  = mapping_param(columns.get(column))
                    mapping_policy["mapping"]["schema"].update({
                        _to_snake(name=column): {
                            "type": data_type,
                            **({"default": ""} if data_type == "string"  else {}),
                            **({"default": False} if data_type == "bool" else {}),
                            "bring": f"[{column}]"
                        }
                    })

            policy_id = declare_mapping_policy(conn=conn, policy=mapping_policy,
                                               table=mapping_policy.get("mapping").get("table"))
            topics += f" and policy={policy_id}"

    topics += ')'
    # print(topics)
    declare_msg_client(conn=conn, broker=broker, port=port, topics=topics, is_rest=is_rest)



if __name__ == "__main__":
    conn = RestClient(conn="50.116.20.125:32149", auth=(), timeout=30 )
    main(conn=conn, broker="rest", port=32149 , is_rest=True)

