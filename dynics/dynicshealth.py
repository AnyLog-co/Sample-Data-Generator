import argparse
import json
import requests

DATA = [
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',10,4293861376,779845632);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',10,4293861376,779845632);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',10,4293861376,779845632);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',8,4293861376,778874880);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',8,4293861376,778874880);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',8,4293861376,778874880);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',8,4293861376,778874880);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',8,4293861376,778874880);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',8,4293861376,778874880);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',8,4293861376,778874880);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,780001280);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,780001280);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,780001280);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,780001280);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,780001280);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,780001280);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',11,4293861376,779051008);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',11,4293861376,779051008);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',11,4293861376,779051008);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',11,4293861376,779051008);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',11,4293861376,779051008);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',11,4293861376,779051008);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',10,4293861376,778657792);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',10,4293861376,778657792);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',10,4293861376,778657792);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',10,4293861376,778657792);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',10,4293861376,778657792);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',10,4293861376,778657792);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',16,4293861376,778342400);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',16,4293861376,778342400);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',16,4293861376,778342400);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',16,4293861376,778342400);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',16,4293861376,778342400);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',16,4293861376,778342400);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',16,4293861376,778342400);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',13,4293861376,771080192);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',13,4293861376,771080192);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',13,4293861376,771080192);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',13,4293861376,771080192);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',13,4293861376,771080192);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',13,4293861376,771080192);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',12,4293861376,769503232);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',12,4293861376,769503232);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',12,4293861376,769503232);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',12,4293861376,769503232);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',12,4293861376,769503232);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',12,4293861376,769503232);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,764526592);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,764526592);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,764526592);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,764526592);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,764526592);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',7,4293861376,764526592);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',4,4293861376,763637760);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',4,4293861376,763637760);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',4,4293861376,763637760);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',4,4293861376,763637760);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',4,4293861376,763637760);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',4,4293861376,763637760);",
    "INSERT INTO dynicshealth VALUES (DEFAULT,'2023-10-25T18:41:28.734296Z',57,7,'fusion-1',4,4293861376,763637760);",
]

def put_data(conn:str=None, db_name="new_company", payload:str=""):
    headers = {
        'type': 'json',
        'dbms': db_name,
        'table': "dynicshealth",
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.put(url=f'http://{conn}', headers=headers, data=payload)
    except Exception as error:
        print(f"Failed to send data into AnyLog (Error: {error})")
        exit(1)
    else:
        if int(r.status_code) != 200:
            print(f"Failed to send data into AnyLog (Network Error: {r.status_code})")
            exit(1)


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--conn', type=str, default="10.0.0.78:7849", help="REST connection information")
    parse.add_argument('--database', type=str, default='new_company', help='Database name')
    args = parse.parse_args()
    row = {
        "name": None,
        "cpu": None,
        "memorytotal": None,
        "memoryavailable": None
    }

    for line in DATA:
        row["name"] = line.replace(");", "").split(",")[4].replace("'","")
        row["cpu"] = int(line.replace(");", "").split(",")[5])
        row["memorytotal"] = int(line.replace(");", "").split(",")[6])
        row["memoryavailable"] = int(line.replace(");", "").split(",")[7])
        put_data(conn=args.conn, payload=json.dumps(row))

if __name__ == '__main__':
    main()


