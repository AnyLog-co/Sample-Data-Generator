import posixpath

from source.mappings import CONFIGS
from source.support import get_files_by_url

from source.mappings import VESSEL_INFO
from source.mappings import RIG_INFO
from source.mappings import WIND_TURBINE_TABLES


URL = None
TOPIC = None
FILES = None

def __check_files(source:str):
    """
    Based on user input (source) extract list of files and select mapping policies to use in code
    :args:
        source:str - source to get data from
    """
    global URL
    global TOPIC
    global FILES

    # extract config information based on source
    if not CONFIGS.get(source):
        raise ValueError(f"Failed to extract default configs for {source} cannot generate data")
    URL = CONFIGS.get(source).get("url")
    if not URL:
        raise ValueError(f"Failed to get files path for {source}")
    TOPIC = CONFIGS.get(source).get("topic")
    FILES = get_files_by_url(url=URL)


def __prep_configs(source:str, publish_group:list=None):
    """

    """
    if source == "rig":
        if publish_group is None:
            publish_group = list(RIG_INFO.keys())
        else:
            for topic in publish_group:
                if topic not in  RIG_INFO:
                    raise ValueError(f"Invalid rig {topic} in rig options")
        for topic in publish_group:
            if topic not in RIG_INFO:
                raise ValueError(f"Invalid rig {topic} in rig options")

            file_name =  RIG_INFO.get(topic).get("file")
            if file_name not in FILES:
                raise FileNotFoundError(f"Failed to to locate {posixpath.join(URL, file_name)}")

    elif source == "vessel":
        is_file = False
        if publish_group:
            for topic in publish_group:
                for fname in FILES:
                    if topic in fname:
                        is_file = True
                        break
            if not is_file:
                raise ValueError(f"Invalid vessel side(s) in vessel options")
        else:
            publish_group = ["DLB", "DLT"]

    elif source == "wind-turbine":
        if publish_group:
            if all(topic < 1 or topic == 4 or topic > 11 for topic in publish_group):
                raise ValueError(f"Invalid turbine in turbine options")
        else:
            publish_group = list(range(1, 12))
            del publish_group[3]

        for topic in publish_group:
            if f"wind_turbine_{topic}.json" not in FILES:
                raise FileNotFoundError(
                    f"Failed to locate {posixpath.join(URL, f'wind_turbine_{topic}.json')}")
    return publish_group

def main(method:str, conn, source:str, publish_group:list=None):
    """
    The following data generator is used to publish content for
    - rig
    - wind-turbine
    - vessels
    :global:
        URL:str - base URL to extract data from
        TOPIC:str - for MQTT and POST the topic used to publish data
        FILES:str - list of files (in URL) associated with source
    :args:
        method:str - format by which to publish data
        conn - connection type (REST or MQTT)
        source:str - type of data to publish
        publish_group:list - group of data to publish (Example rigs: 1 and 7 only)
    :params:
        line_count:int
        is_active:bool
        counter:int
    """
    __check_files(source=source)
    line_count = 0
    is_active = True
    counter = 0

    publish_group = __prep_configs(source=source, publish_group=publish_group)
    print(publish_group)





if __name__ == "__main__":
    main(method="POST", conn=None, source="vessel")
