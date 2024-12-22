import datetime
import random
import string
import uuid
import json

def __save_metadata(metadata):
    for table in metadata:
        if 'data' in metadata[table]:
            del metadata[table]['data']
    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

def __load_metadata():
    try:
        with open("metadata.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def __get_data(data_type:str):
    data = ""
    if data_type == 'timestamp':
        data = datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    if data_type == 'char':
        data = random.choice(string.ascii_lowercase.split())
    elif data_type == 'str':
        length = random.choice(list(range(5, 50)))
        for i in range(length):
            data += random.choice(string.ascii_lowercase.split())
    elif data_type == 'int':
        data = random.randint(0, 1000)
    elif data_type == 'float':
        rand_round = random.choice([0, 1, 3, 10])
        data = round(random.random() * 1000, rand_round)
        if rand_round == 0:
            data = int(data)
    elif data_type == 'bool':
        data = random.choice([True, False])
    elif data_type == 'uuid':
        data = uuid.uuid4().__str__()
    return data


def generate_tables(num_tables=40, num_columns=250, num_rows=10):
    content = __load_metadata()

    for table_idx in range(1, num_tables + 1):
        table_name = f"table_{table_idx}"
        if table_name not in content:
            content[table_name] = {'columns': {}, 'data': []}
            for col_idx in range(1, num_columns + 1):
                content[table_name]['columns'][f"Column_{col_idx}"] = random.choice(['char', 'str', 'int', 'float', 'bool', 'uuid'])
        if 'data' not in content[table_name]:
            content[table_name]['data'] = []

        for _ in range(num_rows):
            data = {'timestamp': __get_data('timestamp')}
            for col_name, col_type in content[table_name]['columns'].items():
                data[col_name] = __get_data(col_type)
            content[table_name]['data'].append(data)

    __save_metadata(content)
    return content


def main():
    tables = generate_tables(num_tables=1)
    for table_name, df in tables.items():
        file_name = f"{table_name}.csv"
        # df.to_csv(file_name, index=False)
        print(f"Saved {file_name}")

if __name__ == '__main__':
    main()



