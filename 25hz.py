import aiohttp
import asyncio
import datetime
import json
import orjson
import random
import string
import uuid
from asyncio import Semaphore, create_task
from collections import defaultdict


DESCRIBE_DATA = "describe_data.json"
rows_per_second = 25  # Target rows per second per table
thread_summary = defaultdict(lambda: defaultdict(int))  # Track rows per thread and second
CONN='23.92.31.110:32149'
NUM_TABLES = 25

# -- Functions for data description --
def describe_data():
    data = {}
    for table in range(NUM_TABLES):
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
    with open(DESCRIBE_DATA, 'wb') as f:
        f.write(orjson.dumps(data))
# -- Functions for data description -- #

async def post_data(session, payload):
    """ Asynchronously posts data to a server with retry logic. """
    headers = {
        'command': 'data',
        'topic': 'telegraf-data',
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'application/json'
    }
    try:
        serialized_payload = json.dumps(payload) if isinstance(payload, (dict, list)) else payload
    except Exception as error:
        raise Exception(f'Failed to serialize data to be published (Error: {error})')
    try:
        response = await session.post(f'http://{CONN}', headers=headers, data=serialized_payload)
        if response.status == 200:
            return  # Success
    except Exception as error:
        raise Exception(f'Failed to POST data to {CONN} (Error: {error})')

def read_description():
    """ Read the JSON description file. """
    with open(DESCRIBE_DATA, 'rb') as f:
        return orjson.loads(f.read())

async def get_column_data(column, props):
    """ Generate data for a single column asynchronously. """
    if column in ['timestamp', 'device_id']:
        return None  # Skip timestamp and device_id

    col_type = props['type']
    result = {}

    if col_type == 'bool':
        result[column] = random.choice(["True", "False", ""])
        result[f'quality_{column}'] = 'NOk' if result[column] else 'Ok'
    elif col_type in ['int', 'float']:
        value = round(random.uniform(props['min'], props['max']), 3)
        result[column] = int(value) if col_type == 'int' else value
        result[f'quality_{column}'] = 'Ok' if 0.75 * ((props['min'] + props['max']) / 2) <= value <= 1.25 * ((props['min'] + props['max']) / 2) else 'Nok'
    elif col_type == 'string':
        length = props['length']
        result[column] = ''.join(random.choices(string.ascii_letters, k=length))
        result[f'quality_{column}'] = 'Ok'

    return result

async def get_data(data_describe):
    """ Generate data asynchronously for all columns except timestamp and device_id. """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    device_id = data_describe['device_id']['value']

    columns = [column for column in data_describe if column not in ['timestamp', 'device_id']]
    tasks = [get_column_data(column, data_describe[column]) for column in columns]

    # Run all tasks in parallel and collect results
    results = await asyncio.gather(*tasks)

    output = {}
    for result in results:
        if result:  # Avoid None for timestamp/device_id
            output.update(result)

    return timestamp, device_id, output

async def generate_data_for_table(thread_id, table_name, data_describe):
    """ Generate data for a single table. """
    global thread_summary
    while True:
        payloads = []
        for i in range(25):  # Ensure 25 rows per timestamp
            timestamp, device_id, data = await get_data(data_describe)
            payloads.append({
                "fields": data,
                "tags": {
                    "table": table_name,
                    "device_id": device_id
                },
                "timestamp": timestamp
            })

        async with aiohttp.ClientSession() as session:
            await post_data(session=session, payload=payloads)

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Update thread summary for rows generated
        thread_summary[thread_id][current_time] += 25  # Adding 25 rows for this timestamp

        # Enforce the target rate (optional)
        await asyncio.sleep(1 / rows_per_second)

async def batch_runner(batch_id, table_name, data_describe):
    """ Run a batch with a fixed rate of row generation. """
    await generate_data_for_table(batch_id, table_name, data_describe)

async def main():
    global thread_summary
    # data_describe = describe_data()  # Now describes data and returns it
    data_describe = read_description()
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=60)  # Run for 60 seconds for demo

    # Create tasks for each batch based on the number of tables in data description
    tasks = [
        create_task(batch_runner(batch_id, table_name, data_describe[table_name]))
        for batch_id, table_name in enumerate(data_describe.keys())
    ]

    # Run all tasks until the end time
    while datetime.datetime.now() < end_time:
        await asyncio.sleep(1)  # Allow tasks to run

    # Cancel tasks after the end time
    for task in tasks:
        task.cancel()

    # Print summary
    total_rows = 0
    timestamp_summary = defaultdict(int)
    for times in thread_summary.values():
        for time, count in times.items():
            total_rows += count
            timestamp_summary[time] += count

    # Display the results
    print(f"Total rows generated: {total_rows}")
    print("Rows generated per timestamp:")
    for time, count in sorted(timestamp_summary.items()):  # Sort by timestamp for readability
        print(f"\t{time}: {count} rows")


if __name__ == '__main__':
    asyncio.run(main())



# Run 1: 3300 - beta
# Run 2: 9000
# Run 3: 9325
# Run 4: 9400
# Run 5: 3425 - beta
# Run 6: 3500 - beta
# Run 7: 9025

"""
AL ori-test-operatorX +> run client () sql nov format=table and include=(table_2, table_3, table_4, table_5) "select min(timestamp), max(timestamp), count(*) from table_1"
[8]
AL ori-test-operatorX +> 
min(timestamp)             max(timestamp)             count(*)
-------------------------- -------------------------- -------- 
2024-12-31 10:07:56.392918 2024-12-31 10:08:55.369805     2500 

{"Statistics":[{"Count": 1,
                "Time":"00:00:00",
                "Nodes": 1}]}

AL ori-test-operatorX +> get msg client 

Subscription ID: 0001
User:         unused
Broker:       rest
Connection:   Connected to local Message Server

     Messages    Success     Errors      Last message time    Last error time      Last Error
     ----------  ----------  ----------  -------------------  -------------------  ----------------------------------
           2500        2500           0  2024-12-31 18:08:58
     
     Subscribed Topics:
     Topic         QOS DBMS Table Column name Column Type Mapping Function Optional Policies                                                          
     -------------|---|----|-----|-----------|-----------|----------------|--------|-----------------------------------------------------------------|
     telegraf-data|  0|    |     |           |           |                |        |blockchain get (mapping,transform) where [id] == telegraf-mapping|
"""