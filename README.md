# IBM / EdgeLake demo 

The following demonstrates publishing images into IBM's AI module and getting corresponding bbox coordinates. 
The returned information and image are then stored into an EdgeLake operator node. 

## Step
1. Deploy IBM's AI tool 
2. Deploy EdgeLake 
3. On the EdgeLake side, deploy a [message client with policy](ibm_demo.al)
4. Deploy program 
```shell
python3 data_generator.py [OPERATOR_NODE_IP_PORT] \
  --batch-size [BATCH_SIZE] \
  --total-rows [TOTAL_ROWS] \
  --db-name [DB_NAME] \
  --topic [TOPIC - should be the same as EdgeLake policy] \
  --data-ip [AI Tool Connection IP:PORT] \
  --sleep [WAIT_TIME] \ 
  [--exception] 
```