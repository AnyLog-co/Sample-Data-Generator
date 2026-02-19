import copy
import json
import posixpath

from source.support import get_files_by_url
from source.support import read_turbine_data
from source.policies.mappings import BASE_POLICY
from source.policies.mappings import WIND_TURBINE_TABLES
from source.support import mapping_policy_config

DATA_DIR = "http://45.33.11.32/Sample-Data/wind-turbine/"
TURBINE_FILES = get_files_by_url(url=DATA_DIR)

TABLE = "wind_turbine"
TOPIC = "wind-turbine"

def main():
    content = {}
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
            print(json.dumps(new_policy, indent=2))
            exit(1)

if __name__ == "__main__":
    main()
