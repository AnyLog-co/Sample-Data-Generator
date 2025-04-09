from data_generator import get_columns
from __support__ import serialize_data


def create_policy()->dict:
    """
    Create a policy that accepts data from the 5 tables
    :params:
        tables:dict - taable name(s) and corresponding column / data type
        new_policy:dict - AnyLog policy
    :retun:
        new_policy
    """
    tables = {}
    for table in ['pp_pm', 'wp_digital', 'wp_analog', 'wwp_digital', 'wwp_analog']:
        tables[table] = get_columns(table)

    new_policy = {
        "mapping": {
            "id": "performance",
            "dbms": "bring [dbms]",
            "table": "bring [table]",
            "schema": {
                "timestamp": {
                    "type": "timestamp",
                    "bring": "[timestamp]",
                    "default": "now()"
                }
            }
        }
    }

    for table in tables:
        for column in tables[table]:
            if column not in new_policy['mapping']['schema']:
                if tables[table][column] == 'int':
                    new_policy['mapping']['schema'][column] = {
                        "type": "int",
                        "bring": f"[{column}]",
                        "optional": True
                    }
                elif tables[table][column] in ['decimal', 'float']:
                    new_policy['mapping']['schema'][column] = {
                        "type": "float",
                        "bring": f"[{column}]",
                        "optional": True
                    }
                elif tables[table][column] == 'boolean':
                    new_policy['mapping']['schema'][column] = {
                        "type": "int",
                        "bring": f"[{column}]",
                        "optional": True
                    }
                else:
                    new_policy['mapping']['schema'][column] = {
                        "type": "string",
                        "bring": f"[{column}]",
                        "optional": True
                    }
    return new_policy


def publish_policy():

