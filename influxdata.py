import influxdb_client
import json
from influxdb_client import InfluxDBClient

# Your InfluxDB information
url = "https://us-central1-1.gcp.cloud2.influxdata.com"
token = "Rx494c_v3EPx5UCnDdBJGe4ENLEKwWjsuq4eQnqBHT1MxenQrXLRBOUEGGL8PFhGa5kjfF8LkL_JeVxKBO_ecw=="
org = "376aed6cc475571d"
bucket = "csobsidian's Bucket"

# Initialize the InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

# Flux query to retrieve data from the last day
query = f'''
from(bucket: "{bucket}")
  |> range(start: -1s)
  |> limit(n: 10)
  |> sort(columns: ["_time"])
'''

# Initialize query API
query_api = client.query_api()

def execute_query():
    try:
        # Run the query
        result = query_api.query(query)

        # Extract and print records as JSON
        for table in result:
            for record in table.records:
                # Create a dictionary for the JSON object
                record_dict = {
                    "time": record.get_time(),
                    "measurement": record.get_measurement(),
                    "field": record.get_field(),
                    "value": record.get_value(),
                    "tags": record.values.get('tags', {}),
                }

                # Convert the dictionary to a JSON formatted string
                record_json = json.dumps(record_dict, default=str)
                print(record_json)

    except Exception as e:
        print(f"Error: {e}")

# Execute the query
execute_query()

# Close the client connection
client.close()
