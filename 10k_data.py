import asyncio
import datetime
import json
import random
import string
import time
import uuid
import aiohttp
from asyncio import Semaphore, create_task

# Constants
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
            output[column] = random.choice([True, False])
            output[f'quality_{column}'] = 'Ok'
        elif col_type in ['int', 'float']:
            value = round(random.uniform(props['min'], props['max']), 3)
            output[column] = int(value) if col_type == 'int' else value
            output[f'quality_{column}'] = 'Ok'
        elif col_type == 'string':
            length = props['length']
            output[column] = ''.join(random.choices(string.ascii_letters, k=length))

    return timestamp, device_id, output


# Async HTTP Functions
async def post_data(conn, payloads):
    headers = {
        'command': 'data',
        'topic': 'telegraf-data',
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'application/json'
    }

    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for payload in payloads:
                try:
                    await session.post(f'http://{conn}', data=json.dumps(payload), headers=headers)
                except Exception as error:
                    raise Exception(f"Failed to execute POST against {conn} (Error: {error})")
            responses = await asyncio.gather(*tasks)  # Send all POST requests in parallel
            # Check responses for any errors
            for response in responses:
                if response.status != 200:
                    raise ConnectionError(f"Error posting data: {response.status} - {await response.text()}")
    except Exception as error:
        raise Exception(f"Failed to open connection session (Error: {error})")

async def put_data(conn, payloads):
    headers = {
        'type': 'json',
        'dbms': 'nov',
        'table': 'summary',
        'mode': 'streaming',
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(f'http://{conn}', json=payloads, headers=headers) as response:
            if response.status != 200:
                print(f"Error posting data: {response.status} - {await response.text()}")


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
    while True:
        if not run_stats:
            await asyncio.sleep(1)  # Sleep for 1 second and retry

        if run_stats:
            await asyncio.sleep(SUMMARY_INTERVAL)
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

            await put_data(conn='10.0.0.131:32149', payloads=summary)


# Main Loop
async def main_loop(parallel_threads, end_time):
    data_describe = read_description()
    semaphore = Semaphore(parallel_threads)
    table_names = list(data_describe.keys())

    while datetime.datetime.now() <= end_time:
        tasks = [
            create_task(generate_data_for_table(table, data_describe[table])) for table in table_names
        ]
        results = await asyncio.gather(*tasks)

        # Batch payloads for efficient transmission
        batch_size = 50  # Adjust batch size for optimal performance
        payload_batches = [results[i:i + batch_size] for i in range(0, len(results), batch_size)]

        # Concurrent POST tasks
        await post_data(conn='10.0.0.131:32149', payloads=[item for batch in payload_batches for item in batch])

        run_stats.append({
            "run_number": len(run_stats) + 1,
            "start_time": datetime.datetime.now(),
            "end_time": datetime.datetime.now(),
            "total_rows": len(results),
        })

        if datetime.datetime.now() > end_time:
            await exit(1)

    # After the time is up, we exit the loop


# Main Entry Point
async def main():
    # Set duration for the generator
    time.sleep(30)
    X_minutes = 30  # Set to desired number of minutes
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=X_minutes)

    await asyncio.gather(
        main_loop(parallel_threads=PARALLEL_THREADS, end_time=end_time),
        generate_summary()
    )


if __name__ == '__main__':
    PARALLEL_THREADS = 1  # Adjust threads for better parallelism

    asyncio.run(main())

    # run client () sql nov format=table and include=(table_24,table_15,table_18,table_25,table_7,table_14,table_19,table_11,table_12,table_20,table_2,table_5,table_21,table_13,table_17,table_8,table_1,table_6,table_3,table_22,table_9,table_16,table_10,table_4) "select min(timestamp), max(timestamp), count(*) from table_23 where insert_timestamp >= '2024-12-27 19:28:29.920843'"
