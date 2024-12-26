import asyncio
import datetime
import json
import random
import string
import uuid
import requests

TOTAL_INSERTS = 0
data = {}

DESCRIBE_DATA = "describe_data.json"


# -- describe data --
def describe_data():
    for table in range(25):
        data[f'table_{table + 1}'] = {}
        for column in ['timestamp', 'device_id', 'insert_id']:
            data[f'table_{table + 1}'][column] = {}
            if column == 'timestamp':
                data[f'table_{table + 1}'][column]['type'] = 'datetime'
            elif column == 'device_id':
                data[f'table_{table + 1}'][column]['value'] = uuid.uuid4().__str__()
            else:
                data[f'table_{table + 1}'][column]['type'] = 'string'
        for column in range(397):
            data[f'table_{table + 1}'][f'column_{column + 1}'] = {
                "type": random.choice(['string', 'bool', 'int', 'float'])
            }
            if data[f'table_{table + 1}'][f'column_{column + 1}']['type'] in ['int', 'float']:
                data[f'table_{table + 1}'][f'column_{column + 1}']['min'] = random.choice(list(range(1, 500)))
                data[f'table_{table + 1}'][f'column_{column + 1}']['max'] = random.choice(list(range(499, 1000)))
            elif data[f'table_{table + 1}'][f'column_{column + 1}']['type'] == 'string':
                data[f'table_{table + 1}'][f'column_{column + 1}']['length'] = random.choice(list(range(1, 10)))

    with open(DESCRIBE_DATA, 'w') as f:
        f.write(json.dumps(data, indent=4))


# -- describe data --

def read_description():
    with open(DESCRIBE_DATA, 'r') as f:
        return json.load(f)


def get_data(data_describe):
    output = {}
    timestamp = None
    device_id = None
    insert_id = None

    for column in data_describe:
        if column == 'timestamp':
            timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        elif column == 'device_id':
            device_id = data_describe[column]['value']
        elif column == 'insert_id':
            insert_id = uuid.uuid4().__str__().replace("-", "")
        elif data_describe[column]['type'] == 'bool':
            output[column] = random.choice([True, False])
        elif data_describe[column]['type'] == 'int':
            output[column] = random.choice(list(range(data_describe[column]['min'], data_describe[column]['max'])))
        elif data_describe[column]['type'] == 'float':
            output[column] = round(random.random() * random.choice(
                list(range(data_describe[column]['min'], data_describe[column]['max']))), 3)
        elif data_describe[column]['type'] == 'string':
            value = ''.join(random.choice(string.ascii_letters) for _ in range(data_describe[column]['length']))
            if len(value) > data_describe[column]['length']:
                output[column] = value[data_describe[column]['length'] - 1:]

    return timestamp, device_id, insert_id, json.dumps(output)


async def post_data(conn: str, auth: tuple, payloads: list):
    headers = {
        'command': 'data',
        'topic': 'telegraf-data',
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }
    json_data = json.dumps(payloads, indent=None)

    try:
        r = requests.post(f'http://{conn}', auth=auth, timeout=30, headers=headers, data=json_data)
    except Exception as e:
        raise Exception(f'Failed to send data via PUT against {conn} (Error: {e})')
    else:
        if int(r.status_code) != 200:
            raise Exception(f'Failed to send data via PUT against {conn} due to network error: {r.status_code}')


async def generate_data_for_table(table_name, data_describe):
    timestamp, device_id, insert_id, data = get_data(data_describe)
    payload = {
        "fields": data,
        "tags": {
            "table": table_name,
            "device_id": device_id,
            "insert_id": insert_id
        },
        "timestamp": timestamp
    }

    return payload


async def main():
    data_describe = read_description()
    payloads = []

    # Collect all payloads in parallel
    tasks = [generate_data_for_table(table, data_describe[table]) for table in data_describe]
    results = await asyncio.gather(*tasks)

    # Add results to the payloads list
    payloads.extend(results)

    # Now send data in batches of 25
    batch_size = 25
    for i in range(0, len(payloads), batch_size):
        batch = payloads[i:i + batch_size]
        await post_data(conn='10.0.0.131:32149', auth=(), payloads=batch)

    return len(payloads)


if __name__ == '__main__':
    print(datetime.datetime.now())
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=1)

    # while datetime.datetime.now() < end_time:
    TOTAL_INSERTS += asyncio.run(main())

    print(datetime.datetime.now())
    print(TOTAL_INSERTS)
