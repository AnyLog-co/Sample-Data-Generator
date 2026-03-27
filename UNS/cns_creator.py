import argparse
import json

from source.northbound.rest_calls import RestClient
from source.northbound.rest_functions import declare_policy

DB_NAME = "cos"
TABLES = ["pp_pm", "pv"]
COLUMN_NAME = "monitor_id"

NAMING = {
    "KPL": "Evergy",
    "BF1": "West Feeder",
    "BF2": "East Feeder",
    "BF3": "Center Feeder",
    "BF4": "Industrial Feeder",
    "BSP": "Station Power",
    "BCT": "Bus Tie 12470/12470",
    "CBT": "Bus Tie 12470/12470",
    "CF1": "Southeast Feeder",
    "CF2": "AC Homes",
    "CF3": "North Feeder",
    "CSP": "Station Power",
    "CDT": "Bus Tie 12470/2400",
    "DCT": "Bus Tie 2400/12470",
    "DF1": "North Residence",
    "DF2": "North Main",
    "DF3": "Wenger West",
    "DF4": "South Main",
    "DSP": "Station Power",
    "BG8": "Generator 8",
    "BG9": "Generator 9",
    "BG10": "Generator 10",
    "BG11": "Generator 11",
    "CG7": "Generator 7",
    "CG12": "Generator 12",
    "DG2": "Generator 2",
    "DG3": "Generator 3",
    "DG4": "Generator 4",
    "DG5": "Generator 5",
    "DG6": "Generator 6"
}



def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("conn", type=str, default=None, help="REST IP & Port")
    args = parse.parse_args()

    conn = RestClient(conn=args.conn, auth=(),timeout=60)

    for table in TABLES:
        for orig_value, new_value in NAMING.items():
            policy = {
                "cns": {
                    # "name": f"{DB_NAME}.{table}: {orig_value} -> {new_value}",
                    "dbms": DB_NAME,
                    "table": table,
                    "column": COLUMN_NAME,
                    "orig_value": orig_value,
                    "new_value": new_value
                }
            }

            headers = {
                "command": "blockchain insert where policy=!new_policy and local=true and master=!ledger_conn",
                "User-Agent": "AnyLog/1.23"
            }

            conn.publish_data(method="POST", headers=headers, payload=f"<new_policy={json.dumps(policy)}>")


if __name__ == "__main__":
    main()