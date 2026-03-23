import copy
import posixpath

from source.support import get_files_by_url
from source.policies.mappings import BASE_POLICY
from source.policies.mappings import WIND_TURBINE_TABLES
from source.northbound.rest_functions import declare_msg_client
from source.northbound.rest_functions import declare_policy
from source.northbound.rest_calls import RestClient
from source.support import read_json_content
from source.support import mapping_policy_config


DATA_DIR = "http://45.33.11.32/Sample-Data/wind-turbine/"
TURBINE_FILES = get_files_by_url(url=DATA_DIR)

TABLE = "wind_turbine"
TOPIC = "wind-turbine"

LOCAL_BASE_POLICY = copy.deepcopy(BASE_POLICY)

def main(conn:RestClient|None, broker:str, port:int, is_rest:bool=False, user:str=None, password:str=None,
         turbine_id:str|None=None):
    content = {}
    topics = f"(name={TOPIC}/# and" if turbine_id is None else f"(name={TOPIC}/turbine-{turbine_id} and"
    for fname in TURBINE_FILES:
        file_path = posixpath.join(DATA_DIR, fname)
        for row_id in range(5):
            row = read_json_content(url=file_path, row_id=row_id, timestamp=None, german_format=True)
            # row = read_turbine_data(file_path, row_id=row_id)
            for key in row:
                if key not in content:
                    content[key] = []
                if type(row.get(key)) not in content[key]:
                    content[key].append(type(row.get(key)))

    for table in WIND_TURBINE_TABLES:
        if table != "identity":
            table_content = {}
            new_policy = copy.deepcopy(LOCAL_BASE_POLICY)
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
            policy_id = declare_policy(conn=conn, policy=new_policy)
            topics += f" policy={policy_id} and"

    topics = topics.rsplit(" and", 1)[0] + ')'
    print(topics)
    declare_msg_client(conn=conn, broker=broker, port=port, user=user, password=password, is_rest=is_rest, topics=topics)


# if __name__ == "__main__":
#     main()
