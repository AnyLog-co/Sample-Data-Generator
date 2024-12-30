import asyncio
import datetime
import orjson
import random
import string
import uuid
from asyncio import Semaphore, create_task
import aiohttp
import msgspec

# Constants
run_stats = []
DESCRIBE_DATA = "describe_data.json"
CONN = '10.0.0.131:32149'
RUN_TIME = 1  # in minutes, how long to run

async def serialize(data):
    encoder = msgspec.json.Encoder()
    return encoder.encode(data)

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
    with open(DESCRIBE_DATA, 'wb') as f:
        f.write(orjson.dumps(data))


def read_description():
    with open(DESCRIBE_DATA, 'rb') as f:
        return orjson.loads(f.read())


# -- Asynchronous Functions --
async def get_column_data(column, props):
    """Generate data for a single column asynchronously."""
    if column in ['timestamp', 'device_id']:
        return None  # Skip timestamp and device_id

    col_type = props['type']
    result = {}

    if col_type == 'bool':
        result[column] = random.choice([True, False])
        result[f'quality_{column}'] = 'Ok'
    elif col_type in ['int', 'float']:
        value = round(random.uniform(props['min'], props['max']), 3)
        result[column] = int(value) if col_type == 'int' else value
        result[f'quality_{column}'] = 'Ok'
    elif col_type == 'string':
        length = props['length']
        result[column] = ''.join(random.choices(string.ascii_letters, k=length))
        result[f'quality_{column}'] = 'Ok'

    return result


async def get_data(data_describe):
    """Generate data asynchronously for all columns except timestamp and device_id."""
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


async def post_data(session, conn, payload, retries=3, delay=2):
    """
    Asynchronously posts data to a server with retry logic.

    Args:
        session: aiohttp ClientSession object.
        conn: Connection string (e.g., "10.0.0.78:7849").
        payload: Data to be sent as JSON.
        retries: Number of retry attempts in case of failure.
        delay: Delay (in seconds) between retry attempts.
    """
    headers = {
        'command': 'data',
        'topic': 'telegraf-data',
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'application/json'
    }

    for attempt in range(retries):
        try:
            # Serialize payload to JSON if necessary
            serialized_payload = orjson.dumps(payload) if isinstance(payload, (dict, list)) else payload

            # Make POST request
            async with session.post(f'http://{conn}', data=serialized_payload, headers=headers) as response:
                if response.status == 200:
                    return  # Success
                # Raise an error for non-successful responses
                raise ConnectionError(f"Error posting data: {response.status} - {await response.text()}")

        except aiohttp.ClientConnectionError as error:
            if attempt < retries - 1:
                await asyncio.sleep(delay)  # Wait before retrying
            else:
                raise Exception(f"Failed to connect after {retries} attempts: {error}")

        except Exception as general_error:
            if attempt < retries - 1:
                await asyncio.sleep(delay)  # Wait before retrying
            else:
                raise Exception(f"Error posting data: {general_error}")


async def generate_data_for_table(session, table_name, data_describe):
    timestamp, device_id, data = await get_data(data_describe)
    payload = {
        "fields": data,
        "tags": {
            "table": table_name,
            "device_id": device_id
        },
        "timestamp": timestamp
    }

    await post_data(session, conn=CONN, payload=payload)


async def main_loop(parallel_threads, end_time):
    data_describe = read_description()
    semaphore = Semaphore(parallel_threads)
    table_names = list(data_describe.keys())

    async with aiohttp.ClientSession() as session:
        while datetime.datetime.now() <= end_time:
            async with semaphore:
                tasks = [
                    create_task(generate_data_for_table(session, table, data_describe[table])) for table in table_names
                ]
                await asyncio.gather(*tasks)


# Main Entry Point
async def main():
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=RUN_TIME)
    await main_loop(parallel_threads=100, end_time=end_time)


if __name__ == '__main__':
    asyncio.run(main())

# run client () sql nov format=table "select count(*) from table_1 where period(minute, 1, now(), insert_timestamp)"