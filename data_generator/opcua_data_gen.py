import asyncio
import datetime
import json
import os
import random
import string
import uuid
import shutil

DATA_FILE = os.path.join(os.path.dirname(__file__).split("data_generator")[0], "blobs", "opcua_describe_data.json")

class PlaceholderVariable:
    def __init__(self):
        self.value = None

    def set_value(self, value):
        self.value = value

    def __repr__(self):
        return f"PlaceholderVariable(value={self.value})"
        # return self.value

def large_data(data, db_name):
    """Process data to ensure all values are serializable."""
    for table_name, table_data in data.items():
        for column, value in table_data.items():
            if isinstance(value, PlaceholderVariable):
                table_data[column] = value.value  # or value.value if that's appropriate
    data['dbms'] = db_name
    return data


def __copy_file():
    if os.path.isfile(DATA_FILE):
        try:
            shutil.copyfile(DATA_FILE, DATA_FILE.replace("json","json.old"))
        except Exception as error:
            raise Exception(f"Failed to create backup for {DATA_FILE} (Error: {error})")



# -- Functions for data description -- #
def describe_data(num_tables:int=20, num_columns:int=100, include_quality:bool=False):
    """
    Generate configuration for data flowing into OPC-UA server.
    """
    __copy_file()
    data = {}
    for table in range(num_tables):
        table_name = f"table_{table + 1}"
        data[table_name] = {}
        for column in ["timestamp", "device_id"]:
            data[table_name][column] = {}
            if column == "timestamp":
                data[table_name][column]["type"] = "datetime"
            elif column == "device_id":
                data[table_name][column]["value"] = uuid.uuid4().__str__()

        column_count = 0
        while column_count < num_columns:
            col_name = f"column_{column_count + 1}"
            col_type = random.choice(["string", "bool", "int", "float"])
            data[table_name][col_name] = {"type": col_type}
            if col_type in ["int", "float"]:
                data[table_name][col_name]["min"] = random.randint(1, 500)
                data[table_name][col_name]["max"] = random.randint(501, 1000)
            elif col_type == "string":
                data[table_name][col_name]["length"] = random.randint(1, 10)
            column_count += 1
            if col_type in ["bool", "int", "float"] and include_quality is True:
                column_count += 1

    with open(DATA_FILE, "w") as f:
        f.write(json.dumps(data, indent=4))
# -- Functions for data description -- #


def read_description(describe_data_file):
    """Read the JSON description file."""
    with open(describe_data_file, "r") as f:
        return json.loads(f.read())

async def get_column_data(column, props, include_quality: bool = False):
    """Generate data for a single column asynchronously."""
    if column in ["timestamp", "device_id"]:
        return None  # Skip timestamp and device_id

    col_type = props["type"]
    result = {}

    if col_type == "bool":
        result[column] = random.choice([True, False, None])
        if include_quality:
            result[f"quality_{column}"] = "NOk" if result[column] is None else "Ok"
    elif col_type in ["int", "float"]:
        value = round(random.uniform(props["min"], props["max"]), 3)
        result[column] = int(value) if col_type == "int" else value
        if include_quality:
            result[f"quality_{column}"] = (
                "Ok"
                if 0.75 * ((props["min"] + props["max"]) / 2)
                <= value
                <= 1.25 * ((props["min"] + props["max"]) / 2)
                else "Nok"
            )
    elif col_type == "string":
        length = props["length"]
        result[column] = "".join(random.choices(string.ascii_letters, k=length))

    return result

async def generate_row_data(data_describe, include_quality:bool=False):
    """Generate a single row of data."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    device_id = data_describe["device_id"]["value"]

    columns = [column for column in data_describe if column not in ["timestamp", "device_id"]]
    tasks = [get_column_data(column, data_describe[column], include_quality) for column in columns]
    results = await asyncio.gather(*tasks)

    row = {"timestamp": timestamp, "device_id": device_id}
    for result in results:
        if result:
            row.update(result)

    return row


async def configuration_data():
    data_describe = read_description(DATA_FILE)

    # Initialize table_variables with an appropriate structure for each table_name
    table_variables = {
        table_name: {
            column: PlaceholderVariable()  # Replace with an appropriate class or logic
            for column in table_desc.keys()
        }
        for table_name, table_desc in data_describe.items()
    }

    for table_name, table_desc in data_describe.items():
        row_data = await generate_row_data(table_desc, False)

        # Update each variable
        for column, value in row_data.items():
            if column in table_variables[table_name]:
                table_variables[table_name][column].set_value(value)
    return table_variables


if __name__ == '__main__':
    asyncio.run(configuration_data())
