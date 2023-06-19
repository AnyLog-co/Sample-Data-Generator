import psycopg2
import requests

CREATE_STMT = """
        CREATE TABLE IF NOT EXISTS transit_map(
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            line CHAR(25),
            location GEOMETRY(Point, 4326)
        );
        CREATE INDEX IF NOT EXISTS transit_map_timestamp ON transit_map(timestamp);
    """

IP='178.79.143.174'
PORT=5432
USER='admin'
PASSWORD='passwd'
DBMS='test'


def get_data(conn:str)->list:
    content = []
    sql = 'sql test format=json and stat=false "SELECT timestamp, line, location FROM transit WHERE period(minute, 1, now(), timestamp);"'
    headers = {
        "command": sql,
        "User-Agent": "AnyLog/1.23",
        'destination': "network"
    }
    try:
        r = requests.get(url=f"http://{conn}", headers=headers)
    except Exception as error:
        print(f"Failed to get data for query {sql} (Error: {error})")
    else:
        if int(r.status_code) != 200:
            print(f"Failed to get data for query {sql} (Network Error: {r.status_code})")
        else:
            try:
                content = r.json()['Query']
            except Exception as error:
                print(f"Failed to extract result from query (Error: {error})")

    return content

def create_insert(cur:psycopg2.extensions.cursor,  content:list)->list:
    CREATE_INSERT = "INSERT INTO transit_map (timestamp, line, location) VALUES ('%s', '%s', ST_SetSRID(ST_MakePoint(%.2f, %.2f), 4326));"
    for row in content:
        long, lat = row['location'].split(",")
        print(CREATE_INSERT % (row['timestamp'], row['line'].strip(), float(long.strip()), float(lat.strip())))
        __execute_query(cur=cur, sql=CREATE_INSERT % (row['timestamp'], row['line'].strip(), float(long.strip()), float(lat.strip())))

def main():
    # Connect to the database
    conn = psycopg2.connect(dbname=DBMS, user=USER, password=PASSWORD, host=IP, port=PORT)

    # Create a cursor object
    cur = conn.cursor()

    # Enable PostGIS extension
    cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # Create a table with a `location` column of type `GEOMETRY(Point, 4326)`
    cur.execute(CREATE_STMT)

    content =

#

