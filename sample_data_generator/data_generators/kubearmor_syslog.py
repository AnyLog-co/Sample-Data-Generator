import random
import time

from sample_data_generator.support.timestamp_generator import generate_timestamp

SAMPLE_DATA = {
  "Host_PID": [261, 9527, 9426, 9811],
  "PPID": [1, 2396, 9663],
  "Operation": ["File", "Network"],
  "Resource": [
    "/var/log/journal/b09389c7d40f420982b5facb1f6e1686",
    "/home/chinwendu/.local/share/JetBrains/consentOptions/accepted",
    "/shm/.com.google.Chrome.h7pJqH",
    "sa_family=AF_NETLINK",
    "/home/chinwendu/.cache/google-chrome/Default/Cache/Cache_Data/todelete_3c4c59a5fecb98f5_0_1",
    "sa_family=AF_INET sin_port=443 sin_addr=142.250.187.202"
  ],
  "Data": [
    "syscall=SYS_OPENAT fd=-100 flags=O_RDONLY|O_NONBLOCK|O_DIRECTORY|O_CLOEXEC",
    "syscall=SYS_OPENAT fd=-100 flags=O_RDONLY",
    "syscall=SYS_OPENAT fd=-100 flags=O_RDWR|O_CREAT|O_EXCL",
    "syscall=SYS_BIND fd=41",
    "syscall=SYS_UNLINK",
    "syscall=SYS_CONNECT fd=43"
  ],
  "Result": ["Passed", "Failed"], # added failed
  "Hostname": ['db-node', 'srv-node', 'mail-host', 'app-node', 'app-host', 'db-server', 'db-host', 'web-server',
               'app-machine', 'srv-machine'], # randomly generated
  "PID": [261,9527,9426, 9811],
  "Type": ["HostLog"],
  "Source": ["/usr/lib/systemd/systemd-journald", "/snap/goland/224/jbr/bin/java", "/opt/google/chrome/chrome"],
  "UID": [6906, 2505, 4693, 7435, 6671, 1896, 2759, 8386, 6915, 4812] # randomly generated
}

def data_generator(db_name:str, row_count:int, sleep:float, timezone:str, timezone_range:bool=False):
    """
    Data generator for Syslog, based on kubearmor
    :url:
        https://docs.kubearmor.io/kubearmor/documentation/kubearmor-events
    :sample-json:
        ...
        "kvlistValue": {
            "values": [
                {"key": "HostPID", "value": {"doubleValue": 261}},
                {"key": "PPID", "value": {"doubleValue": 1}},
                {"key": "Operation", "value": {"stringValue": "File"}},
                {"key": "Resource", "value": {"stringValue": "/var/log/journal/b09389c7d40f420982b5facb1f6e1686"}},
                {"key": "Data", "value": {"stringValue": "syscall=SYS_OPENAT fd=-100 flags=O_RDONLY|O_NONBLOCK|O_DIRECTORY|O_CLOEXEC"}},
                {"key": "Result", "value": {"stringValue": "Passed"}},
                {"key": "UpdatedTime", "value": {"stringValue": "2023-03-27T11:10:26.485913Z"}},
                {"key": "HostName", "value": {"stringValue": "babe-chinwendum"}},
                {"key": "PID", "value": {"doubleValue": 261}},
                {"key": "Type", "value": {"stringValue": "HostLog"}},
                {"key": "Source", "value": {"stringValue": "/usr/lib/systemd/systemd-journald"}}
            ]}
        },
        ...
    :args:
        db_name:str - logical database name
    :global:
        SAMPLE_DATA:dict - data to utilize to generate payload
    :params:
        payload:dict - content to store into AnyLog
    :return:
        payload
    """
    payloads = []

    for i in range(row_count):
        payload = {
            "dbname": db_name,
            "table": "kvlistvalue",
            "UpdatedTime": generate_timestamp(timezone=timezone, enable_timezone_range=timezone_range)
        }
        for key in SAMPLE_DATA:
            payload[key.lower()] = random.choice(SAMPLE_DATA[key])
        payloads.append(payload)

        if i < row_count - 1:
            time.sleep(sleep)

    return payloads
