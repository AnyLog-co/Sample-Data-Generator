import copy
import json
import posixpath

from source.support import get_files_by_url
from source.policies.mappings import BASE_POLICY
from source.policies.mappings import WIND_TURBINE_TABLES
from source.support import mapping_policy_config
from source.northbound.rest_calls import RestClient

DATA_DIR = "http://45.33.11.32/Sample-Data/wind-turbine/"
TURBINE_FILES = get_files_by_url(url=DATA_DIR)

TABLE = "wind_turbine"
TOPIC = "wind-turbine"

def main(conn:RestClient|None, broker:str, port:int, is_rest:bool=False):
    content = {}
    topics = f"(name={TOPIC} and"
    for fname in TURBINE_FILES:
        file_path = posixpath.join(DATA_DIR, fname)
        for row_id in range(5):
            row = read_turbine_data(file_path, row_id=row_id)
            for key in row:
                if key not in content:
                    content[key] = []
                if type(row.get(key)) not in content[key]:
                    content[key].append(type(row.get(key)))

    for table in WIND_TURBINE_TABLES:
        if table != "identity":
            table_content = {}
            new_policy = copy.deepcopy(BASE_POLICY)
            new_policy["mapping"]["id"] = table.replace('_', "-")
            new_policy["mapping"]["table"] = table
            new_policy["mapping"]["schema"].update({
                "turbine_id": {
                    "type": "int",
                    "bring": "[turbine_id]"
                },
                "alias": {
                    "type": "string",
                    "default": "",
                    "bring": "[alias]"
                }
            })
            for key, value in WIND_TURBINE_TABLES[table].items():
                if content.get(value):
                    table_content[key] = content.get(value)

            schema =  mapping_policy_config(content=table_content)
            new_policy["mapping"]["schema"].update(schema)
            policy_id = declare_mapping_policy(conn=conn, policy=new_policy)
            topics += f" policy={policy_id} and"

    topics = topics.rsplit(" and", 1)[0] + ')'
    declare_msg_client(conn=conn, broker=broker, port=port, is_rest=is_rest, topics=topics)


# if __name__ == "__main__":
#     main()
