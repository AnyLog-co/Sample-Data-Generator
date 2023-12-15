import json
import os
import requests

SAMPLE_DATA= []

FILE_PATH = os.path.expanduser(os.path.expandvars('$HOME/Downloads/azure-k8s-cluster-telemetry.json'))

KEYS = []

with open(FILE_PATH, 'r') as f:
    for line in f.readlines():
        if list(json.loads(line).keys()) not in KEYS:
            KEYS.append(list(json.loads(line).keys()))
            SAMPLE_DATA.append(json.loads(line))

for i in range(len(KEYS)):
    print(KEYS[i])
    print(json.dumps(SAMPLE_DATA[i], indent=4))