import posixpath

from source.support import get_files_by_url
from source.support import read_url_content

DATA_DIR = "http://45.33.11.32/Sample-Data/proveit-data/"
PROVEIT_FILES = get_files_by_url(url=DATA_DIR)

if not PROVEIT_FILES:
    raise FileNotFoundError(f"Failed to locate files in {DATA_DIR} for Proveit Data")

def main(method:str=None, conn=None, topic:list=None, iterations:int=10, sleep:float=10):

    is_active = True
    counter = 0

    if method.upper() == "OPCUA":  # go into OPC-UA
        pass
    elif method.upper() == "MQTT":
        while is_active:
            for fname in PROVEIT_FILES:
                full_path = posixpath.join(DATA_DIR, fname)
                row = read_url_content(url=full_path, row_id=line_count)
                if topic is None or row.get("topic") in topic:
                    conn.publish(topic=row.get("topic"), payload=row.get("msg"))
                line_count += 1
                counter += 1
                if 0 < iterations <= counter:
                    time.sleep(sleep)

if __name__ == "__main__":
    main()



