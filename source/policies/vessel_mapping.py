import copy
import json
import posixpath

from source.policies.mappings import BASE_POLICY
from source.policies.mappings import VESSEL_INFO
from source.support import get_files_by_url
from source.support import read_json_content
from source.support import mapping_policy_config
from source.northbound.rest_calls import RestClient
from source.northbound.rest_calls import declare_mapping_policy
from source.northbound.rest_calls import declare_msg_client
from source.support import _to_snake


DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)

TABLE = "vessel_data"
TOPIC = "vessel-data"



def main(conn:RestClient|None, broker:str, port:int, is_rest:bool=False):
    topics = []
    for tier in VESSEL_INFO:
        topic = f"(name={tier} and "
        mappings = []
        rows = []
        content = {}
        for file in VESSEL_FILES:
            if VESSEL_INFO[tier].get("file_id") in file:
                file_path = posixpath.join(DATA_DIR,  file)
                for row_id in range(10):
                    rows.append(read_json_content(url=file_path, row_id=row_id))

        for row in rows:
            for key in row:
                if key not in content:
                    content[key] = []
                if type(row.get(key)) not in content[key]:
                    content[key].append(type(row.get(key)))

        for table in VESSEL_INFO[tier]["tables"]:
            table_content = {}
            new_policy = copy.deepcopy(BASE_POLICY)
            new_policy["mapping"]["id"] = table.replace('_','-')
            new_policy["mapping"] ["table"] = table
            for sensor in VESSEL_INFO[tier]["tables"][table]:
                if content.get(sensor):
                    table_content[sensor] = content.get(sensor)
                elif sensor.endswith('*'):
                    for key in content:
                        if key.startswith(sensor.split('*')[0]):
                            table_content[key] = content.get(key)

            schema = mapping_policy_config(content=table_content, function=_to_snake)
            new_policy["mapping"]["schema"].update(schema)
            policy_id = declare_mapping_policy(conn=conn, policy=new_policy)
            topic += f" policy={policy_id} and"
        topics.append(topic.rsplit(" and", 1)[0] + ')')

    declare_msg_client(conn=conn, broker=broker, port=port, topics=topics, is_rest=is_rest)



# if __name__ == "__main__":
#     main()

