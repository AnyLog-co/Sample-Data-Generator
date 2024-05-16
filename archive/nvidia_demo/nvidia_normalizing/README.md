# Log Normalizing 
The following package is intended to provide support for normalizing (Nvidia) log files and then sending them into 
AnyLog via MQTT. 

## Sample Conversion  
| CSV Column Name | JSON Column Name |  
| :---: | :---: | 
| ts | timestamp | 
| caller | line and table_name |
| component| component | 
| msg | info | 
| latest | version | 
| URL | url | 
| app | app | 
| release | release | 
| gl2_remote_ip | ip | 
| gl2_remote_port | port |
| source |  


```csv
Date and Time,Message,Additional Details
2022-05-29T22:22:07.231Z,"2022-05-29T22:22:07.23189647Z stderr F ts=2022-05-29T22:22:07.231823023Z caller=checkpoint.go:21 component=checkpoint msg=""update available"" latest=1.4.2 URL=https://github.com/fluxcd/helm-operator/releases/tag/1.4.2","{'app': 'helm-operator', 'gl2_accounted_message_size': '484.0', 'release': 'helm-operator', 'gl2_remote_ip': '127.0.0.1', 'gl2_remote_port': '55602.0', 'streams': '[000000000000000000000001]', 'gl2_message_id': '01G48YK4KWK1PH72BW3R1EQ116', 'source': 'system-1.egx.nvidia.com', 'gl2_source_input': '624b89d37a58035d78e001fd', 'pod_name': 'helm-operator-654dffb688-c5sxl', 'namespace_name': 'helm', 'component': 'helm', 'system': 'system-1', 'container_name': 'flux-helm-operator', 'location': 'system-2', 'gl2_source_node': '28f73eb7-1879-450a-a538-2c8eede22877', '_id': 'c76b4bc0-df9d-11ec-8504-e6df01411171'}"
2022-05-29T01:27:20.765Z,"2022-05-29T01:27:20.765387019Z stderr F ts=2022-05-29T01:27:20.765348013Z caller=git.go:104 component=gitchartsync info=""starting sync of git chart sources""","{'app': 'helm-operator', 'gl2_accounted_message_size': '424.0', 'release': 'helm-operator', 'gl2_remote_ip': '127.0.0.1', 'gl2_remote_port': '59222.0', 'streams': '[000000000000000000000001]', 'gl2_message_id': '01G46PSM3B3FT638H8B1SS6FDJ', 'source': 'system-1.egx.nvidia.com', 'gl2_source_input': '624b89d37a58035d78e001fd', 'pod_name': 'helm-operator-654dffb688-8gb6x', 'namespace_name': 'helm', 'component': 'helm', 'system': 'system-1', 'container_name': 'flux-helm-operator', 'location': 'system-2', 'gl2_source_node': '5d8b6e36-5df4-4fde-adf5-991c7b6b5d07', '_id': '7e0e6ca6-deee-11ec-a0c3-46961703d653'}"
2022-05-30T01:10:15.208Z,"2022-05-30T01:10:15.208742319Z stderr F ts=2022-05-30T01:10:15.208700783Z caller=helm.go:69 component=helm version=v3 info=""beginning wait for 6 resources with timeout of 27777h46m39s"" targetNamespace=egx-system release=edge-logging","{'app': 'helm-operator', 'gl2_accounted_message_size': '500.0', 'release': 'helm-operator', 'gl2_remote_ip': '127.0.0.1', 'gl2_remote_port': '55826.0', 'streams': '[000000000000000000000001]', 'gl2_message_id': '01G4986YESDCAD5H88HE7SW8AZ', 'source': 'system-1.egx.nvidia.com', 'gl2_source_input': '624b89d37a58035d78e001fd', 'pod_name': 'helm-operator-654dffb688-c5sxl', 'namespace_name': 'helm', 'component': 'helm', 'system': 'system-1', 'container_name': 'flux-helm-operator', 'location': 'system-2', 'gl2_source_node': '28f73eb7-1879-450a-a538-2c8eede22877', '_id': '43489e8b-dfb5-11ec-8504-e6df01411171'}"
2022-05-30T00:46:32.190Z,"2022-05-30T00:46:32.190799037Z stderr F ts=2022-05-30T00:46:32.19075406Z caller=logwriter.go:28 info=""2022/05/30 00:46:32 warning: skipped value for prefix_routes: Not a table.""","{'app': 'helm-operator', 'gl2_accounted_message_size': '445.0', 'release': 'helm-operator', 'gl2_remote_ip': '127.0.0.1', 'gl2_remote_port': '33108.0', 'streams': '[000000000000000000000001]', 'gl2_message_id': '01G496VQDP73XY6ZKHZV4ERYZV', 'source': 'system-1.egx.nvidia.com', 'gl2_source_input': '624b89d37a58035d78e001fd', 'pod_name': 'helm-operator-654dffb688-c5sxl', 'namespace_name': 'helm', 'component': 'helm', 'system': 'system-1', 'container_name': 'flux-helm-operator', 'location': 'system-2', 'gl2_source_node': '5d8b6e36-5df4-4fde-adf5-991c7b6b5d07', '_id': 'f723d9eb-dfb1-11ec-a0c3-46961703d653'}"
2022-05-29T10:46:35.583Z,"2022-05-29T10:46:35.583167702Z stderr F ts=2022-05-29T10:46:35.583131175Z caller=operator.go:124 component=operator info=""stopping workers""","{'app': 'helm-operator', 'gl2_accounted_message_size': '405.0', 'release': 'helm-operator', 'gl2_remote_ip': '127.0.0.1', 'gl2_remote_port': '54634.0', 'streams': '[000000000000000000000001]', 'gl2_message_id': '01G47PSMNHV08HFVHT9Y940ZT2', 'source': 'system-1.egx.nvidia.com', 'gl2_source_input': '624b89d37a58035d78e001fd', 'pod_name': 'helm-operator-5c7cc957-hs92g', 'namespace_name': 'helm', 'component': 'helm', 'system': 'system-1', 'container_name': 'flux-helm-operator', 'location': 'system-2', 'gl2_source_node': '28f73eb7-1879-450a-a538-2c8eede22877', '_id': '9e676211-df3c-11ec-8504-e6df01411171'}"
2022-05-30T01:10:14.359Z,"2022-05-30T01:10:14.359886529Z stderr F ts=2022-05-30T01:10:14.359850166Z caller=postrender.go:77 component=release kustomizeHook=""#!/bin/bash\ncat <&0 > /tmp/kustomize2644617778/all.yaml\nkubectl kustomize /tmp/kustomize2644617778 && rm /tmp/kustomize2644617778/all.yaml"" kustomizeHookPath=/tmp/kustomize2644617778/kustomize","{'app': 'helm-operator', 'gl2_accounted_message_size': '593.0', 'release': 'helm-operator', 'gl2_remote_ip': '127.0.0.1', 'gl2_remote_port': '55826.0', 'streams': '[000000000000000000000001]', 'gl2_message_id': '01G4986YER85THQJEW9NWN2FTC', 'source': 'system-1.egx.nvidia.com', 'gl2_source_input': '624b89d37a58035d78e001fd', 'pod_name': 'helm-operator-654dffb688-c5sxl', 'namespace_name': 'helm', 'component': 'helm', 'system': 'system-1', 'container_name': 'flux-helm-operator', 'location': 'system-2', 'gl2_source_node': '28f73eb7-1879-450a-a538-2c8eede22877', '_id': '43489e7b-dfb5-11ec-8504-e6df01411171'}"
2022-05-30T01:10:14.359Z,2022-05-30T01:10:14.35945383Z stderr F ts=2022-05-30T01:10:14.359393429Z caller=release.go:565 component=release release=edge-logging targetNamespace=egx-system resource=default:helmrelease/edge-logging helmVersion=v3 UsingPostRenderer=kustomize,"{'app': 'helm-operator', 'gl2_accounted_message_size': '513.0', 'release': 'helm-operator', 'gl2_remote_ip': '127.0.0.1', 'gl2_remote_port': '55826.0', 'streams': '[000000000000000000000001]', 'gl2_message_id': '01G4986YER7S9AQ1KAPZYDAJ4N', 'source': 'system-1.egx.nvidia.com', 'gl2_source_input': '624b89d37a58035d78e001fd', 'pod_name': 'helm-operator-654dffb688-c5sxl', 'namespace_name': 'helm', 'component': 'helm', 'system': 'system-1', 'container_name': 'flux-helm-operator', 'location': 'system-2', 'gl2_source_node': '28f73eb7-1879-450a-a538-2c8eede22877', '_id': '43489e79-dfb5-11ec-8504-e6df01411171'}"
```

```JSON 
{
  "timestamp": "2022-05-29T22:22:07.231823023Z",
  "component": "checkpoint",
  "info": "update available",
  "version": "1.42",
  "url": "https://github.com/fluxcd/helm-operator/releases/tag/1.4.2",
  "line": 21
  "details": {
    "app": "helm-operator", 
    "release": "helm-operator", 
    "ip": "127.0.0.1", 
    "port": 55602, 
    "source": "system-1.egx.nvidia.com", 
    "pod": "helm-operator-654dffb688-c5sxl", 
    "app_namespace": "helm", 
    "app_component": 'helm', 
    "system": 'system-1', 
    "app_container": "flux-helm-operator", 
    "location": "system-2", 
    "node_id": "28f73eb7-1879-450a-a538-2c8eede22877", 
    "app_id": "c76b4bc0-df9d-11ec-8504-e6df01411171"
  },
  "db_name": "{USER-INPUT}"
  "table_name": "checkpoint"
}
```
