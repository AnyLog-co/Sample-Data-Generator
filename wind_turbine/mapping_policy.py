import copy
import locale
locale.setlocale(locale.LC_NUMERIC, "de_DE.UTF-8") # configure code to use German formatting

from source.rest_calls import RestClient
from source.support import declare_policy



MAPPING_POLICY = {
    "mapping": {
        "id": "",
        "dbms": "wind_turbine",
        "table": "wind_turbine",
        "readings": "",
        "schema": {
            "turbine_id": { # turbine_id
                "type": "int",
                "bring": "[Anlage]"
            },
            "timestamp": { # timestamp
                "type": "timestamp",
                "bring": "[Zeit]",
                "default": "now()"
            },
            "alias": { # turbine_alias
                "type": "string",
                "bring": "[Alias]"
            }
        }
    }
}

# def __read_line(read_file:str):
#     if not read_file:
#         raise FileNotFoundError("Failed to locate file to generate policies from")
#
#     # extract line
#     try:
#         sample_data = None
#         with open(read_file, mode='r', encoding="utf-8-sig") as f:
#             for line in f:
#                 line = line.strip()
#                 if not line:
#                     continue
#                 return json.loads(line)
#         if not sample_data:
#             raise ValueError(f"No valid JSON found in {read_file}")
#     except Exception as error:
#         raise Exception(f"Failed to read content in file {read_file} (Error: {error})")

def generate_mapping_policy(conn:RestClient=None):
    """
    Declare mapping policy for wind turbine data

    1. read first row in JSON
    2. declare tables and MQTT policy
    3. declare uns policies
    """
    policies = []

    # Generate mapping policies and print table columns
    for table in TABLES:
        mapping_policy = copy.deepcopy(MAPPING_POLICY)
        mapping_policy["mapping"]["id"] = table.replace("_", "-")
        mapping_policy["mapping"]["table"] = table

        print(f"\nTable: {table}")
        for column in TABLES[table]:
            column_name = column.split(' Ø ')[0].split('[')[0].strip().lower().replace('.','').replace(' ', '_')
            mapping_policy["mapping"]["schema"][column_name] = {
                "type": "float",
                "bring": f"[{TABLES.get(table).get(column)}]"
            }

        declare_policy(conn=conn, policy=mapping_policy)
        # print(json.dumps(mapping_policy, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    generate_mapping_policy(conn=None)


