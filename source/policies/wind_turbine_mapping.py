import posixpath

from source.support import get_files_by_url
from source.support import read_turbine_data


DATA_DIR = "http://45.33.11.32/Sample-Data/wind-turbine/"
TURBINE_FILES = get_files_by_url(url=DATA_DIR)

TABLE = "wind_turbine"
TOPIC = "wind-turbine"
