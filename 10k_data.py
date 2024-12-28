import asyncio
import datetime
import json
import random
import string
import uuid
import requests
from asyncio import Semaphore, create_task

TOTAL_INSERTS = 0
run_stats = []
DESCRIBE_DATA = "describe_data.json"
SUMMARY_INTERVAL = 60  # Interval in seconds for generating summaries

# -- Functions for data description --
def describe_data():
    data = {}
    for table in range(25):
        table_name = f'table_{table + 1}'
        data[table_name] = {}
        for column in ['timestamp', 'device_id']:
            data[table_name][column] = {}
            if column == 'timestamp':
                data[table_name][column]['type'] = 'datetime'
            elif column == 'device_id':
                data[table_name][column]['value'] = uuid.uuid4().__str__()
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

def read_description():
    with open(DESCRIBE_DATA, 'r') as f:
        return json.load(f)

def get_data(data_describe):
    output = {}
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    device_id = data_describe['device_id']['value']

    for column, props in data_describe.items():
        if column in ['timestamp', 'device_id']:
            continue
        col_type = props['type']
        if col_type == 'bool':
            output[column] = random.choice([True, False, ""])
            output[f'quality_{column}'] = 'Nok' if output[column] == "" else 'Ok'
        elif col_type in ['int', 'float']:
            value = round(random.uniform(props['min'], props['max']), 3)
            min_value = random.choice(list(range(80, 90))) / 100
            max_value = 1 + (1 - min_value)
            output[column] = int(value) if col_type == 'int' else value
            output[f'quality_{column}'] = 'Ok' if value * min_value <= value <= value * max_value else 'Nok'
        elif col_type == 'string':
            length = props['length']
            output[column] = ''.join(random.choices(string.ascii_letters, k=length))

    return timestamp, device_id, output

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
    timestamp, device_id, data = get_data(data_describe)
    return {
        "fields": data,
        "tags": {
            "table": table_name,
            "device_id": device_id
        },
        "timestamp": timestamp
    }

# Generate Summary
async def generate_summary():
    while datetime.datetime.now() < end_time:
        await asyncio.sleep(SUMMARY_INTERVAL)  # Run every minute
        summary = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "start_timestamp": run_stats[0]["start_time"].strftime('%Y-%m-%d %H:%M:%S'),
            "end_timestamp": run_stats[-1]["end_time"].strftime('%Y-%m-%d %H:%M:%S'),
            "num_runs": len(run_stats),
        }

        for i in range(25):
            table_key = f"table_{i + 1}_rows"
            summary[table_key] = sum(stat.get(f'table_{i + 1}', 0) for stat in run_stats)
        summary['total_rows'] = sum(summary[f'table_{i + 1}_rows'] for i in range(25))

        # Send summary data
        await put_data(conn='10.0.0.131:32149', auth=(), payloads=summary)

async def main_loop(parallel_threads):
    data_describe = read_description()
    semaphore = Semaphore(parallel_threads)
    table_names = list(data_describe.keys())

    while datetime.datetime.now() < end_time:
        tasks = [
            create_task(generate_data_for_table(table, data_describe[table])) for table in table_names
        ]
        results = await asyncio.gather(*tasks)

        payloads = [json.dumps(result) for result in results]
        await post_data(conn='10.0.0.131:32149', auth=(), payloads=payloads)

        # Initialize row counts for each table
        row_counts = {f'table_{i+1}': 0 for i in range(25)}

        # Increment the row counts based on data generated
        for result in results:
            table_name = result['tags']['table']
            row_counts[table_name] += 1

        run_stats.append({
            "run_number": len(run_stats) + 1,
            "start_time": datetime.datetime.now(),
            "end_time": datetime.datetime.now(),
            "total_rows": len(payloads),
            **row_counts  # Ensure that every table key is added
        })

async def main():
    # Ensure both tasks are awaited and explicitly defined as coroutines
    await asyncio.gather(
        main_loop(PARALLEL_THREADS),
        generate_summary()
    )

if __name__ == '__main__':
    describe_data()  # If needed to generate description
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    PARALLEL_THREADS = 5

    asyncio.run(main())  # Correctly pass a coroutine to asyncio.run
