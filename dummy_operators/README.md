# Dummy Operator 

The following is intended to replace deploying X number of operators with tcp-services that emulate an operator. 

## Sample Data
```
{
  "cpu_percent": 8.5,
  "dbms": "example_db",
  "disk_read": 5956502,
  "disk_space": 31.4,
  "disk_write": 2764847,
  "load_avg_15min": 2.11669921875,
  "load_avg_5min": 1.79541015625,
  "node_id": 5,
  "packets_recv": 8225242,
  "packets_sent": 13016163,
  "swap_memory": 17.5,
  "table": "machine_info",
  "timestamp": "2024-09-03T20:34:42.893521Z",
  "uptime": "2:03:47:47",
  "virtual_memory": 58.9
}
```

## Process 
1. make sure to have an active master and query node running
2. update [configuration file](dummy_configs.yaml)
3. Declare operator(s) on 
```shell
python3 declare_policies.py dummy_configs.yaml --query 127.0.0.1:32349 --ledger 127.0.0.1:32049
```
4. Deploy Operator(s) 
```shell
python3 publish_data_tcp.py
```