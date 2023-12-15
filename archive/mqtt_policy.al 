['Timestamp', 'UpdatedTime', 'ClusterName', 'HostName', 'NamespaceName', 'Owner', 'PodName', 'Labels', 'ContainerID', 'ContainerName', 'ContainerImage', 'ParentProcessName', 'ProcessName', 'HostPPID', 'HostPID', 'PPID', 'PID', 'UID', 'Type', 'Source', 'Operation', 'Resource', 'Data', 'Result']
{ontrollers",
    "ContainerImage": "mcr.microsoft
    "Timestamp": 1702313179,
    "UpdatedTime": "2023-12-11T16:46:19.061735Z",
    "ClusterName": "default",
    "HostName": "aks-agentpool-84859103-vmss000001",
    "NamespaceName": "calico-system",
    "Owner": {
        "Ref": "Deployment",
        "Name": "calico-kube-controllers",
        "Namespace": "calico-system"
    },
    "PodName": "calico-kube-controllers-57c855dd5f-qlkv5",
    "Labels": "app.kubernetes.io/name=calico-kube-controllers,k8s-app=calico-kube-controllers",
    "ContainerID": "df1eef16833abfd8d1049f6e92b3223d38be55ce7a634fc7dd7a50f0941f3719",
    "ContainerName": "calico-kube-c.com/oss/calico/kube-controllers:v3.24.6sha256:56b125578733d7932fb708a87e0926186d05306a6cc10669ab524c1f89748b03",
    "ParentProcessName": "/usr/bin/check-status",
    "ProcessName": "/usr/bin/check-status",
    "HostPPID": 2625021,
    "HostPID": 2625027,
    "PPID": 0,
    "PID": 443975,
    "UID": 999,
    "Type": "ContainerLog",
    "Source": "/usr/bin/runc",
    "Operation": "Process",
    "Resource": "/usr/bin/check-status -r",
    "Data": "syscall=SYS_EXECVE",
    "Result": "Passed"
}

<run mqtt client where broker=rest and port=!anylog_sever_port and log=false and topic=(
    name=aks and
    dbms=openhorizon and
    table="bring [hostname]" and
    column.timestamp.timestamp="bring [UpdatedTime]" and
    column.cluster_name=(type=str and value="bring [ClusterName]") and
    column.namespace=(type=str and value="bring [NamespaceName]") and
    column.owner=(type=str and value="bring [Owner][Name]" and optional=true) and
    column.owner_ref=(type=str and value="bring [Owner][Ref]" and optional=true) and
    column.owner_namespace=(type=str and value="bring [Owner][Namespace] and optional=true) and
    column.podname=(type=str and value="bring [PodName] and optional=true) and
    column.labels=(type=str and value="bring [Labels] and optional=true) and
    column.container_id=(type=str and value="bring [ContainerID] and optional=true) and
    column.container_name=(type=str and value="bring [ContainerName] and optional=true) and
    column.parent_process_name=(type=str and value="bring [ParentProcessName] and optional=true) and
    column.process_name=(type=str and value="bring [ProcessName] and optional=true) and
    column.host_ppid=(type=str and value="bring [HostPPID] and optional=true) and
    column.host_pid=(type=str and value="bring [HostPID] and optional=true) and
    column.pid=(type=str and value="bring [PID] and optional=true) and
    column.uid=(type=str and value="bring [UID] and optional=true) and
    column.type=(type=str and value="bring [Type] and optional=true) and
    column.source=(type=str and value="bring [Source] and optional=true) and
    column.operation=(type=str and value="bring [Operation] and optional=true) and
    column.data=(type=str and value="bring [Data] and optional=true) and
    column.result=(type=str and value="bring [result] and optional=true)
)>



