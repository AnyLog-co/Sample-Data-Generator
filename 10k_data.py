import asyncio
import datetime
import json
import random
import string
import uuid
import requests
from asyncio import Semaphore

TOTAL_INSERTS = 0
run_stats = []
DESCRIBE_DATA = "describe_data.json"

# -- Functions for data description --
def describe_data():
    data = {}
    for table in range(25):
        table_name = f'table_{table + 1}'
        data[table_name] = {}
        for column in ['timestamp', 'device_id', 'insert_id']:
            data[table_name][column] = {}
            if column == 'timestamp':
                data[table_name][column]['type'] = 'datetime'
            elif column == 'device_id':
                data[table_name][column]['value'] = uuid.uuid4().__str__()
            else:
                data[table_name][column]['type'] = 'string'
        for column in range(397):
            col_name = f'column_{column + 1}'
            col_type = random.choice(['string', 'bool', 'int', 'float'])
            data[table_name][col_name] = {"type": col_type}
            if col_type in ['int', 'float']:
                data[table_name][col_name]['min'] = random.randint(1, 500)
                data[table_name][col_name]['max'] = random.randint(501, 1000)
            elif col_type == 'string':
                data[table_name][col_name]['length'] = random.randint(1, 10)
    with open(DESCRIBE_DATA, 'w') as f:
        json.dump(data, f, indent=4)
# -- Functions for data description --


def read_description():
    with open(DESCRIBE_DATA, 'r') as f:
        return json.load(f)

def get_data(data_describe):
    output = {}
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    device_id = data_describe['device_id']['value']
    insert_id = uuid.uuid4().__str__().replace("-", "")

    for column, props in data_describe.items():
        if column in ['timestamp', 'device_id', 'insert_id']:
            continue
        col_type = props['type']
        if col_type == 'bool':
            output[column] = random.choice([True, False, ""])
            output[f'quality_{column}'] = 'Nok' if output[column] is "" else 'Ok'
        elif col_type in ['int', 'float']:
            value = round(random.uniform(props['min'], props['max']), 3)
            min_value = random.choice(list(range(80, 90)))/100
            max_value = 1 + (1 - min_value)
            output[column] = int(value) if col_type == 'int' else value
            output[f'quality_{column}'] = 'Ok' if value * min_value <= value <= value * max_value else 'Nok'
        elif col_type == 'float':
            output[column] = round(random.uniform(props['min'], props['max']), 3)
        elif col_type == 'string':
            length = props['length']
            output[column] = ''.join(random.choices(string.ascii_letters, k=length))

    return timestamp, device_id, insert_id,  output


async def post_data(conn, auth, payloads):
    headers = {
        'command': 'data',
        'topic': 'telegraf-data',
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }

    for payload in payloads:
        try:
            r = requests.post(f'http://{conn}', auth=auth, timeout=30, headers=headers, data=payload)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Error posting data: {e}")


async def put_data(conn, auth, payloads):
    headers = {
        'type': 'json',
        'dbms': 'nov',
        'table': 'summary',
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.put(f'http://{conn}', auth=auth, timeout=30, headers=headers, json=payloads)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error posting data: {e}")




async def generate_data_for_table(table_name, data_describe):
    timestamp, device_id, insert_id, data = get_data(data_describe)
    return {
        "fields": data,
        "tags": {
            "table": table_name,
            "device_id": device_id,
            "insert_id": insert_id
        },
        "timestamp": timestamp
    }

async def limited_gather(semaphore, tasks):
    async with semaphore:
        return await asyncio.gather(*tasks)

async def main(run_number, parallel_threads):
    data_describe = read_description()
    payloads = []
    row_counts = {f'table_{i+1}': 0 for i in range(25)}

    semaphore = Semaphore(parallel_threads)
    tasks = [generate_data_for_table(table, data_describe[table]) for table in data_describe]
    results = await limited_gather(semaphore, tasks)

    for table, result in zip(data_describe.keys(), results):
        payloads.append(result)
        row_counts[table] += 1

    batch_size = 25
    for i in range(0, len(payloads), batch_size):
        batch = payloads[i:i + batch_size]
        serialized_batch = [json.dumps(item) for item in batch]
        await post_data(conn='10.0.0.131:32149', auth=(), payloads=serialized_batch)

    end_time = datetime.datetime.now()
    run_stats.append({
        "run_number": run_number,
        "start_time": start_time,
        "end_time": end_time,
        "total_rows": len(payloads),
        **row_counts
    })
    return len(payloads)

if __name__ == '__main__':
    # describe_data()
    print(datetime.datetime.now())
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=1)

    # Set your desired parallel threads here (1, 5, 10, 25)
    PARALLEL_THREADS = 100  # You can change this value to 1, 5, 10, or 25
    run_number = 1

    while datetime.datetime.now() < end_time:
        start_time = datetime.datetime.now()
        TOTAL_INSERTS += asyncio.run(main(run_number, PARALLEL_THREADS))
        run_number += 1

    # Generate JSON summary
    summary = {
        "start_timestamp": run_stats[0]["start_time"].strftime('%Y-%m-%d %H:%M:%S'),
        "end_timestamp": run_stats[-1]["end_time"].strftime('%Y-%m-%d %H:%M:%S'),
        "num_runs": len(run_stats),
    }

    for i in range(25):
        table_key = f"table_{i + 1}_rows"
        summary[table_key] = sum(stat[f'table_{i + 1}'] for stat in run_stats)
    summary['total_rows'] = sum(summary[f'table_{i + 1}_rows'] for i in range(25))

    # Print JSON summary to screen
    asyncio.run(put_data(conn='10.0.0.131:32149', auth=(), payloads=summary))


