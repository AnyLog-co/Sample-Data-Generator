import argparse
import os


from source.support import extract_credentials
from source.northbound.rest_calls import RestClient
from source.support import read_json_file
from source.northbound.rest_functions import check_policy
from source.northbound.rest_functions import declare_policy

DATA_DIR = os.path.join(os.path.dirname(__file__), "UNS")
FILES = os.listdir(DATA_DIR)

def __publish_policies(conn:RestClient, full_path:str):
    file_content = read_json_file(full_path)
    for policy in file_content:
        namespace = policy.get("uns").get("namespace")
        is_policy = check_policy(conn=conn, policy_type="uns", namespace=namespace)

        if not is_policy or is_policy is None or is_policy == "[]":
            for param in ["id", "parent", "date", "cluster"]:
                if policy.get("uns").get(param) is not None:
                    policy["uns"].pop(param)

            parent_namespace = namespace.rsplit("/", 1)[0]
            if namespace != parent_namespace:
                parent_id = check_policy(conn=conn, policy_type="uns", namespace=parent_namespace)
                policy["uns"]["parent"] = parent_id

            declare_policy(conn=conn, policy=policy)


def main(): 
    parse = argparse.ArgumentParser()
    parse.add_argument("conn", type=str, default=None, help="REST User:Passowrd@IP:Port to send UNS through")
    parse.add_argument("UNS", type=str, choices=["smart-city", "rigs"], default=None,
                       help="UNS group to publish")
    args = parse.parse_args()
    host, port, user, password = extract_credentials(args.conn)
    conn = RestClient(conn=f"{host}:{port}", auth=(user, password), timeout=30)

    if args.UNS == "smart-city":
        for file_name in ["smart_city_base.json", "smart_city_power_plant.json",
                          "smart_city_water_plant.json", "smart_city_waste_water_plant.json"]:
            full_path = os.path.join(DATA_DIR, file_name)
            if file_name not in FILES or not os.path.isfile(full_path):
                raise FileNotFoundError(f"Failed ot locate {file_name} in {DATA_DIR}")
            __publish_policies(conn=conn, full_path=full_path)
    else:
        file_name = f"{args.UNS}.json"
        full_path = os.path.join(DATA_DIR, file_name)
        if file_name not in FILES or not os.path.isfile(full_path):
            raise FileNotFoundError(f"Failed ot locate {file_name} in {DATA_DIR}")
        __publish_policies(conn=conn, full_path=full_path)


    

if __name__ == "__main__":
    main()

