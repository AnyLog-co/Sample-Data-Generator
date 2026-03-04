import random
import posixpath

from source.policies.mappings import BASE_POLICY
from source.support import get_files_by_url
from source.support import read_csv_content
from source.northbound.rest_calls import RestClient
from source.northbound.rest_functions import declare_msg_client
from source.northbound.rest_functions import declare_policy
from source.support import mapping_policy_config

DATA_DIR = "http://45.33.11.32/Sample-Data/rig-data/"
RIG_FILES = get_files_by_url(url=DATA_DIR)

TOPIC = "rig-data"


def main(conn:RestClient|None, broker:str, port:int, is_rest:bool=False):
    BASE_POLICY["mapping"]["id"] = TOPIC

    # read_file
    content = {}
    for row_id in range(10):
        row = read_csv_content(posixpath.join(DATA_DIR, random.choice(RIG_FILES)), row_id=row_id)
        for key in row:
            if key not in content:
                content[key] = []
            elif type(row.get(key)) not in content[key]:
                content[key].append(type(row.get(key)))

    schema = mapping_policy_config(content=content)
    if schema:
        BASE_POLICY["mapping"]["schema"].update(schema)

    declare_policy(conn=conn, policy=BASE_POLICY)
    declare_msg_client(conn=conn, broker=broker, port=port, is_rest=is_rest,
                       topics=f"(name={TOPIC} and policy={TOPIC})")

