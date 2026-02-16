import os
from wind_turbine.mapping_policy import generate_mapping_policy

def generate_mapping_policy(conn:str, data_dir:str):
    """
    1. read first row in JSON
    2. declare tables and MQTT policy
    3. declare uns policies
    """
    dir_path = os.path.expanduser(os.path.expandvars(data_dir))
    if not os.path.isdir(dir_path):
        raise IsADirectoryError(f"Failed to locate data directory {data_dir}")

    read_file = None
    is_read_file = False
    is_uns = []

    for file in os.listdir(dir_path):
        if file.endswith(".json"):
            read_file = os.path.join(dir_path, file)
            if os.path.isfile(read_file):
                if not is_read_file:
                    generate_mapping_policy(conn=conn, read_file=read_file)
                    is_read_file = True