import json
import os
import requests

DIR_PATH = os.path.expanduser(os.path.expandvars('$HOME/AnyLog-Network/test/data'))
DIR_PATH_ZIP = f"{DIR_PATH}.gzip"
# for filename in os.listdir(DIR_PATH):
#
#     filepath = os.path.join(DIR_PATH, filename)
#     header = {
#         "type": "json",
#         "dbms": filename.split('.')[0],
#         "table": filename.split('.')[1],
#         "mode": "streaming",
#         'Content-Type': 'text/plain'
#     }
#     with open(filepath, 'r') as f:
#         for line in f.readlines():
#             r = requests.put(url='http://127.0.0.1:32149', headers=header)
#             input(r.status_code)

import tarfile

with tarfile.open(DIR_PATH_ZIP, 'wb') as gf:
    for filename in os.listdir(DIR_PATH):
        gf.add(filename)
