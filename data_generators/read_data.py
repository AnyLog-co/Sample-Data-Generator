import posixpath
from source.support import read_url_content
from source.support import get_files_by_url

DATA_DIR = "http://45.33.11.32/Sample-Data/rig-data/"
RIG_FILES = get_files_by_url(url=DATA_DIR)

file_path = posixpath.join(DATA_DIR, RIG_FILES[0])
line_count = 350
while True:
    row = read_url_content(file_path, line_count)
    print(line_count)
    if row is None:
        exit(1)
    else:
        print(row)
    line_count+=1
